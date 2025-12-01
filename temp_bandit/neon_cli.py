@@ -417,14 +417,14 @@ def storage_controller_stop(self, immediate: bool, instance_id: int | None = Non
             cmd.append(f""--instance-id={instance_id}"")
         return self.raw_cli(cmd)
 
-    def object_storage_start(self, timeout_in_seconds: int | None = None):
-        cmd = [""object-storage"", ""start""]
+    def endpoint_storage_start(self, timeout_in_seconds: int | None = None):
+        cmd = [""endpoint-storage"", ""start""]
         if timeout_in_seconds is not None:
             cmd.append(f""--start-timeout={timeout_in_seconds}s"")
         return self.raw_cli(cmd)
 
-    def object_storage_stop(self, immediate: bool):
-        cmd = [""object-storage"", ""stop""]
+    def endpoint_storage_stop(self, immediate: bool):
+        cmd = [""endpoint-storage"", ""stop""]
         if immediate:
             cmd.extend([""-m"", ""immediate""])
         return self.raw_cli(cmd)
@@ -535,6 +535,18 @@ def endpoint_create(
         res.check_returncode()
         return res
 
+    def endpoint_generate_jwt(self, endpoint_id: str) -> str:
+        """"""
+        Generate a JWT for making requests to the endpoint's external HTTP
+        server.
+        """"""
+        args = [""endpoint"", ""generate-jwt"", endpoint_id]
+
+        cmd = self.raw_cli(args)
+        cmd.check_returncode()
+
+        return cmd.stdout
+
     def endpoint_start(
         self,
         endpoint_id: str,