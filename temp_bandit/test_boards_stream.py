@@ -1,8 +1,8 @@
 # Copyright (c) 2023 Airbyte, Inc., all rights reserved.
 from unittest import TestCase
 
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.test.mock_http import HttpMocker
-from airbyte_protocol.models import SyncMode
 
 from .config import ConfigBuilder
 from .monday_requests import BoardsRequestBuilder