@@ -4,13 +4,12 @@
 
 
 from dataclasses import dataclass
-from typing import Any, List, Mapping
+from typing import Any, Iterable, List, Mapping
 
 import pendulum
 import requests
 
 from airbyte_cdk.sources.declarative.extractors.record_extractor import RecordExtractor
-from airbyte_cdk.sources.declarative.types import Record
 
 
 @dataclass
@@ -19,10 +18,13 @@ class ZendeskChatBansRecordExtractor(RecordExtractor):
     Unnesting nested bans: `visitor`, `ip_address`.
     """"""
 
-    def extract_records(self, response: requests.Response) -> List[Mapping[str, Any]]:
+    def extract_records(
+        self,
+        response: requests.Response,
+    ) -> Iterable[Mapping[str, Any]]:
         response_data = response.json()
         ip_address: List[Mapping[str, Any]] = response_data.get(""ip_address"", [])
         visitor: List[Mapping[str, Any]] = response_data.get(""visitor"", [])
         bans = ip_address + visitor
         bans = sorted(bans, key=lambda x: pendulum.parse(x[""created_at""]) if x[""created_at""] else pendulum.datetime(1970, 1, 1))
-        return bans
+        yield from bans