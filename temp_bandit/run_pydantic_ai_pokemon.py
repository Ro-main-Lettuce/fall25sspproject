@@ -89,12 +89,12 @@ async def main() -> None:
         async with agent.run_mcp_servers():
             print(""✅ MCP server connection established"")
             print(""🚀 Running PydanticAI agent...
"")
-            
+
             result = await agent.run(user_prompt)
-            
+
             print(""🎉 Agent execution completed!"")
             print(f""📝 Final response:
{result.data}
"")
-            
+
             print(""🔍 Verifying sync results..."")
             verify_result = await agent.run(
                 ""Please check what Pokemon data was successfully synced to our cache. ""
@@ -105,6 +105,7 @@ async def main() -> None:
     except Exception as e:
         print(f""❌ Error during agent execution: {e}"")
         import traceback
+
         traceback.print_exc()
         sys.exit(1)
 