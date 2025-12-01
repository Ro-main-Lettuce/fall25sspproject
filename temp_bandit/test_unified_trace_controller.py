@@ -1,5 +1,5 @@
 import os
-from datetime import UTC, datetime
+from datetime import datetime
 from unittest.mock import MagicMock, patch
 from uuid import UUID
 
@@ -21,6 +21,7 @@
     trace_flow_step,
     trace_llm_call,
 )
+from crewai.utilities.datetime_compat import UTC
 
 
 class TestUnifiedTraceController: