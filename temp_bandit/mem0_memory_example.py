@@ -14,6 +14,7 @@
 
 By using async operations, you can perform multiple memory operations simultaneously instead of waiting for each one to complete sequentially. This is particularly beneficial when dealing with multiple memory additions or searches.
 """"""
+
 import os
 import asyncio
 from dotenv import load_dotenv
@@ -82,7 +83,7 @@ def demonstrate_sync_memory(local_config, sample_messages, sample_preferences, u
 
             if results and ""results"" in results:
                 for j, result in enumerate(results[""results""][:2]):  # Show top 2
-                    print(f""Result {j+1}: {result.get('memory', 'N/A')}"")
+                    print(f""Result {j + 1}: {result.get('memory', 'N/A')}"")
             else:
                 print(""No results found"")
 
@@ -143,7 +144,7 @@ async def add_preference(preference, index):
         tasks = [add_preference(pref, i) for i, pref in enumerate(sample_preferences)]
         results = await asyncio.gather(*tasks)
         for i, result in enumerate(results):
-            print(f""Added async preference {i+1}: {result}"")
+            print(f""Added async preference {i + 1}: {result}"")
 
         # 2. SEARCH operations - perform multiple searches concurrently
         search_queries = [
@@ -163,7 +164,7 @@ async def search_memory(query):
         for result, query in search_results:
             if result and ""results"" in result:
                 for j, res in enumerate(result[""results""][:2]):
-                    print(f""Result {j+1}: {res.get('memory', 'N/A')}"")
+                    print(f""Result {j + 1}: {res.get('memory', 'N/A')}"")
             else:
                 print(""No results found"")
 