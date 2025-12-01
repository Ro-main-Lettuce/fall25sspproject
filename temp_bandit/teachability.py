@@ -8,14 +8,15 @@
 import pickle
 from typing import Optional, Union
 
-import chromadb
-from chromadb.config import Settings
-
-from autogen.agentchat.assistant_agent import ConversableAgent
-from autogen.agentchat.contrib.capabilities.agent_capability import AgentCapability
-from autogen.agentchat.contrib.text_analyzer_agent import TextAnalyzerAgent
-
 from ....formatting_utils import colored
+from ....import_utils import optional_import_block, require_optional_import
+from ...assistant_agent import ConversableAgent
+from ..text_analyzer_agent import TextAnalyzerAgent
+from .agent_capability import AgentCapability
+
+with optional_import_block():
+    import chromadb
+    from chromadb.config import Settings
 
 
 class Teachability(AgentCapability):
@@ -238,6 +239,7 @@ def _analyze(self, text_to_analyze: Union[dict, str], analysis_instructions: Uni
         return self.teachable_agent.last_message(self.analyzer)[""content""]
 
 
+@require_optional_import(""chromadb"", ""teachable"")
 class MemoStore:
     """"""Provides memory storage and retrieval for a teachable agent, using a vector database.
     Each DB entry (called a memo) is a pair of strings: an input text and an output text.