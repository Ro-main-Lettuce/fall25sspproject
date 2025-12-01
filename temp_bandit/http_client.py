@@ -1,215 +1,169 @@
 from typing import Dict, Optional
+import threading
 
 import requests
 
 from agentops.client.http.http_adapter import BaseHTTPAdapter
 from agentops.logging import logger
 from agentops.helpers.version import get_agentops_version
 
+# Import aiohttp for async requests
+try:
+    import aiohttp
+
+    AIOHTTP_AVAILABLE = True
+except ImportError:
+    AIOHTTP_AVAILABLE = False
+    # Don't log warning here, only when actually trying to use async functionality
+
 
 class HttpClient:
-    """"""Base HTTP client with connection pooling and session management""""""
+    """"""HTTP client with async-first design and optional sync fallback for log uploads""""""
 
     _session: Optional[requests.Session] = None
+    _async_session: Optional[aiohttp.ClientSession] = None
     _project_id: Optional[str] = None
+    _session_lock = threading.Lock()
 
     @classmethod
     def get_project_id(cls) -> Optional[str]:
         """"""Get the stored project ID""""""
         return cls._project_id
 
+    @classmethod
+    def set_project_id(cls, project_id: str) -> None:
+        """"""Set the project ID""""""
+        cls._project_id = project_id
+
     @classmethod
     def get_session(cls) -> requests.Session:
-        """"""Get or create the global session with optimized connection pooling""""""
+        """"""
+        Get or create the global session with optimized connection pooling.
+
+        Note: This method is deprecated. Use async_request() instead.
+        Only kept for log upload module compatibility.
+        """"""
         if cls._session is None:
