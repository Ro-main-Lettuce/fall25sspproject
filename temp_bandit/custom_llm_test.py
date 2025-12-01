@@ -1,5 +1,4 @@
-from typing import Any, Dict, List, Optional, Union
-from unittest.mock import Mock
+from typing import Any
 
 import pytest
 
@@ -15,11 +14,12 @@ class CustomLLM(BaseLLM):
     that returns a predefined response for testing purposes.
     """"""
 
-    def __init__(self, response=""Default response"", model=""test-model""):
+    def __init__(self, response=""Default response"", model=""test-model"") -> None:
         """"""Initialize the CustomLLM with a predefined response.
 
         Args:
             response: The predefined response to return from call().
+
         """"""
         super().__init__(model=model)
         self.response = response
@@ -32,8 +32,7 @@ def call(
         callbacks=None,
         available_functions=None,
     ):
-        """"""
-        Mock LLM call that returns a predefined response.
+        """"""Mock LLM call that returns a predefined response.
         Properly formats messages to match OpenAI's expected structure.
         """"""
         self.call_count += 1
@@ -57,6 +56,7 @@ def supports_function_calling(self) -> bool:
 
         Returns:
             False, indicating that this LLM does not support function calling.
+
         """"""
         return False
 
@@ -65,6 +65,7 @@ def supports_stop_words(self) -> bool:
 
         Returns:
             False, indicating that this LLM does not support stop words.
+
         """"""
         return False
 
@@ -73,12 +74,13 @@ def get_context_window_size(self) -> int:
 
         Returns:
             4096, a typical context window size for modern LLMs.
+
         """"""
         return 4096
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_custom_llm_implementation():
+def test_custom_llm_implementation() -> None:
     """"""Test that a custom LLM implementation works with create_llm.""""""
     custom_llm = CustomLLM(response=""The answer is 42"")
 
@@ -89,15 +91,15 @@ def test_custom_llm_implementation():
 
     # Test calling the custom LLM
     response = result_llm.call(
-        ""What is the answer to life, the universe, and everything?""
+        ""What is the answer to life, the universe, and everything?"",
     )
 
     # Verify that the response from the custom LLM was used
     assert ""42"" in response
 
 
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_custom_llm_within_crew():
+def test_custom_llm_within_crew() -> None:
     """"""Test that a custom LLM implementation works with create_llm.""""""
     custom_llm = CustomLLM(response=""Hello! Nice to meet you!"", model=""test-model"")
 
@@ -128,8 +130,8 @@ def test_custom_llm_within_crew():
     assert ""Hello!"" in result.raw
 
 
-def test_custom_llm_message_formatting():
-    """"""Test that the custom LLM properly formats messages""""""
+def test_custom_llm_message_formatting() -> None:
+    """"""Test that the custom LLM properly formats messages.""""""
     custom_llm = CustomLLM(response=""Test response"", model=""test-model"")
 
     # Test with string input
@@ -148,29 +150,30 @@ def test_custom_llm_message_formatting():
 class JWTAuthLLM(BaseLLM):
     """"""Custom LLM implementation with JWT authentication.""""""
 
-    def __init__(self, jwt_token: str):
+    def __init__(self, jwt_token: str) -> None:
         super().__init__(model=""test-model"")
         if not jwt_token or not isinstance(jwt_token, str):
-            raise ValueError(""Invalid JWT token"")
+            msg = ""Invalid JWT token""
+            raise ValueError(msg)
         self.jwt_token = jwt_token
         self.calls = []
         self.stop = []
 
     def call(
         self,
-        messages: Union[str, List[Dict[str, str]]],
-        tools: Optional[List[dict]] = None,
-        callbacks: Optional[List[Any]] = None,
-        available_functions: Optional[Dict[str, Any]] = None,
-    ) -> Union[str, Any]:
+        messages: str | list[dict[str, str]],
+        tools: list[dict] | None = None,
+        callbacks: list[Any] | None = None,
+        available_functions: dict[str, Any] | None = None,
+    ) -> str | Any:
         """"""Record the call and return a predefined response.""""""
         self.calls.append(
             {
                 ""messages"": messages,
                 ""tools"": tools,
                 ""callbacks"": callbacks,
                 ""available_functions"": available_functions,
-            }
+            },
         )
         # In a real implementation, this would use the JWT token to authenticate
         # with an external service
@@ -189,7 +192,7 @@ def get_context_window_size(self) -> int:
         return 8192
 
 
-def test_custom_llm_with_jwt_auth():
+def test_custom_llm_with_jwt_auth() -> None:
     """"""Test a custom LLM implementation with JWT authentication.""""""
     jwt_llm = JWTAuthLLM(jwt_token=""example.jwt.token"")
 
@@ -207,7 +210,7 @@ def test_custom_llm_with_jwt_auth():
     assert response == ""Response from JWT-authenticated LLM""
 
 
