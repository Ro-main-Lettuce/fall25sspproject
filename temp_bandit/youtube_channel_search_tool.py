@@ -31,6 +31,7 @@ class YoutubeChannelSearchTool(RagTool):
     def __init__(self, youtube_channel_handle: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if youtube_channel_handle is not None:
+            kwargs[""data_type""] = DataType.YOUTUBE_CHANNEL
             self.add(youtube_channel_handle)
             self.description = f""A tool that can be used to semantic search a query the {youtube_channel_handle} Youtube Channels content.""
             self.args_schema = FixedYoutubeChannelSearchToolSchema
@@ -43,8 +44,6 @@ def add(
     ) -> None:
         if not youtube_channel_handle.startswith(""@""):
             youtube_channel_handle = f""@{youtube_channel_handle}""
-
-        kwargs[""data_type""] = DataType.YOUTUBE_CHANNEL
         super().add(youtube_channel_handle, **kwargs)
 
     def _before_run(