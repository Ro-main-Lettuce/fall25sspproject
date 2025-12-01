@@ -1,11 +1,10 @@
 from typing import Any, Type, Union
 
+from crewai.tools import BaseTool
 from pydantic import BaseModel, Field
 from sqlalchemy import create_engine, text
 from sqlalchemy.orm import sessionmaker
 
-from ..base_tool import BaseTool
-
 
 class NL2SQLToolInput(BaseModel):
     sql_query: str = Field(