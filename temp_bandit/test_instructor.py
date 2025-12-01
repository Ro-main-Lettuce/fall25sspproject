@@ -1,5 +1,5 @@
 import os
-from typing import Literal, Union
+from typing import Literal
 
 import pytest
 from conftest import BenchmarkResult, create_benchmark
@@ -12,7 +12,7 @@
 load_dotenv()
 
 
-def get_instructor_client(provider: Union[Literal[""openai"", ""gemini"", ""fireworks"", ""ollama""], str] = ""openai""):
+def get_instructor_client(provider: Literal[""openai"", ""gemini"", ""fireworks"", ""ollama""] = ""openai""):
     import instructor
     from openai import OpenAI
 