@@ -9,16 +9,19 @@
 from types import TracebackType
 from typing import Any, Optional, Union
 
-import redis
-
-from .abstract_cache_base import AbstractCache
-
 if sys.version_info >= (3, 11):
     from typing import Self
 else:
     from typing_extensions import Self
 
+from ..import_utils import optional_import_block, require_optional_import
+from .abstract_cache_base import AbstractCache
+
+with optional_import_block():
+    import redis
+
 
+@require_optional_import(""redis"", ""redis"")
 class RedisCache(AbstractCache):
     """"""Implementation of AbstractCache using the Redis database.
 