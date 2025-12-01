@@ -14,6 +14,7 @@
 import time
 import uuid
 from collections import defaultdict
+from collections.abc import Mapping
 from contextlib import closing, contextmanager
 from dataclasses import dataclass
 from datetime import datetime
@@ -1028,7 +1029,7 @@ def __exit__(
 
             self.env.broker.assert_no_errors()
 
-            self.env.object_storage.assert_no_errors()
+            self.env.endpoint_storage.assert_no_errors()
 
         try:
             self.overlay_cleanup_teardown()
@@ -1125,7 +1126,7 @@ def __init__(self, config: NeonEnvBuilder):
             pagectl_env_vars[""RUST_LOG""] = self.rust_log_override
         self.pagectl = Pagectl(extra_env=pagectl_env_vars, binpath=self.neon_binpath)
 
-        self.object_storage = ObjectStorage(self)
+        self.endpoint_storage = EndpointStorage(self)
 
         # The URL for the pageserver to use as its control_plane_api config
         if config.storage_controller_port_override is not None:
@@ -1182,7 +1183,7 @@ def __init__(self, config: NeonEnvBuilder):
             },
             ""safekeepers"": [],
             ""pageservers"": [],
-            ""object_storage"": {""port"": self.port_distributor.get_port()},
+            ""endpoint_storage"": {""port"": self.port_distributor.get_port()},
             ""generate_local_ssl_certs"": self.generate_local_ssl_certs,
         }
 
@@ -1254,6 +1255,7 @@ def __init__(self, config: NeonEnvBuilder):
                 ""mode"": ""pipelined"",
                 ""execution"": ""concurrent-futures"",
                 ""max_batch_size"": 32,
+                ""batching"": ""scattered-lsn"",
             }
 
             get_vectored_concurrent_io = self.pageserver_get_vectored_concurrent_io
@@ -1418,7 +1420,7 @@ def start(self, timeout_in_seconds: int | None = None):
                 self.storage_controller.on_safekeeper_deploy(sk_id, body)
                 self.storage_controller.safekeeper_scheduling_policy(sk_id, ""Active"")
 
-        self.object_storage.start(timeout_in_seconds=timeout_in_seconds)
+        self.endpoint_storage.start(timeout_in_seconds=timeout_in_seconds)
 
     def stop(self, immediate=False, ps_assert_metric_no_errors=False, fail_on_endpoint_errors=True):
         """"""
