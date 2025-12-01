@@ -22,15 +22,15 @@
 async def test_message_endpoint(
     server_url: str,
     messages: List[str],
-    chatbot_id: Optional[str] = None,
+    application_id: Optional[str] = None,
     trace_id: Optional[str] = None,
     agent_state: Optional[Dict[str, Any]] = None,
     settings: Optional[Dict[str, Any]] = None,
     verbose: bool = False,
 ):
     """"""Test the SSE /message endpoint.""""""
-    if not chatbot_id:
-        chatbot_id = f""test-bot-{uuid.uuid4().hex[:8]}""
+    if not application_id:
+        application_id = f""test-bot-{uuid.uuid4().hex[:8]}""
     
     if not trace_id:
         trace_id = uuid.uuid4().hex
@@ -42,7 +42,7 @@ async def test_message_endpoint(
     
     request_data = {
         ""allMessages"": formatted_messages,
-        ""chatbotId"": chatbot_id,
+        ""applicationId"": application_id,
         ""traceId"": trace_id,
     }
     
@@ -122,7 +122,7 @@ async def test_message_endpoint(
                     print(f""Error receiving events: {str(e)}"")
                 
                 return {
-                    ""chatbot_id"": chatbot_id,
+                    ""application_id"": application_id,
                     ""trace_id"": trace_id,
                     ""agentState"": last_agent_state
                 }
@@ -153,7 +153,7 @@ async def interactive_session(server_url: str):
             state = await test_message_endpoint(
                 server_url=server_url,
                 messages=[message],
-                chatbot_id=state[""chatbot_id""],
+                application_id=state[""application_id""],
                 trace_id=state[""trace_id""],
                 agent_state=state[""agentState""],
                 settings={""max-iterations"": 3},
@@ -167,7 +167,7 @@ async def main():
     parser = argparse.ArgumentParser(description=""Test the Agent Server API"")
     parser.add_argument(""--url"", default=""http://localhost:8000/message"", help=""Server URL"")
     parser.add_argument(""--message"", help=""Message to send"")
-    parser.add_argument(""--chatbot-id"", help=""Chatbot ID (default: auto-generated)"")
+    parser.add_argument(""--application-id"", help=""Application ID (default: auto-generated)"")
     parser.add_argument(""--trace-id"", help=""Trace ID (default: auto-generated)"")
     parser.add_argument(""--max-iterations"", type=int, default=3, help=""Maximum iterations"")
     parser.add_argument(""--verbose"", ""-v"", action=""store_true"", help=""Verbose output"")
@@ -190,11 +190,11 @@ async def main():
         await test_message_endpoint(
             server_url=args.url,
             messages=[args.message],
-            chatbot_id=args.chatbot_id,
+            application_id=args.application_id,
             trace_id=args.trace_id,
             settings=settings,
             verbose=args.verbose,
         )
 
 if __name__ == ""__main__"":
-    asyncio.run(main())
\ No newline at end of file
+    asyncio.run(main())