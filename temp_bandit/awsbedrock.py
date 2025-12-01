@@ -24,7 +24,7 @@
 
 from llm_gateway.constants import get_settings
 from llm_gateway.db.models import AWSBedrockRequests
-from llm_gateway.db.utils import write_record_to_db
+from llm_gateway.db.utils import get_session
 from llm_gateway.exceptions import AWSBEDROCK_EXCEPTIONS
 from llm_gateway.pii_scrubber import scrub_all
 from llm_gateway.utils import max_retries
@@ -309,7 +309,9 @@ def send_awsbedrock_request(
 
         return awsbedrock_response, db_record
 
-    def write_logs_to_db(self, db_logs: dict):
+    async def write_logs_to_db(self, db_logs: dict):
         if isinstance(db_logs[""awsbedrock_response""], list):
             db_logs[""awsbedrock_response""] = """".join(db_logs[""awsbedrock_response""])
-        write_record_to_db(AWSBedrockRequests(**db_logs))
+        async with get_session() as session:
+            session.add(AWSBedrockRequests(**db_logs))
+            await session.commit()