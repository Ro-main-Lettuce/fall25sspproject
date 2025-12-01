@@ -107,9 +107,9 @@ def _get_cache_path(self, key: str, *, is_read: bool = False) -> Path:
             The path to the cache file.
         """"""
         base_dir = self.read_dir if is_read else self.cache_dir
-        
+
         extension = "".json"" if self.serialization_format == SerializationFormat.JSON else "".mitm""
-        
+
         return base_dir / f""{key}{extension}""
 
     def request(self, flow: HTTPFlow) -> None:
@@ -129,9 +129,9 @@ def request(self, flow: HTTPFlow) -> None:
             if cache_path.exists():
                 try:
                     cached_data: dict[str, Any] = self.serializer.deserialize(cache_path)
-                    
+
                     cached_flow = HTTPFlow.from_state(cached_data)
-                    
+
                     if hasattr(cached_flow, ""response"") and cached_flow.response:
                         flow.response = cached_flow.response
                         logger.info(f""Serving {flow.request.url} from cache"")
@@ -158,7 +158,7 @@ def response(self, flow: HTTPFlow) -> None:
 
             try:
                 cache_path.parent.mkdir(parents=True, exist_ok=True)
-                
+
                 self.serializer.serialize(flow.get_state(), cache_path)
                 logger.info(f""Cached response for {flow.request.url}"")
             except Exception as e: