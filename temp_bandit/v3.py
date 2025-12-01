@@ -6,7 +6,7 @@
 
 from agentops.client.api.base import BaseApiClient
 from agentops.client.api.types import AuthTokenResponse
-from agentops.exceptions import ApiServerException
+from agentops.client.http.http_client import HttpClient
 from agentops.logging import logger
 from termcolor import colored
 
@@ -24,42 +24,46 @@ def __init__(self, endpoint: str):
         # Set up with V3-specific auth endpoint
         super().__init__(endpoint)
 
-    def fetch_auth_token(self, api_key: str) -> AuthTokenResponse:
-        path = ""/v3/auth/token""
-        data = {""api_key"": api_key}
-        headers = self.prepare_headers()
-
-        r = self.post(path, data, headers)
+    async def fetch_auth_token(self, api_key: str) -> AuthTokenResponse:
+        """"""
+        Asynchronously fetch authentication token.
 
-        if r.status_code != 200:
-            error_msg = f""Authentication failed: {r.status_code}""
-            try:
-                error_data = r.json()
-                if ""error"" in error_data:
-                    error_msg = f""{error_data['error']}""
-            except Exception:
-                pass
-            logger.error(f""{error_msg} - Perhaps an invalid API key?"")
-            raise ApiServerException(error_msg)
+        Args:
+            api_key: The API key to authenticate with
 
+        Returns:
+            AuthTokenResponse containing token and project information, or None if failed
+        """"""
         try:
-            jr = r.json()
-            token = jr.get(""token"")
+            path = ""/v3/auth/token""
+            data = {""api_key"": api_key}
+            headers = self.prepare_headers()
+
+            # Build full URL
+            url = self._get_full_url(path)
+
+            # Make async request
+            response_data = await HttpClient.async_request(
+                method=""POST"", url=url, data=data, headers=headers, timeout=30
+            )
+
+            token = response_data.get(""token"")
             if not token:
-                raise ApiServerException(""No token in authentication response"")
+                logger.warning(""Authentication failed: Perhaps an invalid API key?"")
+                return None
 
             # Check project premium status
-            if jr.get(""project_prem_status"") != ""pro"":
+            if response_data.get(""project_prem_status"") != ""pro"":
                 logger.info(
                     colored(
                         ""\x1b[34mYou're on the agentops free plan 🤔\x1b[0m"",
                         ""blue"",
                     )
                 )
 
-            return jr
-        except Exception as e:
-            logger.error(f""Failed to process authentication response: {str(e)}"")
-            raise ApiServerException(f""Failed to process authentication response: {str(e)}"")
+            return response_data
+
+        except Exception:
+            return None
 
     # Add V3-specific API methods here