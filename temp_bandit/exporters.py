@@ -30,10 +30,6 @@ def __init__(
         compression: Optional[Compression] = None,
         **kwargs,
     ):
-        # TODO: Implement re-authentication
-        # FIXME: endpoint here is not ""endpoint"" from config
-        # self._session = HttpClient.get_authenticated_session(endpoint, api_key)
-
         # Initialize the parent class
         super().__init__(
             endpoint=endpoint,