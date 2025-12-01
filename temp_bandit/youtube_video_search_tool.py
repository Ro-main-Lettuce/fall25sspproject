@@ -31,6 +31,7 @@ class YoutubeVideoSearchTool(RagTool):
     def __init__(self, youtube_video_url: Optional[str] = None, **kwargs):
         super().__init__(**kwargs)
         if youtube_video_url is not None:
+            kwargs[""data_type""] = DataType.YOUTUBE_VIDEO
             self.add(youtube_video_url)
             self.description = f""A tool that can be used to semantic search a query the {youtube_video_url} Youtube Video content.""
             self.args_schema = FixedYoutubeVideoSearchToolSchema
@@ -41,7 +42,6 @@ def add(
         *args: Any,
         **kwargs: Any,
     ) -> None:
-        kwargs[""data_type""] = DataType.YOUTUBE_VIDEO
         super().add(*args, **kwargs)
 
     def _before_run(