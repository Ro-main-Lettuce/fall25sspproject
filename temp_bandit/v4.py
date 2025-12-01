@@ -4,18 +4,22 @@
 This module provides the client for the V4 version of the AgentOps API.
 """"""
 
-from typing import Optional, Union, Dict
+from typing import Optional, Union, Dict, Any
 
+import requests
 from agentops.client.api.base import BaseApiClient
+from agentops.client.http.http_client import HttpClient
 from agentops.exceptions import ApiServerException
-from agentops.client.api.types import UploadedObjectResponse
 from agentops.helpers.version import get_agentops_version
 
 
 class V4Client(BaseApiClient):
     """"""Client for the AgentOps V4 API""""""
 
-    auth_token: str
+    def __init__(self, endpoint: str):
+        """"""Initialize the V4 API client.""""""
+        super().__init__(endpoint)
+        self.auth_token: Optional[str] = None
 
     def set_auth_token(self, token: str):
         """"""
@@ -36,69 +40,106 @@ def prepare_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Di
             Headers dictionary with standard headers and any custom headers
         """"""
         headers = {
-            ""Authorization"": f""Bearer {self.auth_token}"",
             ""User-Agent"": f""agentops-python/{get_agentops_version() or 'unknown'}"",
         }
+
+        # Only add Authorization header if we have a token
+        if self.auth_token:
+            headers[""Authorization""] = f""Bearer {self.auth_token}""
+
         if custom_headers:
             headers.update(custom_headers)
         return headers
 
-    def upload_object(self, body: Union[str, bytes]) -> UploadedObjectResponse:
+    def post(self, path: str, body: Union[str, bytes], headers: Optional[Dict[str, str]] = None) -> requests.Response:
         """"""
-        Upload an object to the API and return the response.
+        Make a POST request to the V4 API.
 
         Args:
-            body: The object to upload, either as a string or bytes.
+            path: The API path to POST to
+            body: The request body (string or bytes)
+            headers: Optional headers to include
+
         Returns:
-            UploadedObjectResponse: The response from the API after upload.
+            The response object
         """"""
-        if isinstance(body, bytes):
-            body = body.decode(""utf-8"")
+        url = self._get_full_url(path)
+        request_headers = headers or self.prepare_headers()
 
-        response = self.post(""/v4/objects/upload/"", body, self.prepare_headers())
+        return HttpClient.get_session().post(url, json={""body"": body}, headers=request_headers, timeout=30)
 
-        if response.status_code != 200:
-            error_msg = f""Upload failed: {response.status_code}""
-            try:
-                error_data = response.json()
-                if ""error"" in error_data:
-                    error_msg = error_data[""error""]
-            except Exception:
-                pass
-            raise ApiServerException(error_msg)
+    def upload_object(self, body: Union[str, bytes]) -> Dict[str, Any]:
+        """"""
+        Upload an object to the V4 API.
+
+        Args:
+            body: The object body to upload
+
+        Returns:
+            Dictionary containing upload response data
 
+        Raises:
+            ApiServerException: If the upload fails
+        """"""
         try:
-            response_data = response.json()
-            return UploadedObjectResponse(**response_data)
-        except Exception as e:
-            raise ApiServerException(f""Failed to process upload response: {str(e)}"")
+            # Convert bytes to string for consistency with test expectations
+            if isinstance(body, bytes):
+                body = body.decode(""utf-8"")
+
+            response = self.post(""/v4/objects/upload/"", body, self.prepare_headers())
+
+            if response.status_code != 200:
+                error_msg = f""Upload failed: {response.status_code}""
+                try:
+                    error_data = response.json()
+                    if ""error"" in error_data:
+                        error_msg = error_data[""error""]
+                except:
+                    pass
+                raise ApiServerException(error_msg)
+
+            try:
+                return response.json()
+            except Exception as e:
+                raise ApiServerException(f""Failed to process upload response: {str(e)}"")
+        except requests.exceptions.RequestException as e:
+            raise ApiServerException(f""Failed to upload object: {e}"")
 
-    def upload_logfile(self, body: Union[str, bytes], trace_id: int) -> UploadedObjectResponse:
+    def upload_logfile(self, body: Union[str, bytes], trace_id: str) -> Dict[str, Any]:
         """"""
-        Upload an log file to the API and return the response.
+        Upload a logfile to the V4 API.
 
         Args:
-            body: The log file to upload, either as a string or bytes.
+            body: The logfile content to upload
+            trace_id: The trace ID associated with the logfile
+
         Returns:
-            UploadedObjectResponse: The response from the API after upload.
-        """"""
-        if isinstance(body, bytes):
-            body = body.decode(""utf-8"")
+            Dictionary containing upload response data
 
-        response = self.post(""/v4/logs/upload/"", body, {**self.prepare_headers(), ""Trace-Id"": str(trace_id)})
+        Raises:
+            ApiServerException: If the upload fails
+        """"""
+        try:
+            # Convert bytes to string for consistency with test expectations
+            if isinstance(body, bytes):
+                body = body.decode(""utf-8"")
+
+            headers = {**self.prepare_headers(), ""Trace-Id"": str(trace_id)}
+            response = self.post(""/v4/logs/upload/"", body, headers)
+
+            if response.status_code != 200:
+                error_msg = f""Upload failed: {response.status_code}""
+                try:
+                    error_data = response.json()
+                    if ""error"" in error_data:
+                        error_msg = error_data[""error""]
+                except:
+                    pass
+                raise ApiServerException(error_msg)
 
-        if response.status_code != 200:
-            error_msg = f""Upload failed: {response.status_code}""
             try:
-                error_data = response.json()
-                if ""error"" in error_data:
-                    error_msg = error_data[""error""]
-            except Exception:
-                pass
-            raise ApiServerException(error_msg)
-
-        try:
-            response_data = response.json()
-            return UploadedObjectResponse(**response_data)
-        except Exception as e:
-            raise ApiServerException(f""Failed to process upload response: {str(e)}"")
+                return response.json()
+            except Exception as e:
+                raise ApiServerException(f""Failed to process upload response: {str(e)}"")
+        except requests.exceptions.RequestException as e:
+            raise ApiServerException(f""Failed to upload logfile: {e}"")