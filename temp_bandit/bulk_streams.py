@@ -11,17 +11,20 @@
 from numpy import nan
 
 from airbyte_cdk.models import SyncMode
-from airbyte_cdk.sources.streams import IncrementalMixin
+from airbyte_cdk.sources.streams import CheckpointMixin
 from airbyte_cdk.sources.utils.transform import TransformConfig, TypeTransformer
 from source_bing_ads.base_streams import Accounts, BingAdsBaseStream
 from source_bing_ads.utils import transform_bulk_datetime_format_to_rfc_3339
 
 
-class BingAdsBulkStream(BingAdsBaseStream, IncrementalMixin, ABC):
+class BingAdsBulkStream(BingAdsBaseStream, CheckpointMixin, ABC):
     transformer: TypeTransformer = TypeTransformer(TransformConfig.DefaultSchemaNormalization | TransformConfig.CustomSchemaNormalization)
     cursor_field = ""Modified Time""
     primary_key = ""Id""
-    _state = {}
+
+    def __init__(self, *args, **kwargs):
+        super().__init__(*args, **kwargs)
+        self._state = {}
 
     @staticmethod
     @transformer.registerCustomTransform