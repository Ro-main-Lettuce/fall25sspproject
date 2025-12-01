@@ -9,20 +9,24 @@
 import pickle
 from typing import Any, Optional, TypedDict, Union
 
-from azure.cosmos import CosmosClient, PartitionKey
-from azure.cosmos.exceptions import CosmosResourceNotFoundError
+from ..import_utils import optional_import_block, require_optional_import
+from .abstract_cache_base import AbstractCache
 
-from autogen.cache.abstract_cache_base import AbstractCache
+with optional_import_block():
+    from azure.cosmos import CosmosClient, PartitionKey
+    from azure.cosmos.exceptions import CosmosResourceNotFoundError
 
 
+@require_optional_import(""azure"", ""cosmosdb"")
 class CosmosDBConfig(TypedDict, total=False):
     connection_string: str
     database_id: str
     container_id: str
     cache_seed: Optional[Union[str, int]]
-    client: Optional[CosmosClient]
+    client: Optional[""CosmosClient""]
 
 
+@require_optional_import(""azure"", ""cosmosdb"")
 class CosmosDBCache(AbstractCache):
     """"""Synchronous implementation of AbstractCache using Azure Cosmos DB NoSQL API.
 
@@ -75,7 +79,7 @@ def from_connection_string(cls, seed: Union[str, int], connection_string: str, d
         return cls(str(seed), config)
 
     @classmethod
-    def from_existing_client(cls, seed: Union[str, int], client: CosmosClient, database_id: str, container_id: str):
+    def from_existing_client(cls, seed: Union[str, int], client: ""CosmosClient"", database_id: str, container_id: str):
         config = {""client"": client, ""database_id"": database_id, ""container_id"": container_id}
         return cls(str(seed), config)
 