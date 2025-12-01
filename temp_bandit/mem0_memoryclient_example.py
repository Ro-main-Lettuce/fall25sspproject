@@ -14,6 +14,7 @@
 
 By using the cloud-based MemoryClient with async operations, you can leverage Mem0's managed infrastructure while performing multiple memory operations simultaneously. This is ideal for production applications that need scalable memory management without managing local storage.
 """"""
+
 import os
 import asyncio
 from dotenv import load_dotenv
@@ -124,7 +125,7 @@ async def demonstrate_async_memory_client(sample_messages, sample_preferences, u
         # Execute all add operations concurrently
         results = await asyncio.gather(add_conversation_task, *add_preference_tasks)
         for i, result in enumerate(results):
-            print(f""{i+1}. {result}"")
+            print(f""{i + 1}. {result}"")
 
         # 2. Concurrent SEARCH operations - multiple cloud searches in parallel
         search_tasks = [
@@ -136,7 +137,7 @@ async def demonstrate_async_memory_client(sample_messages, sample_preferences, u
         # Execute all searches concurrently
         search_results = await asyncio.gather(*search_tasks)
         for i, result in enumerate(search_results):
-            print(f""Search {i+1} result: {result}"")
+            print(f""Search {i + 1} result: {result}"")
 
         # 3. GET_ALL operation - retrieve filtered memories from cloud
         filters = {""AND"": [{""user_id"": user_id}]}