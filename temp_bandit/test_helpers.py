@@ -4,6 +4,7 @@
 
 
 import json
+import os
 from typing import Any, Mapping
 
 from destination_google_sheets.client import GoogleSheetsClient
@@ -25,8 +26,15 @@ def get_config(config_path: str = ""secrets/config_oauth.json"") -> Mapping[str, A
         return json.loads(f.read())
 
 
+def get_service_config(config_path: str = ""secrets/config_service.json"") -> Mapping[str, Any]:
+    with open(config_path, ""r"") as f:
+        return json.loads(f.read())
+
+
 # using real config from secrets/config_oauth.json
 TEST_CONFIG: dict = get_config()
+TEST_SERVICE_CONFIG = get_service_config()
+
 # client instance
 TEST_CLIENT: pygsheets_client = GoogleSheetsClient(TEST_CONFIG).authorize()
 # get test spreadsheet_id
@@ -39,8 +47,6 @@ def get_config(config_path: str = ""secrets/config_oauth.json"") -> Mapping[str, A
 TEST_CATALOG_PATH: str = ""integration_tests/configured_catalog.json""
 # reading prepared catalog with streams
 TEST_CATALOG: ConfiguredAirbyteCatalog = ConfiguredAirbyteCatalog.parse_file(TEST_CATALOG_PATH)
-
-
 # ----- BEGIN TESTS -----
 
 