@@ -40,12 +40,8 @@ def main(args):
         help=""Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)"",
     )
     parser.add_argument(""--model"", type=str, help=""Model to use"", default=""gemini/gemini-1.5-flash"")
-    parser.add_argument(
-        ""--max-requests-per-minute"", type=int, help=""Max requests per minute"", default=None
-    )
-    parser.add_argument(
-        ""--max-tokens-per-minute"", type=int, help=""Max tokens per minute"", default=None
-    )
+    parser.add_argument(""--max-requests-per-minute"", type=int, help=""Max requests per minute"", default=None)
+    parser.add_argument(""--max-tokens-per-minute"", type=int, help=""Max tokens per minute"", default=None)
     parser.add_argument(""--max-retries"", type=int, help=""Max retries"", default=None)
     parser.add_argument(
         ""--partial-responses"",