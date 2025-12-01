@@ -10,12 +10,12 @@
 )
 
 from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY
-from agentops.instrumentation.openai.utils import (
+from opentelemetry.instrumentation.openai.utils import (
     dont_throw,
     start_as_current_span_async,
     _with_embeddings_telemetry_wrapper,
 )
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai.shared import (
     metric_shared_attributes,
     _set_client_attributes,
     _set_request_attributes,
@@ -29,9 +29,9 @@
     propagate_trace_context,
 )
 
-from agentops.instrumentation.openai.shared.config import Config
+from opentelemetry.instrumentation.openai.shared.config import Config
 
-from agentops.instrumentation.openai.utils import is_openai_v1
+from opentelemetry.instrumentation.openai.utils import is_openai_v1
 
 from opentelemetry.trace import SpanKind
 from opentelemetry.trace import Status, StatusCode