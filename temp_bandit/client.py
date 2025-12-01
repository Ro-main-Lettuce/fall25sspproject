@@ -3,15 +3,14 @@
 #
 
 
+import logging
 from typing import Any, Dict
 
 import pygsheets
 from google.auth.transport.requests import Request
 from google.oauth2 import credentials as client_account
 from pygsheets.client import Client as pygsheets_client
 
-import logging
-
 
 # the list of required scopes/permissions
 # more info: https://developers.google.com/sheets/api/guides/authorizing#OAuth2Authorizing