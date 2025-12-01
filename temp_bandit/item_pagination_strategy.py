@@ -4,7 +4,10 @@
 
 from typing import Any, List, Mapping, Optional, Tuple
 
+import requests
+
 from airbyte_cdk.sources.declarative.requesters.paginators.strategies.page_increment import PageIncrement
+from airbyte_cdk.sources.types import Record
 
 
 #
@@ -32,15 +35,17 @@ def __post_init__(self, parameters: Mapping[str, Any]):
         self._page: Optional[int] = self.start_from_page
         self._sub_page: Optional[int] = self.start_from_page
 
-    def next_page_token(self, response, last_records: List[Mapping[str, Any]]) -> Optional[Tuple[Optional[int], Optional[int]]]:
+    def next_page_token(
+        self, response: requests.Response, last_page_size: int, last_record: Optional[Record], last_page_token_value: Optional[Any]
+    ) -> Optional[Tuple[Optional[int], Optional[int]]]:
         """"""
         Determines page and subpage numbers for the `items` stream
 
         Attributes:
             response: Contains `boards` and corresponding lists of `items` for each `board`
             last_records: Parsed `items` from the response
         """"""
-        if len(last_records) >= self.page_size:
+        if last_page_size >= self.page_size:
             self._sub_page += 1
         else:
             self._sub_page = self.start_from_page
@@ -72,7 +77,9 @@ def __post_init__(self, parameters: Mapping[str, Any]):
         self._page: Optional[int] = self.start_from_page
         self._sub_page: Optional[int] = self.start_from_page
 
-    def next_page_token(self, response, last_records: List[Mapping[str, Any]]) -> Optional[Tuple[Optional[int], Optional[int]]]:
+    def next_page_token(
+        self, response: requests.Response, last_page_size: int, last_record: Optional[Record], last_page_token_value: Optional[Any]
+    ) -> Optional[Tuple[Optional[int], Optional[int]]]:
         """"""
         `items` stream use a separate 2 level pagination strategy where:
         1st level `boards` - incremental pagination