@@ -11,7 +11,7 @@
 
 
 class UsernamePasswordAuth(BaseModel):
-    mode: Literal[""username_password""] = Field(""username_password"", const=True)
+    mode: Literal[""username_password""] = ""username_password""
     username: str = Field(..., title=""Username"", description=""Username for the Milvus instance"", order=1)
     password: str = Field(..., title=""Password"", description=""Password for the Milvus instance"", airbyte_secret=True, order=2)
 
@@ -22,7 +22,7 @@ class Config(OneOfOptionConfig):
 
 
 class NoAuth(BaseModel):
-    mode: Literal[""no_auth""] = Field(""no_auth"", const=True)
+    mode: Literal[""no_auth""] = ""no_auth""
 
     class Config(OneOfOptionConfig):
         title = ""No auth""
@@ -31,7 +31,7 @@ class Config(OneOfOptionConfig):
 
 
 class TokenAuth(BaseModel):
-    mode: Literal[""token""] = Field(""token"", const=True)
+    mode: Literal[""token""] = ""token""
     token: str = Field(..., title=""API Token"", description=""API Token for the Milvus instance"", airbyte_secret=True)
 
     class Config(OneOfOptionConfig):