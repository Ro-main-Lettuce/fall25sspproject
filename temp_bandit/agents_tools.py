@@ -32,6 +32,7 @@
 import subprocess
 import sys
 import tempfile
+import asyncio
 
 from agents import (
     Agent,
@@ -48,7 +49,15 @@
 os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_api_key_here"")
 os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
 
-agentops.init(auto_start_session=False, tags=[""agentops-example""])
+agentops.init(
+    auto_start_session=False,
+    trace_name=""OpenAI Agents Tools Examples"",
+    tags=[""openai-agents"", ""tools"", ""agentops-example""],
+)
+tracer = agentops.start_trace(
+    trace_name=""OpenAI Agents Tools Examples"",
+    tags=[""openai-agents"", ""tools"", ""agentops-example""],
+)
 
 # ## 1. Code Interpreter Tool
 #
@@ -59,10 +68,7 @@
 # - Perform complex mathematical calculations
 # - Generate plots and visualizations
 # - Handle data processing tasks
-# Start the AgentOps trace session
-tracer = agentops.start_trace(
-    trace_name=""Code Interpreter Tool Example"", tags=[""tools-demo"", ""openai-agents"", ""agentops-example""]
-)
+# Code Interpreter Tool Example
 
 
 async def run_code_interpreter_demo():
@@ -93,10 +99,7 @@ async def run_code_interpreter_demo():
 
 
 # Run the demo
-# await run_code_interpreter_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
+asyncio.run(run_code_interpreter_demo())
 
 # ## 2. File Search Tool
 #
@@ -109,10 +112,7 @@ async def run_code_interpreter_demo():
 # - Configurable result limits
 #
 # **Note:** This example requires a pre-configured vector store ID.
-# Start the AgentOps trace session
-tracer = agentops.start_trace(
-    trace_name=""File Search Tool Example"", tags=[""tools-demo"", ""openai-agents"", ""agentops-example""]
-)
+# File Search Tool Example
 
 
 async def run_file_search_demo():
@@ -141,10 +141,7 @@ async def run_file_search_demo():
 
 
 # Run the demo
-# await run_file_search_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
+asyncio.run(run_file_search_demo())
 
 # ## 3. Image Generation Tool
 #
@@ -155,10 +152,7 @@ async def run_file_search_demo():
 # - Configurable quality settings
 # - Support for various image styles
 # - Automatic image saving and display
-# Start the AgentOps trace session
-tracer = agentops.start_trace(
-    trace_name=""Image Generation Tool Example"", tags=[""tools-demo"", ""openai-agents"", ""agentops-example""]
-)
+# Image Generation Tool Example
 
 
 def open_file(path: str) -> None:
@@ -197,19 +191,18 @@ async def run_image_generation_demo():
                     tmp.write(base64.b64decode(img_result))
                     temp_path = tmp.name
 
-                # Open the image
+                # Open the image (optional - may not work in headless environments)
                 print(f""Image saved to: {temp_path}"")
                 try:
                     open_file(temp_path)
+                    print(""Image opened successfully"")
                 except Exception as e:
-                    print(f""Could not open image automatically: {e}"")
+                    print(f""Could not open image automatically (this is normal in headless environments): {e}"")
+                    print(""You can manually open the image file if needed"")
 
 
 # Run the demo
-# await run_image_generation_demo()
-
-# End the AgentOps trace session
-agentops.end_trace(tracer, end_state=""Success"")
+asyncio.run(run_image_generation_demo())
 
 # ## 4. Web Search Tool
 #
@@ -220,10 +213,7 @@ async def run_image_generation_demo():
 # - Location-aware search results
 # - Real-time data access
 # - Configurable search parameters
-# Start the AgentOps trace session
-tracer = agentops.start_trace(
-    trace_name=""Web Search Tool Example"", tags=[""tools-demo"", ""openai-agents"", ""agentops-example""]
-)
+# Web Search Tool Example
 
 
 async def run_web_search_demo():
@@ -243,11 +233,20 @@ async def run_web_search_demo():
 
 
 # Run the demo
-# await run_web_search_demo()
-
-# End the AgentOps trace session
+asyncio.run(run_web_search_demo())
 agentops.end_trace(tracer, end_state=""Success"")
 
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=tracer)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise
+
+
 # ## Conclusion
 #
 # Each tool extends agent capabilities and enables sophisticated automation. **AgentOps makes tool observability effortless** - simply import the library and all your tool interactions are automatically tracked, visualized, and analyzed. This enables you to: