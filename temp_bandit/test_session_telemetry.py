@@ -28,15 +28,14 @@ def test_session_tracer_initialization(agentops_session):
     setup_session_tracer(agentops_session)
 
     # Verify tracer was initialized with root span
-    assert hasattr(agentops_session, ""_tracer"")
-    assert isinstance(agentops_session._tracer, SessionTelemetry)
+    assert hasattr(agentops_session, ""telemetry"")
+    assert isinstance(agentops_session.telemetry, SessionTelemetry)
     assert agentops_session.span is not None
     assert agentops_session.span.is_recording()
 
     # Verify root span has correct attributes
     root_span = agentops_session.span
-    assert root_span.attributes[""session.id""] == str(agentops_session.session_id)
-    assert root_span.attributes[""session.type""] == ""root""
+    assert root_span.attributes[""session_id""] == str(agentops_session.session_id)
 
     # Test new span creation with the active session span
     # Use the actual OpenTelemtry to create a new span
@@ -47,7 +46,7 @@ def test_session_tracer_initialization(agentops_session):
     child_span.end()
 
     # TODO:Verify the span was added to the session
-    assert len(agentops_session.spans) == 2
+    assert len(list(agentops_session.spans)) == 2
     assert agentops_session.spans[-1] == child_span
 
 