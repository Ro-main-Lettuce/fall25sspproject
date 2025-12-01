@@ -19,11 +19,13 @@
 from opentelemetry.sdk.trace import TracerProvider
 from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                             SimpleSpanProcessor)
+from opentelemetry.trace import NonRecordingSpan, SpanContext, TraceFlags
 from opentelemetry.trace.propagation.tracecontext import \
     TraceContextTextMapPropagator
 
 from agentops.logging import logger
-from agentops.session.signals import session_ended, session_started
+from agentops.session.signals import (session_ended, session_initialized,
+                                      session_started)
 from agentops.telemetry.helpers import dict_to_span_attributes
 
 if TYPE_CHECKING:
@@ -45,12 +47,14 @@ def get_tracer_provider() -> TracerProvider:
     return _tracer_provider
 
 
-@session_started.connect
+@session_initialized.connect
 def setup_session_tracer(sender: Session, **kwargs):
-    """"""Set up and start session tracing.""""""
+    """"""When session initializes, create telemetry with non-recording span""""""
     try:
-        setattr(sender,'telemetry',SessionTelemetry(sender))
-        logger.debug(f""[{sender.session_id}] Session telemetry started"")
+        setattr(sender, ""telemetry"", SessionTelemetry(sender))
+        logger.debug(
+            f""[{sender.session_id}] Session telemetry initialized with non-recording span""
+        )
     except Exception as e:
         logger.error(f""[{sender.session_id}] Failed to initialize session tracer: {e}"")
         raise
@@ -66,6 +70,23 @@ def cleanup_session_tracer(sender: Session, **kwargs):
         logger.debug(f""[{session_id}] Session tracing cleaned up"")
 
 
+@session_started.connect
+def start_recording_session_span(sender: Session, **kwargs):
+    """"""Start recording the session span when session is actually started""""""
+    try:
+        if hasattr(sender, 'telemetry'):
+            sender.telemetry.start_recording_span()
+            # Add verification that the span was actually replaced
+            if isinstance(sender.span, NonRecordingSpan):
+                logger.error(f""[{sender.session_id}] Failed to replace NonRecordingSpan with recording span"")
+            else:
+                logger.debug(f""[{sender.session_id}] Session span started recording successfully"")
+    except Exception as e:
+        logger.error(f""[{sender.session_id}] Failed to start recording session span: {e}"")
+        import traceback
+        logger.error(traceback.format_exc())
+
+
 def get_session_tracer(session_id: str) -> Optional[SessionTelemetry]:
     """"""Get tracer for a session.""""""
     return _session_tracers.get(str(session_id))
@@ -87,31 +108,84 @@ def __init__(self, session: Session):
         self.session = session
         self._is_ended = False
         self._shutdown_lock = threading.Lock()
+        self._token = None
+        self._context = None
+        self._recording_span = None  # Initialize the recording span attribute
 
         # Use global provider
         provider = get_tracer_provider()
 
         # Set up processor and exporter
-        processor = SimpleSpanProcessor(OTLPSpanExporter(endpoint=""http://localhost:4318/v1/traces""))
-
+        processor = SimpleSpanProcessor(
+            OTLPSpanExporter(endpoint=""http://localhost:4318/v1/traces"")
+        )
         provider.add_span_processor(processor)
 
-        # Initialize tracer and root span
+        # Initialize tracer
         self.tracer = provider.get_tracer(""agentops.session"")
-        session.span = self.tracer.start_span(
-            ""session"", 
-            attributes=dict_to_span_attributes(self.session.dict())
+
+        # Create a non-recording span context
+        span_context = SpanContext(
+            trace_id=int(
+                self.session_id.replace(""-"", """")[:16], 16
+            ),  # Use part of session_id as trace_id
+            span_id=int(
+                self.session_id.replace(""-"", """")[-16:], 16
+            ),  # Use part of session_id as span_id
+            is_remote=False,
+            trace_flags=TraceFlags(0),  # 0 means not sampled (non-recording)
         )
-        
-        # Create and activate the session context immediately
-        self._context = trace.set_span_in_context(session.span)
-        self._token = context.attach(self._context)
+
+        # Create a non-recording span and assign it to session.span
+        self.session.span = NonRecordingSpan(span_context)
 
         # Store for cleanup
         _session_tracers[self.session_id] = self
         atexit.register(self.shutdown)
 
-        logger.debug(f""[{self.session_id}] Session tracer initialized"")
+        logger.debug(
+            f""[{self.session_id}] Session tracer initialized with non-recording span""
+        )
+
+    def start_recording_span(self):
+        """"""Start a recording span when the session actually starts""""""
+        # Add more detailed logging
+        logger.debug(f""[{self.session_id}] Attempting to start recording span"")
+        
+        if self._recording_span is not None:
+            logger.debug(f""[{self.session_id}] Recording span already started"")
+            return
+            
+        try:
+            # Create a real recording span with the same context as the non-recording one
+            attributes = dict_to_span_attributes(self.session.dict())
+            
+            # Make sure self.session.span is not None before using it
+            if self.session.span is None:
+                logger.error(f""[{self.session_id}] Session span is None, cannot start recording"")
+                return
+                
+            # Get the span context from the non-recording span
+            span_context = self.session.span.get_span_context()
+            
+            # Create the recording span using the context from the non-recording span
+            self._recording_span = self.tracer.start_span(
+                ""session"",
+                attributes=attributes
+            )
+            
+            # Replace the non-recording span with the recording one
+            self.session.span = self._recording_span
+            
+            # Create and activate the session context
+            self._context = trace.set_span_in_context(self.session.span)
+            self._token = context.attach(self._context)
+            
+            logger.debug(f""[{self.session_id}] Started recording session span: {type(self.session.span).__name__}"")
+        except Exception as e:
+            logger.error(f""[{self.session_id}] Error starting recording span: {e}"")
+            import traceback
+            logger.error(traceback.format_exc())
 
     def shutdown(self) -> None:
         """"""Shutdown and cleanup resources.""""""
@@ -126,7 +200,8 @@ def shutdown(self) -> None:
                 context.detach(self._token)
                 self._token = None
 
-            if self.session.span:
+            # End the span if it exists
+            if self.session.span is not None:
                 self.session.span.end()
 
             provider = trace.get_tracer_provider()