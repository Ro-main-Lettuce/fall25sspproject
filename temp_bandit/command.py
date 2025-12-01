@@ -10,13 +10,13 @@
 
 
 class BaseCommand:
-    def __init__(self):
+    def __init__(self) -> None:
         self._telemetry = Telemetry()
         self._telemetry.set_tracer()
 
 
 class PlusAPIMixin:
-    def __init__(self, telemetry):
+    def __init__(self, telemetry) -> None:
         try:
             telemetry.set_tracer()
             self.plus_api_client = PlusAPI(api_key=get_auth_token())
@@ -30,11 +30,11 @@ def __init__(self, telemetry):
             raise SystemExit
 
     def _validate_response(self, response: requests.Response) -> None:
-        """"""
-        Handle and display error messages from API responses.
+        """"""Handle and display error messages from API responses.
 
         Args:
             response (requests.Response): The response from the Plus API
+
         """"""
         try:
             json_response = response.json()
@@ -55,13 +55,13 @@ def _validate_response(self, response: requests.Response) -> None:
             for field, messages in json_response.items():
                 for message in messages:
                     console.print(
-                        f""* [bold red]{field.capitalize()}[/bold red] {message}""
+                        f""* [bold red]{field.capitalize()}[/bold red] {message}"",
                     )
             raise SystemExit
 
         if not response.ok:
             console.print(
-                ""Request to Enterprise API failed. Details:"", style=""bold red""
+                ""Request to Enterprise API failed. Details:"", style=""bold red"",
             )
             details = (
                 json_response.get(""error"")