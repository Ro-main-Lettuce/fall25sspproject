@@ -2,7 +2,7 @@
 import json
 import logging
 import time
-from agentops.instrumentation.openai.shared.config import Config
+from opentelemetry.instrumentation.openai.shared.config import Config
 from wrapt import ObjectProxy
 
 
@@ -15,12 +15,12 @@
 )
 
 from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY
-from agentops.instrumentation.openai.utils import (
+from opentelemetry.instrumentation.openai.utils import (
     _with_chat_telemetry_wrapper,
     dont_throw,
     run_async,
 )
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai.shared import (
     metric_shared_attributes,
     _set_client_attributes,
     _set_request_attributes,
@@ -42,8 +42,7 @@
 from opentelemetry.trace import SpanKind, Tracer
 from opentelemetry.trace.status import Status, StatusCode
 
-from agentops.instrumentation.openai.utils import is_openai_v1
-from agentops.instrumentation.context import get_current_session
+from opentelemetry.instrumentation.openai.utils import is_openai_v1
 
 SPAN_NAME = ""openai.chat""
 PROMPT_FILTER_KEY = ""prompt_filter_results""
@@ -86,8 +85,22 @@ def chat_wrapper(
         start_time = time.time()
         response = wrapped(*args, **kwargs)
         end_time = time.time()
-    except Exception as e:
-        _handle_error(e)
+    except Exception as e:  # pylint: disable=broad-except
+        end_time = time.time()
+        duration = end_time - start_time if ""start_time"" in locals() else 0
+
+        attributes = {
+            ""error.type"": e.__class__.__name__,
+        }
+
+        if duration > 0 and duration_histogram:
+            duration_histogram.record(duration, attributes=attributes)
+        if exception_counter:
+            exception_counter.add(1, attributes=attributes)
+
+        span.set_status(Status(StatusCode.ERROR, str(e)))
+        span.end()
+
         raise e
 
     if is_streaming_response(response):
@@ -165,8 +178,24 @@ async def achat_wrapper(
         start_time = time.time()
         response = await wrapped(*args, **kwargs)
         end_time = time.time()
-    except Exception as e:
-        _handle_error(e)
+    except Exception as e:  # pylint: disable=broad-except
+        end_time = time.time()
+        duration = end_time - start_time if ""start_time"" in locals() else 0
+
+        common_attributes = Config.get_common_metrics_attributes()
+        attributes = {
+            **common_attributes,
+            ""error.type"": e.__class__.__name__,
+        }
+
+        if duration > 0 and duration_histogram:
+            duration_histogram.record(duration, attributes=attributes)
+        if exception_counter:
+            exception_counter.add(1, attributes=attributes)
+
+        span.set_status(Status(StatusCode.ERROR, str(e)))
+        span.end()
+
         raise e
 
     if is_streaming_response(response):
@@ -216,9 +245,7 @@ async def achat_wrapper(
 
 @dont_throw
 async def _handle_request(span, kwargs, instance):
-    """"""Handle the request phase of the chat completion""""""
-    # Pass instance to _set_request_attributes
-    _set_request_attributes(span, kwargs, instance)
+    _set_request_attributes(span, kwargs)
     _set_client_attributes(span, instance)
     if should_send_prompts():
         await _set_prompts(span, kwargs.get(""messages""))
@@ -857,14 +884,3 @@ def _accumulate_stream_items(item, complete_response):
                     span_function[""name""] = tool_call_function.get(""name"")
                 if tool_call_function and tool_call_function.get(""arguments""):
                     span_function[""arguments""] += tool_call_function.get(""arguments"")
-
-
-def _handle_error(e: Exception):
-    """"""Handle errors in session context""""""
-    session = get_current_session()
-    if session:
-        session.event_counts[""errors""] += 1
-        
-        # If session is still running, mark as failed
-        if session.is_running:
-            session.end(""FAILED"", f""OpenAI error: {str(e)}"")