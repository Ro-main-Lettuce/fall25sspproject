@@ -245,43 +245,74 @@ def perform_action(self, action_name: str, kwargs) -> Any:
     
     def get_latest_casts(self, fid: int, cursor: Optional[int] = None, limit: Optional[int] = 25) -> IterableCastsResult:
         """"""Get the latest casts from a user""""""
-        logger.debug(f""Getting latest casts for {fid}, cursor: {cursor}, limit: {limit}"")
-
-        casts = self._client.get_casts(fid, cursor, limit)
-        logger.debug(f""Retrieved {len(casts)} casts"")
-        return casts
+        try:
+            logger.debug(f""Getting latest casts for {fid}, cursor: {cursor}, limit: {limit}"")
+            casts = self._client.get_casts(fid, cursor, limit)
+            logger.debug(f""Retrieved {len(casts)} casts"")
+            return casts
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to get latest casts: {e}"")
 
     def post_cast(self, text: str, embeds: Optional[List[str]] = None, channel_key: Optional[str] = None) -> CastContent:
         """"""Post a new cast""""""
-        logger.debug(f""Posting cast: {text}, embeds: {embeds}"")
-        return self._client.post_cast(text, embeds, None, channel_key)
-
+        try:
+            logger.debug(f""Posting cast: {text}, embeds: {embeds}"")
+            result = self._client.post_cast(text, embeds, None, channel_key)
+            logger.debug(""Cast posted successfully"")
+            return result
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to post cast: {e}"")
 
     def read_timeline(self, cursor: Optional[int] = None, limit: Optional[int] = 100) -> IterableCastsResult:
         """"""Read all recent casts""""""
-        logger.debug(f""Reading timeline, cursor: {cursor}, limit: {limit}"")
-        return self._client.get_recent_casts(cursor, limit)
+        try:
+            logger.debug(f""Reading timeline, cursor: {cursor}, limit: {limit}"")
+            casts = self._client.get_recent_casts(cursor, limit)
+            logger.debug(f""Retrieved {len(casts)} casts from timeline"")
+            return casts
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to read timeline: {e}"")
 
     def like_cast(self, cast_hash: str) -> ReactionsPutResult:
         """"""Like a specific cast""""""
-        logger.debug(f""Liking cast: {cast_hash}"")
-        return self._client.like_cast(cast_hash)
+        try:
+            logger.debug(f""Liking cast: {cast_hash}"")
+            result = self._client.like_cast(cast_hash)
+            logger.debug(""Cast liked successfully"")
+            return result
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to like cast: {e}"")
     
     def requote_cast(self, cast_hash: str) -> CastHash:
         """"""Requote a cast (recast)""""""
-        logger.debug(f""Requoting cast: {cast_hash}"")
-        return self._client.recast(cast_hash)
+        try:
+            logger.debug(f""Requoting cast: {cast_hash}"")
+            result = self._client.recast(cast_hash)
+            logger.debug(""Cast requoted successfully"")
+            return result
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to requote cast: {e}"")
 
     def reply_to_cast(self, parent_fid: int, parent_hash: str, text: str, embeds: Optional[List[str]] = None, channel_key: Optional[str] = None) -> CastContent:
         """"""Reply to an existing cast""""""
-        logger.debug(f""Replying to cast: {parent_hash}, text: {text}"")
-        parent = Parent(fid=parent_fid, hash=parent_hash)
-        return self._client.post_cast(text, embeds, parent, channel_key)
+        try:
+            logger.debug(f""Replying to cast: {parent_hash}, text: {text}"")
+            parent = Parent(fid=parent_fid, hash=parent_hash)
+            result = self._client.post_cast(text, embeds, parent, channel_key)
+            logger.debug(""Reply posted successfully"")
+            return result
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to reply to cast: {e}"")
     
     def get_cast_replies(self, thread_hash: str) -> IterableCastsResult:
         """"""Fetch cast replies (thread)""""""
-        logger.debug(f""Fetching replies for thread: {thread_hash}"")
-        return self._client.get_all_casts_in_thread(thread_hash)
+        try:
+            logger.debug(f""Fetching replies for thread: {thread_hash}"")
+            replies = self._client.get_all_casts_in_thread(thread_hash)
+            logger.debug(f""Retrieved {len(replies)} replies"")
+            return replies
+        except Exception as e:
+            raise FarcasterAPIError(f""Failed to get cast replies: {e}"")
 
     def __del__(self):
         """"""Ensure cleanup on deletion""""""