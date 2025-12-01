@@ -7,6 +7,7 @@
 
 import pytest
 
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput
 from airbyte_cdk.test.mock_http import HttpMocker, HttpResponse
 from airbyte_cdk.test.mock_http.response_builder import (
@@ -17,7 +18,6 @@
     create_response_builder,
     find_template,
 )
-from airbyte_protocol.models import SyncMode
 
 from .config import BUSINESS_ACCOUNT_ID, ConfigBuilder
 from .pagination import NEXT_PAGE_TOKEN, InstagramPaginationStrategy