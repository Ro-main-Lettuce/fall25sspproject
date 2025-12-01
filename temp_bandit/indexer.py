@@ -17,6 +17,7 @@
 from airbyte_cdk.models.airbyte_protocol import DestinationSyncMode
 from destination_milvus.config import MilvusIndexingConfigModel
 
+
 logger = logging.getLogger(""airbyte"")
 
 
@@ -43,7 +44,7 @@ def _connect(self):
 
         # Determine if we're using Milvus Lite
         use_lite = self.config.host.endswith("".db"")
-        
+
         try:
             connections.connect(
                 alias=""default"",
@@ -53,7 +54,7 @@ def _connect(self):
                 password=self.config.auth.password if self.config.auth.mode == ""username_password"" else """",
                 token=self.config.auth.token if self.config.auth.mode == ""token"" else """",
                 use_lite=use_lite,
-                timeout=30
+                timeout=30,
             )
             logger.info(f""Successfully connected to {'Milvus Lite' if use_lite else 'Milvus'} at {self.config.host}"")
         except Exception as e:
@@ -64,7 +65,7 @@ def _connect_with_timeout(self):
         """"""Connect to Milvus with timeout handling.""""""
         # Determine if we're using Milvus Lite
         use_lite = self.config.host.endswith("".db"")
-        
+
         if use_lite:
             # Direct connection for Milvus Lite
             try:
@@ -96,11 +97,8 @@ def _create_index(self, collection: Collection):
         }
         if not use_lite:
             index_params[""params""] = {""nlist"": 1024}
-            
-        collection.create_index(
-            field_name=self.config.vector_field,
-            index_params=index_params
-        )
+
+        collection.create_index(field_name=self.config.vector_field, index_params=index_params)
 
     def _create_client(self):
         self._connect_with_timeout()
@@ -133,7 +131,7 @@ def check(self) -> Optional[str]:
                 return f""Vector field {self.config.vector_field} not found""
             if vector_field[""type""] != DataType.FLOAT_VECTOR:
                 return f""Vector field {self.config.vector_field} is not a vector""
-            
+
             # Skip server version check for Milvus Lite
             use_lite = self.config.host.endswith("".db"")
             if not use_lite:
@@ -142,7 +140,7 @@ def check(self) -> Optional[str]:
                     logger.info(f""Connected to Milvus server version: {version}"")
                 except Exception as e:
                     logger.warning(f""Could not get server version (this is expected for Milvus Lite): {str(e)}"")
-            
+
             if vector_field[""params""][""dim""] != self.embedder_dimensions:
                 return f""Vector field {self.config.vector_field} is not a {self.embedder_dimensions}-dimensional vector""
         except Exception as e: