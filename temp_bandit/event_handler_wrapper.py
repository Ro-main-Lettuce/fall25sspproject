@@ -1,4 +1,4 @@
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai.shared import (
     _set_span_attribute,
 )
 from opentelemetry.semconv_ai import SpanAttributes