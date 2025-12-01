@@ -5,6 +5,7 @@
 import json
 from unittest import TestCase
 
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput
 from airbyte_cdk.test.mock_http import HttpMocker, HttpResponse
 from airbyte_cdk.test.mock_http.response_builder import (
@@ -15,7 +16,6 @@
     create_response_builder,
     find_template,
 )
-from airbyte_protocol.models import SyncMode
 
 from .config import BUSINESS_ACCOUNT_ID, ConfigBuilder
 from .pagination import NEXT_PAGE_TOKEN, InstagramPaginationStrategy