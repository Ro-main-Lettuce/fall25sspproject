@@ -3,6 +3,7 @@
 #
 
 
+import logging
 import sys
 from io import StringIO
 
@@ -12,7 +13,6 @@
 from integration_tests.test_helpers import TEST_CONFIG
 from integration_tests.test_writer import TEST_CATALOG, TEST_SPREADSHEET, TEST_STREAM
 
-import logging
 from airbyte_cdk.models import AirbyteConnectionStatus, Status
 
 