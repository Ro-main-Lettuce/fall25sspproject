@@ -6,7 +6,7 @@
 import warnings
 from concurrent.futures import ThreadPoolExecutor
 from textwrap import indent
-from typing import TYPE_CHECKING, Any
+from typing import TYPE_CHECKING
 
 import sqlalchemy
 from overrides import overrides
@@ -39,44 +39,44 @@ class SnowflakeConfig(SqlConfig):
     account: str
     username: str
     password: SecretString | None = None
-    private_key_path: str | None = None
-    private_key_passphrase: SecretString | None = None
+    private_key_file: str | None = None
+    private_key_file_pwd: SecretString | None = None
     warehouse: str
     database: str
     role: str
     schema_name: str = Field(default=DEFAULT_CACHE_SCHEMA_NAME)
     data_retention_time_in_days: int | None = None
 
-    @validator(""password"", ""private_key_path"")
+    @validator(""password"", ""private_key_file"")
     @classmethod
     def validate_auth_method(
-        cls, v: str | SecretString | None, values: dict[str, Any]
+        cls, v: str | SecretString | None, values: dict[str, object]
     ) -> str | SecretString | None:
         """"""Validate that at least one authentication method is provided.""""""
         if (
             ""password"" in values
             and values[""password""] is None
-            and ""private_key_path"" in values
-            and values[""private_key_path""] is None
+            and ""private_key_file"" in values
+            and values[""private_key_file""] is None
         ):
-            raise ValueError(""Either password or private_key_path must be provided"")
+            raise ValueError(""Either password or private_key_file must be provided"")
 
         if (
-            ""private_key_passphrase"" in values
-            and values[""private_key_passphrase""] is not None
-            and (""private_key_path"" not in values or values[""private_key_path""] is None)
+            ""private_key_file_pwd"" in values
+            and values[""private_key_file_pwd""] is not None
+            and (""private_key_file"" not in values or values[""private_key_file""] is None)
         ):
             raise ValueError(
-                ""private_key_passphrase can only be provided when private_key_path is provided""
+                ""private_key_file_pwd can only be provided when private_key_file is provided""
             )
 
         return v
 
-    def __init__(self, **data: Any) -> None:
+    def __init__(self, **data: object) -> None:
         """"""Initialize the SnowflakeConfig with a deprecation warning for password authentication.""""""
         super().__init__(**data)
 
-        if self.password is not None and self.private_key_path is None:
+        if self.password is not None and self.private_key_file is None:
             warnings.warn(
                 ""Password authentication for Snowflake is deprecated and will be removed in a ""
                 ""future version. Please use key-pair authentication instead."",
@@ -113,10 +113,10 @@ def get_sql_alchemy_url(self) -> SecretString:
 
         if self.password:
             url_params[""password""] = self.password
-        elif self.private_key_path:
-            url_params[""private_key_path""] = self.private_key_path
-            if self.private_key_passphrase:
-                url_params[""private_key_passphrase""] = self.private_key_passphrase
+        elif self.private_key_file:
+            url_params[""private_key_file""] = self.private_key_file
+            if self.private_key_file_pwd:
+                url_params[""private_key_file_pwd""] = self.private_key_file_pwd
 
         return SecretString(URL(**url_params))
 
@@ -133,10 +133,10 @@ def get_vendor_client(self) -> object:
 
         if self.password:
             connection_params[""password""] = self.password
-        elif self.private_key_path:
-            connection_params[""private_key_path""] = self.private_key_path
-            if self.private_key_passphrase:
-                connection_params[""private_key_passphrase""] = self.private_key_passphrase
+        elif self.private_key_file:
+            connection_params[""private_key_file""] = self.private_key_file
+            if self.private_key_file_pwd:
+                connection_params[""private_key_file_pwd""] = self.private_key_file_pwd
 
         return connector.connect(**connection_params)
 