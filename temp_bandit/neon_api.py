@@ -22,19 +22,62 @@ def connection_parameters_to_env(params: dict[str, str]) -> dict[str, str]:
     }
 
 
+# Some API calls not yet implemented.
+# You may want to copy not-yet-implemented methods from the PR https://github.com/neondatabase/neon/pull/11305
 class NeonAPI:
     def __init__(self, neon_api_key: str, neon_api_base_url: str):
         self.__neon_api_key = neon_api_key
         self.__neon_api_base_url = neon_api_base_url.strip(""/"")
+        self.retry_if_possible = False
+        self.attempts = 10
+        self.sleep_before_retry = 1
+        self.retries524 = 0
+        self.retries4xx = 0
 
     def __request(self, method: str | bytes, endpoint: str, **kwargs: Any) -> requests.Response:
-        if ""headers"" not in kwargs:
-            kwargs[""headers""] = {}
+        kwargs[""headers""] = kwargs.get(""headers"", {})
         kwargs[""headers""][""Authorization""] = f""Bearer {self.__neon_api_key}""
 
-        resp = requests.request(method, f""{self.__neon_api_base_url}{endpoint}"", **kwargs)
-        log.debug(""%s %s returned a %d: %s"", method, endpoint, resp.status_code, resp.text)
-        resp.raise_for_status()
+        for attempt in range(self.attempts):
+            retry = False
+            resp = requests.request(method, f""{self.__neon_api_base_url}{endpoint}"", **kwargs)
+            if resp.status_code >= 400:
+                log.error(
+                    ""%s %s returned a %d: %s"",
+                    method,
+                    endpoint,
+                    resp.status_code,
+                    resp.text if resp.status_code != 524 else ""CloudFlare error page"",
+                )
+            else:
+                log.debug(""%s %s returned a %d: %s"", method, endpoint, resp.status_code, resp.text)
+            if not self.retry_if_possible:
+                resp.raise_for_status()
+                break
+            elif resp.status_code >= 400:
+                if resp.status_code == 422:
+                    if resp.json()[""message""] == ""branch not ready yet"":
+                        retry = True
+                        self.retries4xx += 1
+                elif resp.status_code == 423 and resp.json()[""message""] in {
+                    ""endpoint is in some transitive state, could not suspend"",
+                    ""project already has running conflicting operations, scheduling of new ones is prohibited"",
+                }:
+                    retry = True
+                    self.retries4xx += 1
+                elif resp.status_code == 524:
+                    log.info(""The request was timed out, trying to get operations"")
+                    retry = True
+                    self.retries524 += 1
+            if retry:
+                log.info(""Retrying, attempt %s/%s"", attempt + 1, self.attempts)
+                time.sleep(self.sleep_before_retry)
+                continue
+            else:
+                resp.raise_for_status()
+            break
+        else:
+            raise RuntimeError(""Max retry count is reached"")
 
         return resp
 
@@ -101,6 +144,96 @@ def delete_project(
 
         return cast(""dict[str, Any]"", resp.json())
 
+    def create_branch(
+        self,
+        project_id: str,
+        branch_name: str | None = None,
+        parent_id: str | None = None,
+        parent_lsn: str | None = None,
+        parent_timestamp: str | None = None,
+        protected: bool | None = None,
+        archived: bool | None = None,
+        init_source: str | None = None,
+        add_endpoint=True,
+    ) -> dict[str, Any]:
+        data: dict[str, Any] = {}
+        if add_endpoint:
+            data[""endpoints""] = [{""type"": ""read_write""}]
+        data[""branch""] = {}
+        if parent_id:
+            data[""branch""][""parent_id""] = parent_id
+        if branch_name:
+            data[""branch""][""name""] = branch_name
+        if parent_lsn is not None:
+            data[""branch""][""parent_lsn""] = parent_lsn
+        if parent_timestamp is not None:
+            data[""branch""][""parent_timestamp""] = parent_timestamp
+        if protected is not None:
+            data[""branch""][""protected""] = protected
+        if init_source is not None:
+            data[""branch""][""init_source""] = init_source
+        if archived is not None:
+            data[""branch""][""archived""] = archived
+        if not data[""branch""]:
+            data.pop(""branch"")
+        resp = self.__request(
+            ""POST"",
+            f""/projects/{project_id}/branches"",
+            headers={
+                ""Accept"": ""application/json"",
+                ""Content-Type"": ""application/json"",
+            },
+            json=data,
+        )
+        return cast(""dict[str, Any]"", resp.json())
+
+    def get_branch_details(self, project_id: str, branch_id: str) -> dict[str, Any]:
+        resp = self.__request(
+            ""GET"",
+            f""/projects/{project_id}/branches/{branch_id}"",
+            headers={
+                ""Accept"": ""application/json"",
+            },
+        )
+        return cast(""dict[str, Any]"", resp.json())
+
+    def delete_branch(self, project_id: str, branch_id: str) -> dict[str, Any]:
+        resp = self.__request(
+            ""DELETE"",
+            f""/projects/{project_id}/branches/{branch_id}"",
+            headers={
+                ""Accept"": ""application/json"",
+            },
+        )
+        return cast(""dict[str, Any]"", resp.json())
+
+    def restore_branch(
+        self,
+        project_id: str,
+        branch_id: str,
+        source_branch_id: str,
+        source_lsn: str | None,
+        source_timestamp: str | None,
+        preserve_under_name: str | None,
+    ):
+        data = {""source_branch_id"": source_branch_id}
+        if source_lsn:
+            data[""source_lsn""] = source_lsn
+        if source_timestamp:
+            data[""source_timestamp""] = source_timestamp
+        if preserve_under_name:
+            data[""preserve_under_name""] = preserve_under_name
+        log.info(""Data: %s"", data)
+        resp = self.__request(
+            ""POST"",
+            f""/projects/{project_id}/branches/{branch_id}/restore"",
+            headers={
+                ""Accept"": ""application/json"",
+            },
+            json=data,
+        )
+        return cast(""dict[str, Any]"", resp.json())
+
     def start_endpoint(
         self,
         project_id: str,
@@ -176,6 +309,10 @@ def create_endpoint(
 
         return cast(""dict[str, Any]"", resp.json())
 
+    def delete_endpoint(self, project_id: str, endpoint_id: str) -> dict[str, Any]:
+        resp = self.__request(""DELETE"", f""/projects/{project_id}/endpoints/{endpoint_id}"")
+        return cast(""dict[str,Any]"", resp.json())
+
     def get_connection_uri(
         self,
         project_id: str,