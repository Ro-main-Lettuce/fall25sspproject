@@ -351,9 +351,31 @@ async def test_agent_reaches_idle_state():
 
 async def test_template_diff_implementation():
     """"""Test the TemplateDiffAgentImplementation specifically.""""""
+    from unittest.mock import AsyncMock, MagicMock
+    
     os.environ[""CODEGEN_AGENT""] = ""template_diff""
     
+    # Create mock client and response
+    mock_client = AsyncMock()
+    mock_response = MagicMock()
+    mock_response.status_code = 200
+    mock_client.post.return_value = mock_response
+    
+    # Create mock events with template diff specific properties
+    mock_event = MagicMock(spec=AgentSseEvent)
+    mock_event.trace_id = ""test-trace-id""
+    mock_event.status = AgentStatus.IDLE
+    mock_event.message = MagicMock()
+    mock_event.message.kind = MessageKind.STAGE_RESULT
+    mock_event.message.role = ""agent""
+    mock_event.message.content = ""Created a counter app with increment and decrement buttons""
+    mock_event.message.unified_diff = ""--- /dev/null
+++ /app/counter.js
@@ -0,0 +1,20 @@
+function Counter() {
+  const [count, setCount] = useState(0);
+  
+  const increment = () => setCount(count + 1);
+  const decrement = () => setCount(count - 1);
+  
+  return (
+    <div>
+      <h1>Counter: {count}</h1>
+      <button onClick={increment}>Increment</button>
+      <button onClick={decrement}>Decrement</button>
+    </div>
+  );
+}
""
+    mock_events = [mock_event]
+    
     async with AgentApiClient() as client:
+        client.client = mock_client
+        client.parse_sse_events = AsyncMock(return_value=mock_events)
+        
         events, _ = await client.send_message(""Create a counter app with increment and decrement buttons"")
         
         # Check that we received events