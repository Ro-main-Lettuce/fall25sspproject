@@ -16,10 +16,12 @@ class SimpleLLM:
     """"""
 
     def __init__(self, model_name: str, backend: str = ""openai""):
+        """"""Initialize the SimpleLLM instance.""""""
         self._model_name = model_name
         self._backend = backend
 
     def __call__(self, prompt: Union[str, List[str]]) -> Union[str, List[str]]:
+        """"""Call the SimpleLLM instance.""""""
         prompt_list = [prompt] if isinstance(prompt, str) else prompt
         dataset: Dataset = Dataset.from_dict({""prompt"": prompt_list})
 