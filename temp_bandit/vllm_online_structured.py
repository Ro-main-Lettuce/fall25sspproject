@@ -1,5 +1,9 @@
-""""""
-Generate synthetic recipes for different cuisines using vLLM online API.
+""""""Generate synthetic recipes for different cuisines using vLLM online API with structured output.
+
+This script demonstrates using vLLM backend with curator to generate structured recipe data for various
+world cuisines in an efficient batched manner. It uses the Qwen2.5-3B-Instruct model and expects
+responses in a structured format defined by Pydantic models.
+
 To start the vLLM server, run the following command:
 vllm serve
 Qwen/Qwen2.5-3B-Instruct
@@ -8,14 +12,18 @@
 --api-key token-abc123
 """"""
 
-from bespokelabs import curator
-from datasets import Dataset
 import os
 from typing import List
+
+from datasets import Dataset
 from pydantic import BaseModel, Field
 
+from bespokelabs import curator
+
 
 class Recipe(BaseModel):
+    """"""A recipe with structured fields for title, ingredients, instructions and timing details.""""""
+
     title: str = Field(description=""Title of the recipe"")
     ingredients: List[str] = Field(description=""List of ingredients needed"")
     instructions: List[str] = Field(description=""Step by step cooking instructions"")
@@ -25,6 +33,13 @@ class Recipe(BaseModel):
 
 
 def main():
+    """"""Generate structured recipes for different world cuisines using vLLM.
+
+    Creates a dataset of cuisine names, sets up a recipe generation prompter using vLLM backend,
+    and generates creative but realistic recipes for each cuisine. The results are parsed into
+    a structured format with title, ingredients, instructions and timing details. The structured
+    recipes are printed as a pandas DataFrame.
+    """"""
     # List of cuisines to generate recipes for
     cuisines = [
         {""cuisine"": cuisine}
@@ -46,9 +61,9 @@ def main():
     model_path = ""Qwen/Qwen2.5-3B-Instruct""
     model_path = f""hosted_vllm/{model_path}""
 
-    API_KEY = ""token-abc123""
+    api_key = ""token-abc123""
 
-    os.environ[""HOSTED_VLLM_API_KEY""] = API_KEY
+    os.environ[""HOSTED_VLLM_API_KEY""] = api_key
 
     # Define the vLLM server params
     PORT = 8787