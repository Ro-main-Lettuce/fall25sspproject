@@ -5,7 +5,7 @@
 
 from typing import Optional
 
-from pydantic import BaseModel, Extra
+from pydantic import BaseModel, Extra, Field
 from typing_extensions import Literal
 
 
@@ -16,3 +16,7 @@ class Config:
     sl: Optional[Literal[0, 100, 200, 300]] = None
     ql: Optional[Literal[0, 100, 200, 300, 400, 500, 600]] = None
     isEnterprise: Optional[bool] = False
+    requireVersionIncrementsInPullRequests: Optional[bool] = Field(
+        True,
+        description=""When false, version increment checks will be skipped for this connector"",
+    )