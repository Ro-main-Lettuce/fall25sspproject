@@ -1,96 +1,149 @@
 """"""
-# Tool Integration with RAG (Retrieval-Augmented Generation) in Agno
+# Tool Integration Example with Agno
 
-This example demonstrates how to enhance Agno agents with RAG capabilities, allowing them to access and reason over external knowledge bases for more accurate and source-backed responses.
+This example demonstrates how to integrate and use various tools with Agno agents,
+showing how AgentOps automatically tracks tool usage and agent interactions.
 
 ## Overview
-This example shows how to integrate RAG with Agno agents where we:
+This example demonstrates:
 
-1. **Set up a knowledge base** with documents, URLs, and other external sources
-2. **Configure vector databases** (like Pinecone, Weaviate, or ChromaDB) for efficient semantic search
-3. **Implement retrieval** using embeddings and reranking for accurate information access
-4. **Create RAG-enabled agents** that can search, retrieve, and reason over the knowledge base
+1. **Using built-in Agno tools** like GoogleSearch, DuckDuckGo, and Arxiv
+2. **Creating agents with tools** and seeing how they use them
+3. **Tool execution tracking** with AgentOps
+4. **Combining multiple tools** for comprehensive research
 
-By using RAG, agents can provide responses backed by external sources rather than relying solely on their training data, significantly improving accuracy and verifiability of their outputs.
-
-RAG enables agents to access and reason over large knowledge bases,
-providing accurate, source-backed responses instead of relying solely on training data.
+This example uses actual Agno components to show real tool integration patterns.
 """"""
 
 import os
+from dotenv import load_dotenv
+import agentops
 from agno.agent import Agent
 from agno.models.openai import OpenAIChat
-import agentops
-from dotenv import load_dotenv
-
-# Knowledge and RAG components
-from agno.knowledge.url import UrlKnowledge
-from agno.vectordb.lancedb import LanceDb
-from agno.vectordb.search import SearchType
-from agno.embedder.cohere import CohereEmbedder
-from agno.reranker.cohere import CohereReranker
-from agno.tools.reasoning import ReasoningTools
+from agno.tools.googlesearch import GoogleSearchTools
+from agno.tools.duckduckgo import DuckDuckGoTools
+from agno.tools.arxiv import ArxivTools
 
 # Load environment variables
 load_dotenv()
 
-# Initialize AgentOps for monitoring
-agentops.init(auto_start_session=False, tags=[""agno-example"", ""tool-integrations""])
+# Set environment variables if not already set
+os.environ[""OPENAI_API_KEY""] = os.getenv(""OPENAI_API_KEY"", ""your_openai_api_key_here"")
+os.environ[""AGENTOPS_API_KEY""] = os.getenv(""AGENTOPS_API_KEY"", ""your_agentops_api_key_here"")
 
-# API keys and configuration
-os.environ[""COHERE_API_KEY""] = os.getenv(""COHERE_API_KEY"")
+# Initialize AgentOps
+agentops.init(
+    auto_start_session=False,
+    tags=[""agno-tools"", ""tool-integration"", ""demo""]
+)
 
 
 def demonstrate_tool_integration():
-    """"""
-    Demonstrate advanced tool integration with RAG and knowledge bases.
-
-    This function shows how to:
-    1. Create a knowledge base from external sources
-    2. Set up a vector database with embeddings
-    3. Configure an agent with RAG capabilities
-    4. Enable reasoning tools for complex problem-solving
-    """"""
-    tracer = agentops.start_trace(trace_name=""Agno Tool Integration Demonstration"")
+    """"""Demonstrate tool integration with Agno agents.""""""
+    print(""🚀 Agno Tool Integration Demonstration"")
+    print(""="" * 60)
+
+    # Start AgentOps trace
+    tracer = agentops.start_trace(trace_name=""Agno Tool Integration Demo"")
+
     try:
