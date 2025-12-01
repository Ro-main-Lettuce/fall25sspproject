@@ -1,18 +1,22 @@
-""""""Generate synthetic recipes for different cuisines. 
+""""""Generate synthetic recipes for different cuisines.
 
 Demonstrates how to use a structured output format with vllm.
 """"""
 
+import logging
 from typing import List
+
 from pydantic import BaseModel, Field
+
 from bespokelabs import curator
-import logging
 
 logger = logging.getLogger(__name__)
 
 
 # Define response format using Pydantic
 class Recipe(BaseModel):
+    """"""A recipe with title, ingredients, instructions, prep time, cook time, and servings.""""""
+
     title: str = Field(description=""Title of the recipe"")
     ingredients: List[str] = Field(description=""List of ingredients needed"")
     instructions: List[str] = Field(description=""Step by step cooking instructions"")
@@ -22,14 +26,22 @@ class Recipe(BaseModel):
 
 
 class Cuisines(BaseModel):
+    """"""A list of cuisines.""""""
+
     cuisines_list: List[str] = Field(description=""A list of cuisines."")
 
 
 def main():
+    """"""Generate recipes for different world cuisines using vLLM.
+
+    Creates a dataset of cuisine names, sets up a recipe generation prompter using vLLM backend,
+    and generates creative but realistic recipes for each cuisine. The results are printed
+    as a pandas DataFrame.
+    """"""
     # List of cuisines to generate recipes for
     model_path = ""Qwen/Qwen2.5-3B-Instruct""
     cuisines_generator = curator.LLM(
-        prompt_func=lambda: f""Generate 10 diverse cuisines."",
+        prompt_func=lambda: ""Generate 10 diverse cuisines."",
         model_name=model_path,
         response_format=Cuisines,
         parse_func=lambda _, cuisines: [{""cuisine"": t} for t in cuisines.cuisines_list],