@@ -3,13 +3,13 @@
 #
 
 
+import logging
 import re
 from typing import List
 
 from pygsheets import Spreadsheet, Worksheet
 from pygsheets.exceptions import WorksheetNotFound
 
-import logging
 from airbyte_cdk.models import ConfiguredAirbyteCatalog
 
 