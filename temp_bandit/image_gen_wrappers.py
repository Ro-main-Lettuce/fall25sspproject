@@ -1,13 +1,13 @@
 import time
 
 from opentelemetry import context as context_api
-from agentops.instrumentation.openai import is_openai_v1
-from agentops.instrumentation.openai.shared import (
+from opentelemetry.instrumentation.openai import is_openai_v1
+from opentelemetry.instrumentation.openai.shared import (
     _get_openai_base_url,
     metric_shared_attributes,
     model_as_dict,
 )
-from agentops.instrumentation.openai.utils import (
+from opentelemetry.instrumentation.openai.utils import (
     _with_image_gen_metric_wrapper,
 )
 from opentelemetry.instrumentation.utils import _SUPPRESS_INSTRUMENTATION_KEY