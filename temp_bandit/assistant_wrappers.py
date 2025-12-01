@@ -1,7 +1,7 @@
 import logging
 import time
 from opentelemetry import context as context_api
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai.shared import (
     _set_span_attribute,
     model_as_dict,
 )
@@ -10,8 +10,8 @@
 
 from opentelemetry.semconv_ai import SpanAttributes, LLMRequestTypeValues
 
-from agentops.instrumentation.openai.utils import _with_tracer_wrapper, dont_throw
-from agentops.instrumentation.openai.shared.config import Config
+from opentelemetry.instrumentation.openai.utils import _with_tracer_wrapper, dont_throw
+from opentelemetry.instrumentation.openai.shared.config import Config
 
 from openai._legacy_response import LegacyAPIResponse
 from openai.types.beta.threads.run import Run
@@ -218,7 +218,7 @@ def runs_create_and_stream_wrapper(tracer, wrapped, instance, args, kwargs):
     _set_span_attribute(span, f""{SpanAttributes.LLM_PROMPTS}.{i}.role"", ""system"")
     _set_span_attribute(span, f""{SpanAttributes.LLM_PROMPTS}.{i}.content"", instructions)
 
-    from agentops.instrumentation.openai.v1.event_handler_wrapper import (
+    from opentelemetry.instrumentation.openai.v1.event_handler_wrapper import (
         EventHandleWrapper,
     )
 