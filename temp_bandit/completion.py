@@ -20,30 +20,40 @@
 null_handler = logging.NullHandler()
 flaml_logger.addHandler(null_handler)
 
-from flaml import BlendSearch, tune
-from flaml.tune.space import is_constant
+from ..import_utils import optional_import_block, require_optional_import
+
+with optional_import_block() as result:
+    from flaml import BlendSearch, tune
+    from flaml.tune.space import is_constant
+
+FLAML_INSTALLED = result.is_successful
 
 # Restore logging by removing the NullHandler
 flaml_logger.removeHandler(null_handler)
 
+from ..import_utils import optional_import_block
 from .client_utils import logging_formatter
 from .openai_utils import get_key
 
 try:
-    import diskcache
-    import openai
-    from openai import (
-        APIConnectionError,
-        APIError,
-        AuthenticationError,
-        BadRequestError,
-        RateLimitError,
-        Timeout,
-    )
-    from openai import Completion as OpenAICompletion
+    with optional_import_block() as result:
+        import diskcache
+        import openai
+        from openai import (
+            APIConnectionError,
+            APIError,
+            AuthenticationError,
+            BadRequestError,
+            RateLimitError,
+            Timeout,
+        )
+        from openai import Completion as OpenAICompletion
 
-    ERROR = None
-    assert openai.__version__ < ""1""
+    if result.is_successful:
+        ERROR = None
+        assert openai.__version__ < ""1""
+    else:
+        raise ImportError(""openai<1 is required."")
 except (AssertionError, ImportError):
     OpenAICompletion = object
     # The autogen.Completion class requires openai<1
@@ -106,26 +116,30 @@ class Completion(OpenAICompletion):
         ""gpt-4-32k-0613"": (0.06, 0.12),
     }
 
-    default_search_space = {
-        ""model"": tune.choice(
-            [
-                ""text-ada-001"",
-                ""text-babbage-001"",
-                ""text-davinci-003"",
-                ""gpt-3.5-turbo"",
-                ""gpt-4"",
-            ]
-        ),
-        ""temperature_or_top_p"": tune.choice(
-            [
-                {""temperature"": tune.uniform(0, 2)},
-                {""top_p"": tune.uniform(0, 1)},
-            ]
-        ),
-        ""max_tokens"": tune.lograndint(50, 1000),
-        ""n"": tune.randint(1, 100),
-        ""prompt"": ""{prompt}"",
-    }
+    default_search_space = (
+        {
+            ""model"": tune.choice(
+                [
+                    ""text-ada-001"",
+                    ""text-babbage-001"",
+                    ""text-davinci-003"",
+                    ""gpt-3.5-turbo"",
+                    ""gpt-4"",
+                ]
+            ),
+            ""temperature_or_top_p"": tune.choice(
+                [
+                    {""temperature"": tune.uniform(0, 2)},
+                    {""top_p"": tune.uniform(0, 1)},
+                ]
+            ),
+            ""max_tokens"": tune.lograndint(50, 1000),
+            ""n"": tune.randint(1, 100),
+            ""prompt"": ""{prompt}"",
+        }
+        if FLAML_INSTALLED
+        else {}
+    )
 
     cache_seed = 41
     cache_path = f"".cache/{cache_seed}""
@@ -520,6 +534,7 @@ def _eval(cls, config: dict, prune=True, eval_only=False):
         return result
 
     @classmethod
+    @require_optional_import(""flaml"", ""flaml"")
     def tune(
         cls,
         data: list[dict],
@@ -745,40 +760,40 @@ def create(
                 Only the differences from the default config need to be provided.
                 E.g.,
 
-        ```python
-        response = oai.Completion.create(
-            config_list=[
-                {
-                    ""model"": ""gpt-4"",
-                    ""api_key"": os.environ.get(""AZURE_OPENAI_API_KEY""),
-                    ""api_type"": ""azure"",
-                    ""base_url"": os.environ.get(""AZURE_OPENAI_API_BASE""),
-                    ""api_version"": ""2024-02-01"",
-                },
-                {
-                    ""model"": ""gpt-3.5-turbo"",
-                    ""api_key"": os.environ.get(""OPENAI_API_KEY""),
-                    ""api_type"": ""openai"",
-                    ""base_url"": ""https://api.openai.com/v1"",
-                },
-                {
-                    ""model"": ""llama-7B"",
-                    ""base_url"": ""http://127.0.0.1:8080"",
-                    ""api_type"": ""openai"",
-                },
-            ],
-            prompt=""Hi"",
-        )
-        ```
+                ```python
+                    response = oai.Completion.create(
+                        config_list = [
+                            {
+                                ""model"": ""gpt-4"",
+                                ""api_key"": os.environ.get(""AZURE_OPENAI_API_KEY""),
+                                ""api_type"": ""azure"",
+                                ""base_url"": os.environ.get(""AZURE_OPENAI_API_BASE""),
+                                ""api_version"": ""2024-02-01"",
+                            },
+                            {
+                                ""model"": ""gpt-3.5-turbo"",
+                                ""api_key"": os.environ.get(""OPENAI_API_KEY""),
+                                ""api_type"": ""openai"",
+                                ""base_url"": ""https://api.openai.com/v1"",
+                            },
+                            {
+                                ""model"": ""llama-7B"",
+                                ""base_url"": ""http://127.0.0.1:8080"",
+                                ""api_type"": ""openai"",
+                            },
+                        ],
+                        prompt=""Hi"",
+                    )
+                ```
 
             filter_func (Callable, Optional): A function that takes in the context and the response and returns a boolean to indicate whether the response is valid. E.g.,
 
-        ```python
-        def yes_or_no_filter(context, config, response):
-            return context.get(""yes_or_no_choice"", False) is False or any(
-                text in [""Yes."", ""No.""] for text in oai.Completion.extract_text(response)
-            )
-        ```
+                ```python
+                    def yes_or_no_filter(context, config, response):
+                        return context.get(""yes_or_no_choice"", False) is False or any(
+                            text in [""Yes."", ""No.""] for text in oai.Completion.extract_text(response)
+                        )
+                ```
 
             raise_on_ratelimit_or_timeout (bool, Optional): Whether to raise RateLimitError or Timeout when all configs fail.
                 When set to False, -1 will be returned when all configs fail.
@@ -1208,5 +1223,5 @@ class ChatCompletion(Completion):
     """"""`(openai<1)` A class for OpenAI API ChatCompletion. Share the same API as Completion.""""""
 
     default_search_space = Completion.default_search_space.copy()
-    default_search_space[""model""] = tune.choice([""gpt-3.5-turbo"", ""gpt-4""])
+    default_search_space[""model""] = tune.choice([""gpt-3.5-turbo"", ""gpt-4""]) if FLAML_INSTALLED else {}
     openai_completion_class = not ERROR and openai.ChatCompletion