-        # Create knowledge base from documentation URLs
-        # This loads content from the specified URLs and prepares it for RAG
-        knowledge_base = UrlKnowledge(
-            urls=[""https://docs.agno.com/introduction/agents.md""],
-            vector_db=LanceDb(
-                uri=""tmp/lancedb"",
-                table_name=""agno_docs"",
-                search_type=SearchType.hybrid,
-                embedder=CohereEmbedder(
-                    id=""embed-v4.0"",
-                ),
-                reranker=CohereReranker(
-                    model=""rerank-v3.5"",
-                ),
-            ),
+        # Example 1: Single Tool Agent
+        print(""
📌 Example 1: Agent with Google Search Tool"")
+        print(""-"" * 40)
+
+        search_agent = Agent(
+            name=""Search Agent"",
+            role=""Research information using Google Search"",
+            model=OpenAIChat(id=""gpt-4o-mini""),
+            tools=[GoogleSearchTools()],
+            instructions=""You are a research assistant. Use Google Search to find accurate, up-to-date information.""
+        )
+
+        response = search_agent.run(""What are the latest developments in AI agents?"")
+        print(f""Search Agent Response:
{response.content}"")
+
+        # Example 2: Multi-Tool Agent
+        print(""

📌 Example 2: Agent with Multiple Tools"")
+        print(""-"" * 40)
+
+        research_agent = Agent(
+            name=""Research Agent"",
+            role=""Comprehensive research using multiple tools"",
+            model=OpenAIChat(id=""gpt-4o-mini""),
+            tools=[
+                GoogleSearchTools(),
+                ArxivTools(),
+                DuckDuckGoTools()
+            ],
+            instructions=""""""You are a comprehensive research assistant. 
+            Use Google Search for general information, Arxiv for academic papers, 
+            and DuckDuckGo as an alternative search engine. 
+            Provide well-researched, balanced information from multiple sources.""""""
         )
 
-        # Create an intelligent agent with RAG capabilities
-        agent = Agent(
+        response = research_agent.run(
+            ""Find information about recent advances in tool-use for AI agents. ""
+            ""Include both academic research and practical implementations.""
+        )
+        print(f""Research Agent Response:
{response.content}"")
+
+        # Example 3: Specialized Tool Usage
+        print(""

📌 Example 3: Academic Research with Arxiv"")
+        print(""-"" * 40)
+
+        academic_agent = Agent(
+            name=""Academic Agent"",
+            role=""Find and summarize academic papers"",
             model=OpenAIChat(id=""gpt-4o-mini""),
-            knowledge=knowledge_base,
-            search_knowledge=True,
-            tools=[ReasoningTools(add_instructions=True)],
-            instructions=[
-                ""Include sources in your response."",
-                ""Always search your knowledge before answering the question."",
-                ""Only include the output in your response. No other text."",
+            tools=[ArxivTools()],
+            instructions=""You are an academic research assistant. Use Arxiv to find relevant papers and provide concise summaries.""
+        )
+
+        response = academic_agent.run(
+            ""Find recent papers about tool augmented language models""
+        )
+        print(f""Academic Agent Response:
{response.content}"")
+
+        # Example 4: Comparing Search Tools
+        print(""

📌 Example 4: Comparing Different Search Tools"")
+        print(""-"" * 40)
+
+        comparison_agent = Agent(
+            name=""Comparison Agent"",
+            role=""Compare results from different search engines"",
+            model=OpenAIChat(id=""gpt-4o-mini""),
+            tools=[
+                GoogleSearchTools(),
+                DuckDuckGoTools()
             ],
+            instructions=""""""Compare search results from Google and DuckDuckGo. 
+            Note any differences in results, ranking, or information quality.
+            Be objective in your comparison.""""""
         )
 
-        # Print response with full reasoning process visible
-        agent.print_response(
-            ""What are Agents?"",
-            show_full_reasoning=True,
+        response = comparison_agent.run(
+            ""Search for 'AgentOps observability platform' on both search engines and compare the results""
         )
+        print(f""Comparison Agent Response:
{response.content}"")
+
+        print(""

✨ Demonstration Complete!"")
+        print(""
Key Takeaways:"")
+        print(""- Agno agents can use multiple tools seamlessly"")
+        print(""- Tools are automatically invoked based on the agent's task"")
+        print(""- AgentOps tracks all tool executions automatically"")
+        print(""- Different tools serve different purposes (web search, academic search, etc.)"")
+        print(""- Agents can compare and synthesize information from multiple tools"")
+
+        # End the AgentOps trace successfully
+        print(""
📊 View your tool execution traces in AgentOps:"")
+        print(""   Visit https://app.agentops.ai/ to see detailed analytics"")
         agentops.end_trace(tracer, end_state=""Success"")
-    except Exception:
+
+    except Exception as e:
+        print(f""
❌ An error occurred: {e}"")
         agentops.end_trace(tracer, end_state=""Error"")
+        raise
 
 
-demonstrate_tool_integration()
+if __name__ == ""__main__"":
+    demonstrate_tool_integration()