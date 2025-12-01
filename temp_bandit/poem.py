@@ -1,6 +1,7 @@
 """"""Example of using the curator library to generate diverse poems.
 
-We generate 10 diverse topics and then generate 2 poems for each topic.""""""
+We generate 10 diverse topics and then generate 2 poems for each topic.
+""""""
 
 from typing import List
 
@@ -13,6 +14,8 @@
 # We use Pydantic and structured outputs to define the format of the response.
 # This defines a list of topics, which is the response format for the topic generator.
 class Topics(BaseModel):
+    """"""A list of topics.""""""
+
     topics_list: List[str] = Field(description=""A list of topics."")
 
 
@@ -32,6 +35,8 @@ class Topics(BaseModel):
 
 # Define a list of poems.
 class Poems(BaseModel):
+    """"""A list of poems.""""""
+
     poems_list: List[str] = Field(description=""A list of poems."")
 
 