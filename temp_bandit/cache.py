@@ -6,18 +6,12 @@
 # SPDX-License-Identifier: MIT
 from __future__ import annotations
 
-import sys
 from types import TracebackType
 from typing import Any
 
 from .abstract_cache_base import AbstractCache
 from .cache_factory import CacheFactory
 
-if sys.version_info >= (3, 11):
-    pass
-else:
-    pass
-
 
 class Cache(AbstractCache):
     """"""A wrapper class for managing cache configuration and instances.