@@ -21,8 +21,8 @@ def __init__(self, name: str, **kwargs):
             ""config_list"": [{""model"": ""gpt-4"", ""api_key"": ""fake-key""}]
         }
         class MockConfig(BaseCommsPlatformConfig):
-            timeout_minutes: int = Field(default=1, gt=0)
-            max_reply_messages: int = Field(default=1, gt=0)
+            timeout_minutes: int = 1
+            max_reply_messages: int = 1
 
             def validate_config(self) -> bool:
                 return True