-            cls._session = requests.Session()
-
-            # Configure connection pooling
-            adapter = BaseHTTPAdapter()
-
-            # Mount adapter for both HTTP and HTTPS
-            cls._session.mount(""http://"", adapter)
-            cls._session.mount(""https://"", adapter)
-
-            # Set default headers
-            cls._session.headers.update(
-                {
-                    ""Connection"": ""keep-alive"",
-                    ""Keep-Alive"": ""timeout=10, max=1000"",
-                    ""Content-Type"": ""application/json"",
-                    ""User-Agent"": f""agentops-python/{get_agentops_version() or 'unknown'}"",
-                }
-            )
-            logger.debug(f""Agentops version: agentops-python/{get_agentops_version() or 'unknown'}"")
+            with cls._session_lock:
+                if cls._session is None:  # Double-check locking
+                    cls._session = requests.Session()
+
+                    # Configure connection pooling
+                    adapter = BaseHTTPAdapter()
+
+                    # Mount adapter for both HTTP and HTTPS
+                    cls._session.mount(""http://"", adapter)
+                    cls._session.mount(""https://"", adapter)
+
+                    # Set default headers
+                    cls._session.headers.update(
+                        {
+                            ""Connection"": ""keep-alive"",
+                            ""Keep-Alive"": ""timeout=10, max=1000"",
+                            ""Content-Type"": ""application/json"",
+                            ""User-Agent"": f""agentops-python/{get_agentops_version() or 'unknown'}"",
+                        }
+                    )
+                    logger.debug(f""Agentops version: agentops-python/{get_agentops_version() or 'unknown'}"")
         return cls._session
 
-    # @classmethod
-    # def get_authenticated_session(
-    #     cls,
-    #     endpoint: str,
-    #     api_key: str,
-    #     token_fetcher: Optional[Callable[[str], str]] = None,
-    # ) -> requests.Session:
-    #     """"""
-    #     Create a new session with authentication handling.
-    #
-    #     Args:
-    #         endpoint: Base API endpoint (used to derive auth endpoint if needed)
-    #         api_key: The API key to use for authentication
-    #         token_fetcher: Optional custom token fetcher function
-    #
-    #     Returns:
-    #         A requests.Session with authentication handling
-    #     """"""
-    #     # Create auth manager with default token endpoint
-    #     auth_endpoint = f""{endpoint}/auth/token""
-    #     auth_manager = AuthManager(auth_endpoint)
-    #
-    #     # Use provided token fetcher or create a default one
-    #     if token_fetcher is None:
-    #         def default_token_fetcher(key: str) -> str:
-    #             # Simple token fetching implementation
-    #             try:
-    #                 response = requests.post(
-    #                     auth_manager.token_endpoint,
-    #                     json={""api_key"": key},
-    #                     headers={""Content-Type"": ""application/json""},
-    #                     timeout=30
-    #                 )
-    #
-    #                 if response.status_code == 401 or response.status_code == 403:
-    #                     error_msg = ""Invalid API key or unauthorized access""
-    #                     try:
-    #                         error_data = response.json()
-    #                         if ""error"" in error_data:
-    #                             error_msg = error_data[""error""]
-    #                     except Exception:
-    #                         if response.text:
-    #                             error_msg = response.text
-    #
-    #                     logger.error(f""Authentication failed: {error_msg}"")
-    #                     raise AgentOpsApiJwtExpiredException(f""Authentication failed: {error_msg}"")
-    #
-    #                 if response.status_code >= 500:
-    #                     logger.error(f""Server error during authentication: {response.status_code}"")
-    #                     raise ApiServerException(f""Server error during authentication: {response.status_code}"")
-    #
-    #                 if response.status_code != 200:
-    #                     logger.error(f""Unexpected status code during authentication: {response.status_code}"")
-    #                     raise AgentOpsApiJwtExpiredException(f""Failed to fetch token: {response.status_code}"")
-    #
-    #                 token_data = response.json()
-    #                 if ""token"" not in token_data:
-    #                     logger.error(""Token not found in response"")
-    #                     raise AgentOpsApiJwtExpiredException(""Token not found in response"")
-    #
-    #                 # Store project_id if present in the response
-    #                 if ""project_id"" in token_data:
-    #                     HttpClient._project_id = token_data[""project_id""]
-    #                     logger.debug(f""Project ID stored: {HttpClient._project_id} (will be set as {ResourceAttributes.PROJECT_ID})"")
-    #
-    #                 return token_data[""token""]
-    #             except requests.RequestException as e:
-    #                 logger.error(f""Network error during authentication: {e}"")
-    #                 raise AgentOpsApiJwtExpiredException(f""Network error during authentication: {e}"")
-    #
-    #         token_fetcher = default_token_fetcher
-    #
-    #     # Create a new session
-    #     session = requests.Session()
-    #
-    #     # Create an authenticated adapter
-    #     adapter = AuthenticatedHttpAdapter(
-    #         auth_manager=auth_manager,
-    #         api_key=api_key,
-    #         token_fetcher=token_fetcher
-    #     )
-    #
-    #     # Mount the adapter for both HTTP and HTTPS
-    #     session.mount(""http://"", adapter)
-    #     session.mount(""https://"", adapter)
-    #
-    #     # Set default headers
-    #     session.headers.update({
-    #         ""Connection"": ""keep-alive"",
-    #         ""Keep-Alive"": ""timeout=10, max=1000"",
-    #         ""Content-Type"": ""application/json"",
-    #     })
-    #
-    #     return session
+    @classmethod
+    async def get_async_session(cls) -> Optional[aiohttp.ClientSession]:
+        """"""Get or create the global async session with optimized connection pooling""""""
+        if not AIOHTTP_AVAILABLE:
+            logger.warning(""aiohttp not available, cannot create async session"")
+            return None
+
+        # Always create a new session if the current one is None or closed
+        if cls._async_session is None or cls._async_session.closed:
+            # Close the old session if it exists but is closed
+            if cls._async_session is not None and cls._async_session.closed:
+                cls._async_session = None
+
+            # Create connector with connection pooling
+            connector = aiohttp.TCPConnector(
+                limit=100,  # Total connection pool size
+                limit_per_host=30,  # Per-host connection limit
+                ttl_dns_cache=300,  # DNS cache TTL
+                use_dns_cache=True,
+                enable_cleanup_closed=True,
+            )
+
+            # Create session with default headers
+            headers = {
+                ""Content-Type"": ""application/json"",
+                ""User-Agent"": f""agentops-python/{get_agentops_version() or 'unknown'}"",
+            }
+
+            cls._async_session = aiohttp.ClientSession(
+                connector=connector, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
+            )
+
+        return cls._async_session
+
+    @classmethod
+    async def close_async_session(cls):
+        """"""Close the async session""""""
+        if cls._async_session and not cls._async_session.closed:
+            await cls._async_session.close()
+            cls._async_session = None
 
     @classmethod
-    def request(
+    async def async_request(
         cls,
         method: str,
         url: str,
         data: Optional[Dict] = None,
         headers: Optional[Dict] = None,
         timeout: int = 30,
-        max_redirects: int = 5,
-    ) -> requests.Response:
+    ) -> Optional[Dict]:
         """"""
-        Make a generic HTTP request
+        Make an async HTTP request and return JSON response
 
         Args:
             method: HTTP method (e.g., 'get', 'post', 'put', 'delete')
             url: Full URL for the request
             data: Request payload (for POST, PUT methods)
             headers: Request headers
             timeout: Request timeout in seconds
-            max_redirects: Maximum number of redirects to follow (default: 5)
 
         Returns:
-            Response from the API
-
-        Raises:
-            requests.RequestException: If the request fails
-            ValueError: If the redirect limit is exceeded or an unsupported HTTP method is used
+            JSON response as dictionary, or None if request failed
         """"""
-        session = cls.get_session()
-        method = method.lower()
-        redirect_count = 0
-
-        while redirect_count <= max_redirects:
-            # Make the request with allow_redirects=False
-            if method == ""get"":
-                response = session.get(url, headers=headers, timeout=timeout, allow_redirects=False)
-            elif method == ""post"":
-                response = session.post(url, json=data, headers=headers, timeout=timeout, allow_redirects=False)
-            elif method == ""put"":
-                response = session.put(url, json=data, headers=headers, timeout=timeout, allow_redirects=False)
-            elif method == ""delete"":
-                response = session.delete(url, headers=headers, timeout=timeout, allow_redirects=False)
-            else:
-                raise ValueError(f""Unsupported HTTP method: {method}"")
-
-            # Check if we got a redirect response
-            if response.status_code in (301, 302, 303, 307, 308):
-                redirect_count += 1
-
-                if redirect_count > max_redirects:
-                    raise ValueError(f""Exceeded maximum number of redirects ({max_redirects})"")
-
-                # Get the new location
-                if ""location"" not in response.headers:
-                    # No location header, can't redirect
-                    return response
-
-                # Update URL to the redirect location
-                url = response.headers[""location""]
-
-                # For 303 redirects, always use GET for the next request
-                if response.status_code == 303:
-                    method = ""get""
-                    data = None
-
-                logger.debug(f""Following redirect ({redirect_count}/{max_redirects}) to: {url}"")
-
-                # Continue the loop to make the next request
-                continue
-
-            # Not a redirect, return the response
-            return response
-
-        # This should never be reached due to the max_redirects check above
-        return response
+        if not AIOHTTP_AVAILABLE:
+            logger.warning(""aiohttp not available, cannot make async request"")
+            return None
+
+        try:
+            session = await cls.get_async_session()
+            if not session:
+                return None
+
+            logger.debug(f""Making async {method} request to {url}"")
+
+            # Prepare request parameters
+            kwargs = {""timeout"": aiohttp.ClientTimeout(total=timeout), ""headers"": headers or {}}
+
+            if data and method.lower() in [""post"", ""put"", ""patch""]:
+                kwargs[""json""] = data
+
+            # Make the request
+            async with session.request(method.upper(), url, **kwargs) as response:
+                logger.debug(f""Async request response status: {response.status}"")
+
+                # Check if response is successful
+                if response.status >= 400:
+                    return None
+
+                # Parse JSON response
+                try:
+                    response_data = await response.json()
+                    logger.debug(
+                        f""Async request successful, response keys: {list(response_data.keys()) if response_data else 'None'}""
+                    )
+                    return response_data
+                except Exception:
+                    return None
+
+        except Exception:
+            return None