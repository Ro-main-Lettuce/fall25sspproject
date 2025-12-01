@@ -189,7 +189,7 @@ def print(self, f: Optional[Callable[..., Any]] = None) -> None:
 
 @wrap_message
 class TextMessage(BasePrintReceivedMessage):
-    content: Optional[Union[str, int, float, bool, list[dict[str, str]]]] = None  # type: ignore [assignment]
+    content: Optional[Union[str, int, float, bool, list[dict[str, Union[str, dict[str, Any]]]]]] = None  # type: ignore [assignment]
 
     def print(self, f: Optional[Callable[..., Any]] = None) -> None:
         f = f or print