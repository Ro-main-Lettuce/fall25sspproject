@@ -42,25 +42,3 @@ class TwitterCard(BaseModel):
     """"""A Twitter card containing tweet information and any quoted tweets.""""""
     tweet: Tweet = Field(..., description=""The main tweet content and metadata."")
     quoted_tweet: Tweet | None = Field(default=None, description=""A tweet that is quoted by the main tweet, if any."")
-
-    class Config:
-        """"""Configuration for the TwitterCard model.""""""
-        schema_extra = {
-            ""example"": {
-                ""tweet"": {
-                    ""content"": ""Introducing GPT-4 Turbo with vision"",
-                    ""created_at"": ""2023-11-06T18:00:00Z"",
-                    ""user"": {
-                        ""username"": ""OpenAI"",
-                        ""display_name"": ""OpenAI""
-                    },
-                    ""media"": ""Image of GPT-4 Turbo announcement"",
-                    ""retweet_count"": 5421,
-                    ""like_count"": 28900,
-                    ""reply_count"": 1234,
-                    ""view_count"": ""2.1M"",
-                    ""quote_count"": 892
-                },
-                ""quoted_tweet"": None
-            }
-        }