@@ -1437,7 +1439,7 @@ def stop(self, immediate=False, ps_assert_metric_no_errors=False, fail_on_endpoi
         except Exception as e:
             raise_later = e
 
-        self.object_storage.stop(immediate=immediate)
+        self.endpoint_storage.stop(immediate=immediate)
 
         # Stop storage controller before pageservers: we don't want it to spuriously
         # detect a pageserver ""failure"" during test teardown
@@ -1455,6 +1457,12 @@ def stop(self, immediate=False, ps_assert_metric_no_errors=False, fail_on_endpoi
                 except Exception as e:
                     metric_errors.append(e)
                     log.error(f""metric validation failed on {pageserver.id}: {e}"")
+
+            try:
+                pageserver.snapshot_final_metrics()
+            except Exception as e:
+                log.error(f""metric snapshot failed on {pageserver.id}: {e}"")
+
             try:
                 pageserver.stop(immediate=immediate)
             except RuntimeError:
@@ -1985,10 +1993,13 @@ def attach_hook_issue(
         tenant_shard_id: TenantId | TenantShardId,
         pageserver_id: int,
         generation_override: int | None = None,
+        config: None | dict[str, Any] = None,
     ) -> int:
         body = {""tenant_shard_id"": str(tenant_shard_id), ""node_id"": pageserver_id}
         if generation_override is not None:
             body[""generation_override""] = generation_override
+        if config is not None:
+            body[""config""] = config
 
         response = self.request(
             ""POST"",
@@ -2649,24 +2660,24 @@ def __exit__(
         self.stop(immediate=True)
 
 
-class ObjectStorage(LogUtils):
+class EndpointStorage(LogUtils):
     def __init__(self, env: NeonEnv):
-        service_dir = env.repo_dir / ""object_storage""
-        super().__init__(logfile=service_dir / ""object_storage.log"")
-        self.conf_path = service_dir / ""object_storage.json""
+        service_dir = env.repo_dir / ""endpoint_storage""
+        super().__init__(logfile=service_dir / ""endpoint_storage.log"")
+        self.conf_path = service_dir / ""endpoint_storage.json""
         self.env = env
 
     def base_url(self):
         return json.loads(self.conf_path.read_text())[""listen""]
 
     def start(self, timeout_in_seconds: int | None = None):
-        self.env.neon_cli.object_storage_start(timeout_in_seconds)
+        self.env.neon_cli.endpoint_storage_start(timeout_in_seconds)
 
     def stop(self, immediate: bool = False):
-        self.env.neon_cli.object_storage_stop(immediate)
+        self.env.neon_cli.endpoint_storage_stop(immediate)
 
     def assert_no_errors(self):
-        assert_no_errors(self.logfile, ""object_storage"", [])
+        assert_no_errors(self.logfile, ""endpoint_storage"", [])
 
 
 class NeonProxiedStorageController(NeonStorageController):
@@ -2883,13 +2894,14 @@ def restart(
         self,
         immediate: bool = False,
         timeout_in_seconds: int | None = None,
+        extra_env_vars: dict[str, str] | None = None,
     ):
         """"""
         High level wrapper for restart: restarts the process, and waits for
         tenant state to stabilize.
         """"""
         self.stop(immediate=immediate)
-        self.start(timeout_in_seconds=timeout_in_seconds)
+        self.start(timeout_in_seconds=timeout_in_seconds, extra_env_vars=extra_env_vars)
         self.quiesce_tenants()
 
     def quiesce_tenants(self):
@@ -2966,6 +2978,20 @@ def assert_no_metric_errors(self):
             value = self.http_client().get_metric_value(metric)
             assert value == 0, f""Nonzero {metric} == {value}""
 
+    def snapshot_final_metrics(self):
+        """"""
+        Take a snapshot of this pageserver's metrics and stash in its work directory.
+        """"""
+        if not self.running:
+            log.info(f""Skipping metrics snapshot on pageserver {self.id}, it is not running"")
+            return
+
+        metrics = self.http_client().get_metrics_str()
+        metrics_snapshot_path = self.workdir / ""final_metrics.txt""
+
+        with open(metrics_snapshot_path, ""w"") as f:
+            f.write(metrics)
+
     def tenant_attach(
         self,
         tenant_id: TenantId,
@@ -2978,11 +3004,12 @@ def tenant_attach(
         to call into the pageserver HTTP client.
         """"""
         client = self.http_client()
-        if generation is None:
-            generation = self.env.storage_controller.attach_hook_issue(tenant_id, self.id)
-        elif override_storage_controller_generation:
+        if generation is None or override_storage_controller_generation:
             generation = self.env.storage_controller.attach_hook_issue(
-                tenant_id, self.id, generation
+                tenant_id,
+                self.id,
+                generation_override=generation if override_storage_controller_generation else None,
+                config=config,
             )
         return client.tenant_attach(
             tenant_id,
@@ -3158,6 +3185,7 @@ def run_nonblocking(
         command: list[str],
         env: Env | None = None,
         cwd: str | Path | None = None,
+        stderr_pipe: Any | None = None,
     ) -> subprocess.Popen[Any]:
         """"""
         Run one of the postgres binaries, not waiting for it to finish
@@ -3175,7 +3203,9 @@ def run_nonblocking(
         log.info(f""Running command '{' '.join(command)}'"")
         env = self._build_env(env)
         self._log_env(env)
-        return subprocess.Popen(command, env=env, cwd=cwd, stdout=subprocess.PIPE, text=True)
+        return subprocess.Popen(
+            command, env=env, cwd=cwd, stdout=subprocess.PIPE, stderr=stderr_pipe, text=True
+        )
 
     def run(
         self,
@@ -4083,13 +4113,14 @@ def __init__(
         # try and stop the same process twice, as stop() is called by test teardown and
         # potentially by some __del__ chains in other threads.
         self._running = threading.Semaphore(0)
+        self.__jwt: str | None = None
 
-    def http_client(
-        self, auth_token: str | None = None, retries: Retry | None = None
-    ) -> EndpointHttpClient:
+    def http_client(self, retries: Retry | None = None) -> EndpointHttpClient:
+        assert self.__jwt is not None
         return EndpointHttpClient(
             external_port=self.external_http_port,
             internal_port=self.internal_http_port,
+            jwt=self.__jwt,
         )
 
     def create(
@@ -4173,6 +4204,8 @@ def create(
 
         self.config(config_lines)
 
+        self.__jwt = self.env.neon_cli.endpoint_generate_jwt(self.endpoint_id)
+
         return self
 
     def start(
@@ -4297,31 +4330,32 @@ def respec(self, **kwargs: Any) -> None:
     def respec_deep(self, **kwargs: Any) -> None:
         """"""
         Update the endpoint.json file taking into account nested keys.
-        It does one level deep update. Should enough for most cases.
         Distinct method from respec() to do not break existing functionality.
-        NOTE: This method also updates the spec.json file, not endpoint.json.
-        We need it because neon_local also writes to spec.json, so intended
+        NOTE: This method also updates the config.json file, not endpoint.json.
+        We need it because neon_local also writes to config.json, so intended
         use-case is i) start endpoint with some config, ii) respec_deep(),
         iii) call reconfigure() to apply the changes.
         """"""
-        config_path = os.path.join(self.endpoint_path(), ""spec.json"")
+
+        def update(curr, patch):
+            for k, v in patch.items():
+                if isinstance(v, Mapping):
+                    curr[k] = update(curr.get(k, {}), v)
+                else:
+                    curr[k] = v
+            return curr
+
+        config_path = os.path.join(self.endpoint_path(), ""config.json"")
         with open(config_path) as f:
-            data_dict: dict[str, Any] = json.load(f)
+            config: dict[str, Any] = json.load(f)
 
-        log.debug(""Current compute spec: %s"", json.dumps(data_dict, indent=4))
+        log.debug(""Current compute config: %s"", json.dumps(config, indent=4))
 
-        for key, value in kwargs.items():
-            if isinstance(value, dict):
-                if key not in data_dict:
-                    data_dict[key] = value
-                else:
-                    data_dict[key] = {**data_dict[key], **value}
-            else:
-                data_dict[key] = value
+        update(config, kwargs)
 
         with open(config_path, ""w"") as file:
-            log.debug(""Updating compute spec to: %s"", json.dumps(data_dict, indent=4))
-            json.dump(data_dict, file, indent=4)
+            log.debug(""Updating compute config to: %s"", json.dumps(config, indent=4))
+            json.dump(config, file, indent=4)
 
     def wait_for_migrations(self, wait_for: int = NUM_COMPUTE_MIGRATIONS) -> None:
         """"""
@@ -4338,7 +4372,7 @@ def check_migrations_done():
             wait_until(check_migrations_done)
 
     # Mock the extension part of spec passed from control plane for local testing
-    # endpooint.rs adds content of this file as a part of the spec.json
+    # endpooint.rs adds content of this file as a part of the config.json
     def create_remote_extension_spec(self, spec: dict[str, Any]):
         """"""Create a remote extension spec file for the endpoint.""""""
         remote_extensions_spec_path = os.path.join(
@@ -5126,7 +5160,6 @@ def pytest_addoption(parser: Parser):
     r""config-v1|heatmap-v1|tenant-manifest|metadata|.+\.(?:toml|pid|json|sql|conf)""
 )
 
-
 SKIP_DIRS = frozenset(
     (
         ""pg_wal"",