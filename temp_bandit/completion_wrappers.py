@@ -9,8 +9,8 @@
 )
 
 from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY
-from agentops.instrumentation.openai.utils import _with_tracer_wrapper, dont_throw
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai.utils import _with_tracer_wrapper, dont_throw
+from opentelemetry.instrumentation.openai.shared import (
     _set_client_attributes,
     _set_request_attributes,
     _set_span_attribute,
@@ -25,12 +25,12 @@
     propagate_trace_context,
 )
 
-from agentops.instrumentation.openai.utils import is_openai_v1
+from opentelemetry.instrumentation.openai.utils import is_openai_v1
 
 from opentelemetry.trace import SpanKind
 from opentelemetry.trace.status import Status, StatusCode
 
-from agentops.instrumentation.openai.shared.config import Config
+from opentelemetry.instrumentation.openai.shared.config import Config
 
 SPAN_NAME = ""openai.completion""
 LLM_REQUEST_TYPE = LLMRequestTypeValues.COMPLETION