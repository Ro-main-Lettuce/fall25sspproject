@@ -1,10 +1,9 @@
 import logging
 from typing import Any, Dict, Literal, Optional, Type
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 
-from crewai_tools.tools.base_tool import BaseTool
-
 logger = logging.getLogger(__file__)
 
 