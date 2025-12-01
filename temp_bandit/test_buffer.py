@@ -4,12 +4,12 @@
 
 
 import io
+import logging
 from typing import Iterable
 
 import pytest
 from destination_google_sheets.buffer import WriteBufferMixin
 
-import logging
 from airbyte_cdk.models import AirbyteMessage, ConfiguredAirbyteCatalog, Type
 
 