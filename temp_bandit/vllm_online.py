@@ -1,5 +1,8 @@
-""""""
-Generate synthetic recipes for different cuisines using vLLM online API.
+""""""Generate synthetic recipes for different cuisines using vLLM online API.
+
+This script demonstrates using vLLM backend with curator to generate recipes for various
+world cuisines in an efficient batched manner. It uses Meta-Llama-3.1-8B-Instruct model.
+
 To start the vLLM server, run the following command:
 vllm serve
 Qwen/Qwen2.5-3B-Instruct
@@ -8,12 +11,20 @@
 --api-key token-abc123
 """"""
 
-from bespokelabs import curator
-from datasets import Dataset
 import os
 
+from datasets import Dataset
+
+from bespokelabs import curator
+
 
 def main():
+    """"""Generate recipes for different world cuisines using vLLM.
+
+    Creates a dataset of cuisine names, sets up a recipe generation prompter using vLLM backend,
+    and generates creative but realistic recipes for each cuisine. The results are printed
+    as a pandas DataFrame.
+    """"""
     # List of cuisines to generate recipes for
     cuisines = [
         {""cuisine"": cuisine}