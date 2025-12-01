@@ -1,9 +1,11 @@
-import pytest
 from unittest.mock import MagicMock, patch
 
+import pytest
+from pydantic import BaseModel, Field
+
 from crewai import Agent, Crew, Task
 from crewai.utilities.converter import Converter
-from pydantic import BaseModel, Field
+
 
 class ResponseFormat(BaseModel):
     string: str = Field(description='string needs to be maintained')