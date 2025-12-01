@@ -1,4 +1,4 @@
-""""""Generate synthetic recipes for different cuisines. 
+""""""Generate synthetic recipes for different cuisines.
 
 Demonstrates how to use a structured output format with Litellm.
 """"""
@@ -15,6 +15,8 @@
 
 # Define response format using Pydantic
 class Recipe(BaseModel):
+    """"""A recipe with title, ingredients, instructions, prep time, cook time, and servings.""""""
+
     title: str = Field(description=""Title of the recipe"")
     ingredients: List[str] = Field(description=""List of ingredients needed"")
     instructions: List[str] = Field(description=""Step by step cooking instructions"")
@@ -24,10 +26,13 @@ class Recipe(BaseModel):
 
 
 class Cuisines(BaseModel):
+    """"""A list of cuisines.""""""
+
     cuisines_list: List[str] = Field(description=""A list of cuisines."")
 
 
 def main():
+    """"""Main function to generate synthetic recipes.""""""
     # We define a prompter that generates cuisines
     #############################################
     # To use Claude models:
@@ -36,7 +41,7 @@ def main():
     # 3. Set environment variable: ANTHROPIC_API_KEY
     #############################################
     cuisines_generator = curator.LLM(
-        prompt_func=lambda: f""Generate 10 diverse cuisines."",
+        prompt_func=lambda: ""Generate 10 diverse cuisines."",
         model_name=""claude-3-5-haiku-20241022"",
         response_format=Cuisines,
         parse_func=lambda _, cuisines: [{""cuisine"": t} for t in cuisines.cuisines_list],