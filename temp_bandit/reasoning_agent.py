@@ -7,6 +7,7 @@
 import warnings
 from typing import Optional
 
+from ...import_utils import optional_import_block
 from ..agent import Agent
 from ..assistant_agent import AssistantAgent
 
@@ -169,9 +170,10 @@ def visualize_tree(root: ThinkNode) -> None:
     Args:
         root (ThinkNode): The root node of the tree.
     """"""
-    try:
+    with optional_import_block() as result:
         from graphviz import Digraph
-    except ImportError:
+
+    if not result.is_successful:
         print(""Please install graphviz: pip install graphviz"")
         return
 
@@ -341,9 +343,9 @@ def __init__(
                     exploration_constant (float): UCT exploration parameter (default: 1.41)
 
                 Example configs:
-                    {""method"": ""beam_search"", ""beam_size"": 5, ""max_depth"": 4}
-                    {""method"": ""mcts"", ""nsim"": 10, ""exploration_constant"": 2.0}
-                    {""method"": ""lats"", ""nsim"": 5, ""forest_size"": 3}
+                    `{""method"": ""beam_search"", ""beam_size"": 5, ""max_depth"": 4}`
+                    `{""method"": ""mcts"", ""nsim"": 10, ""exploration_constant"": 2.0}`
+                    `{""method"": ""lats"", ""nsim"": 5, ""forest_size"": 3}`
         """"""
         super().__init__(name=name, llm_config=llm_config, **kwargs)
         self._verbose = verbose