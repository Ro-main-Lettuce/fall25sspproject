@@ -6,7 +6,6 @@
 
 import sys
 import traceback
-from typing import Any
 
 def test_function_tool():
     """"""Test 1: Function Tool with @tool decorator""""""
@@ -20,13 +19,14 @@ def fetch_logs(query: str) -> str:
             """"""Fetch logs from New Relic based on query""""""
             return f""Logs for query: {query}""
         
-        teacher = Agent(
+        agent = Agent(
             role='CrashFetcher',
             goal='Extract logs',
             backstory='An agent that fetches logs',
             tools=[fetch_logs],
             allow_delegation=False
         )
+        assert len(agent.tools) == 1, f""Expected 1 tool, got {len(agent.tools)}""
         print(""✅ Function tool with @tool decorator: SUCCESS"")
         return True
     except Exception as e:
@@ -49,13 +49,14 @@ def fetch_logs_func(query: str) -> str:
             'func': fetch_logs_func
         }
         
-        teacher = Agent(
+        agent = Agent(
             role='CrashFetcher',
             goal='Extract logs',
             backstory='An agent that fetches logs',
             tools=[fetch_logs_dict],
             allow_delegation=False
         )
+        assert len(agent.tools) == 1, f""Expected 1 tool, got {len(agent.tools)}""
         print(""✅ Dict-based tool: SUCCESS"")
         return True
     except Exception as e:
@@ -77,13 +78,14 @@ class FetchLogsTool(BaseTool):
             def _run(self, query: str) -> str:
                 return f""Logs for query: {query}""
         
-        teacher = Agent(
+        agent = Agent(
             role='CrashFetcher',
             goal='Extract logs',
             backstory='An agent that fetches logs',
             tools=[FetchLogsTool()],
             allow_delegation=False
         )
+        assert len(agent.tools) == 1, f""Expected 1 tool, got {len(agent.tools)}""
         print(""✅ BaseTool class inheritance: SUCCESS"")
         return True
     except Exception as e:
@@ -101,13 +103,14 @@ def fetch_logs(query: str) -> str:
             """"""Fetch logs from New Relic based on query""""""
             return f""Logs for query: {query}""
         
-        teacher = Agent(
+        agent = Agent(
             role='CrashFetcher',
             goal='Extract logs',
             backstory='An agent that fetches logs',
             tools=[fetch_logs],
             allow_delegation=False
         )
+        assert len(agent.tools) == 1, f""Expected 1 tool, got {len(agent.tools)}""
         print(""✅ Direct function assignment: SUCCESS"")
         return True
     except Exception as e:
@@ -125,7 +128,7 @@ def main():
     results.append(test_basetool_class())
     results.append(test_direct_function())
     
-    print(f""
=== SUMMARY ==="")
+    print(""
=== SUMMARY ==="")
     passed = sum(results)
     total = len(results)
     print(f""Tests passed: {passed}/{total}"")