-def test_jwt_auth_llm_validation():
+def test_jwt_auth_llm_validation() -> None:
     """"""Test that JWT token validation works correctly.""""""
     # Test with invalid JWT token (empty string)
     with pytest.raises(ValueError, match=""Invalid JWT token""):
@@ -221,12 +224,13 @@ def test_jwt_auth_llm_validation():
 class TimeoutHandlingLLM(BaseLLM):
     """"""Custom LLM implementation with timeout handling and retry logic.""""""
 
-    def __init__(self, max_retries: int = 3, timeout: int = 30):
+    def __init__(self, max_retries: int = 3, timeout: int = 30) -> None:
         """"""Initialize the TimeoutHandlingLLM with retry and timeout settings.
 
         Args:
             max_retries: Maximum number of retry attempts.
             timeout: Timeout in seconds for each API call.
+
         """"""
         super().__init__(model=""test-model"")
         self.max_retries = max_retries
@@ -237,11 +241,11 @@ def __init__(self, max_retries: int = 3, timeout: int = 30):
 
     def call(
         self,
-        messages: Union[str, List[Dict[str, str]]],
-        tools: Optional[List[dict]] = None,
-        callbacks: Optional[List[Any]] = None,
-        available_functions: Optional[Dict[str, Any]] = None,
-    ) -> Union[str, Any]:
+        messages: str | list[dict[str, str]],
+        tools: list[dict] | None = None,
+        callbacks: list[Any] | None = None,
+        available_functions: dict[str, Any] | None = None,
+    ) -> str | Any:
         """"""Simulate API calls with timeout handling and retry logic.
 
         Args:
@@ -255,6 +259,7 @@ def call(
 
         Raises:
             TimeoutError: If all retry attempts fail.
+
         """"""
         # Record the initial call
         self.calls.append(
@@ -264,7 +269,7 @@ def call(
                 ""callbacks"": callbacks,
                 ""available_functions"": available_functions,
                 ""attempt"": 0,
-            }
+            },
         )
 
         # Simulate retry logic
@@ -276,46 +281,47 @@ def call(
                     self.fail_count -= 1
                     # If we've used all retries, raise an error
                     if attempt == self.max_retries - 1:
+                        msg = f""LLM request failed after {self.max_retries} attempts""
                         raise TimeoutError(
-                            f""LLM request failed after {self.max_retries} attempts""
-                        )
-                    # Otherwise, continue to the next attempt (simulating backoff)
-                    continue
-                else:
-                    # Success on first attempt
-                    return ""First attempt response""
-            else:
-                # This is a retry attempt (attempt > 0)
-                # Always record retry attempts
-                self.calls.append(
-                    {
-                        ""retry_attempt"": attempt,
-                        ""messages"": messages,
-                        ""tools"": tools,
-                        ""callbacks"": callbacks,
-                        ""available_functions"": available_functions,
-                    }
-                )
-
-                # Simulate a failure if fail_count > 0
-                if self.fail_count > 0:
-                    self.fail_count -= 1
-                    # If we've used all retries, raise an error
-                    if attempt == self.max_retries - 1:
-                        raise TimeoutError(
-                            f""LLM request failed after {self.max_retries} attempts""
+                            msg,
                         )
                     # Otherwise, continue to the next attempt (simulating backoff)
                     continue
-                else:
-                    # Success on retry
-                    return ""Response after retry""
+                # Success on first attempt
+                return ""First attempt response""
+            # This is a retry attempt (attempt > 0)
+            # Always record retry attempts
+            self.calls.append(
+                {
+                    ""retry_attempt"": attempt,
+                    ""messages"": messages,
+                    ""tools"": tools,
+                    ""callbacks"": callbacks,
+                    ""available_functions"": available_functions,
+                },
+            )
+
+            # Simulate a failure if fail_count > 0
+            if self.fail_count > 0:
+                self.fail_count -= 1
+                # If we've used all retries, raise an error
+                if attempt == self.max_retries - 1:
+                    msg = f""LLM request failed after {self.max_retries} attempts""
+                    raise TimeoutError(
+                        msg,
+                    )
+                # Otherwise, continue to the next attempt (simulating backoff)
+                continue
+            # Success on retry
+            return ""Response after retry""
+        return None
 
     def supports_function_calling(self) -> bool:
         """"""Return True to indicate that function calling is supported.
 
         Returns:
             True, indicating that this LLM supports function calling.
+
         """"""
         return True
 
@@ -324,6 +330,7 @@ def supports_stop_words(self) -> bool:
 
         Returns:
             True, indicating that this LLM supports stop words.
+
         """"""
         return True
 
@@ -332,11 +339,12 @@ def get_context_window_size(self) -> int:
 
         Returns:
             8192, a typical context window size for modern LLMs.
+
         """"""
         return 8192
 
 
-def test_timeout_handling_llm():
+def test_timeout_handling_llm() -> None:
     """"""Test a custom LLM implementation with timeout handling and retry logic.""""""
     # Test successful first attempt
     llm = TimeoutHandlingLLM()