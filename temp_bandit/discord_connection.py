@@ -347,11 +347,13 @@ def list_channels(self, server_id: str, **kwargs) -> dict:
 
     def read_messages(self, channel_id: str, count: int, **kwargs) -> dict:
         """"""Reading messages in a channel""""""
-        logger.debug(""Sending a new message"")
+        logger.debug(""Reading messages"")
+        after = kwargs.get('after')
         request_path = f""/channels/{channel_id}/messages?limit={count}""
+        if after:
+            request_path += f""&after={after}""
         response = self._get_request(request_path)
         formatted_response = self._format_messages(response)
-
         logger.info(f""Retrieved {len(formatted_response)} messages"")
         return formatted_response
 