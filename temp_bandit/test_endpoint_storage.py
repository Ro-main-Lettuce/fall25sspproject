@@ -8,7 +8,7 @@
 
 
 @pytest.mark.asyncio
-async def test_object_storage_insert_retrieve_delete(neon_simple_env: NeonEnv):
+async def test_endpoint_storage_insert_retrieve_delete(neon_simple_env: NeonEnv):
     """"""
     Inserts, retrieves, and deletes test file using a JWT token
     """"""
@@ -31,7 +31,7 @@ async def test_object_storage_insert_retrieve_delete(neon_simple_env: NeonEnv):
     token.make_signed_token(key)
     token = token.serialize()
 
-    base_url = env.object_storage.base_url()
+    base_url = env.endpoint_storage.base_url()
     key = f""http://{base_url}/{tenant_id}/{timeline_id}/{endpoint_id}/key""
     headers = {""Authorization"": f""Bearer {token}""}
     log.info(f""cache key url {key}"")