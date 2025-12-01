@@ -7,10 +7,10 @@
 from collections.abc import Hashable
 from typing import Any, Optional
 
-from autogen import token_count_utils
-from autogen.cache.abstract_cache_base import AbstractCache
-from autogen.oai.openai_utils import filter_config
-from autogen.types import MessageContentType
+from .... import token_count_utils
+from ....cache.abstract_cache_base import AbstractCache
+from ....oai.openai_utils import filter_config
+from ....types import MessageContentType
 
 
 def cache_key(content: MessageContentType, *args: Hashable) -> str: