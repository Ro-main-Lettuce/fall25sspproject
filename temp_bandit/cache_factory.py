@@ -8,6 +8,7 @@
 import os
 from typing import Any, Optional, Union
 
+from ..import_utils import optional_import_block
 from .abstract_cache_base import AbstractCache
 from .disk_cache import DiskCache
 
@@ -63,22 +64,23 @@ def cache_factory(
 
         """"""
         if redis_url:
-            try:
+            with optional_import_block() as result:
                 from .redis_cache import RedisCache
 
+            if result.is_successful:
                 return RedisCache(seed, redis_url)
-            except ImportError:
+            else:
                 logging.warning(
                     ""RedisCache is not available. Checking other cache options. The last fallback is DiskCache.""
                 )
 
         if cosmosdb_config:
-            try:
+            with optional_import_block() as result:
                 from .cosmos_db_cache import CosmosDBCache
 
+            if result.is_successful:
                 return CosmosDBCache.create_cache(seed, cosmosdb_config)
-
-            except ImportError:
+            else:
                 logging.warning(""CosmosDBCache is not available. Fallback to DiskCache."")
 
         # Default to DiskCache if neither Redis nor Cosmos DB configurations are provided