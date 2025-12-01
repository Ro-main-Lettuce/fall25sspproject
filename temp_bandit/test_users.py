@@ -4,6 +4,7 @@
 
 from unittest import TestCase
 
+from airbyte_cdk.models import SyncMode
 from airbyte_cdk.test.entrypoint_wrapper import EntrypointOutput
 from airbyte_cdk.test.mock_http import HttpMocker
 from airbyte_cdk.test.mock_http.response_builder import (
@@ -14,7 +15,6 @@
     create_response_builder,
     find_template,
 )
-from airbyte_protocol.models import SyncMode
 
 from .config import BUSINESS_ACCOUNT_ID, ConfigBuilder
 from .request_builder import RequestBuilder, get_account_request