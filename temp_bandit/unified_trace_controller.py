@@ -1,6 +1,6 @@
 import inspect
 import os
-from datetime import UTC, datetime
+from datetime import datetime
 from functools import wraps
 from typing import Any, Awaitable, Callable, Dict, List, Optional
 from uuid import uuid4
@@ -14,6 +14,7 @@
     LLMResponse,
     ToolCall,
 )
+from crewai.utilities.datetime_compat import UTC
 
 
 class UnifiedTraceController: