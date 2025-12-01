@@ -2,11 +2,11 @@
 # Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 #
 
+import logging
 from typing import Any, Dict, Iterable, Mapping
 
 from google.auth.exceptions import RefreshError
 
-import logging
 from airbyte_cdk.destinations import Destination
 from airbyte_cdk.models import AirbyteConnectionStatus, AirbyteMessage, ConfiguredAirbyteCatalog, DestinationSyncMode, Status, Type
 