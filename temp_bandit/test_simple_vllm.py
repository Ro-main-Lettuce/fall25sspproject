@@ -1,26 +1,25 @@
-from bespokelabs.curator import LLM
-import huggingface_hub
+import shutil
 import tempfile
+
+import huggingface_hub
 import pytest
-import shutil
+
+from bespokelabs.curator import LLM
 
 
 def download_model(model_name):
     """"""Download a model from the Hugging Face Hub.""""""
     tmpdirname = tempfile.mkdtemp()
-    model_path = huggingface_hub.snapshot_download(
-        repo_id=model_name, repo_type=""model"", local_dir=tmpdirname
-    )
+    model_path = huggingface_hub.snapshot_download(repo_id=model_name, repo_type=""model"", local_dir=tmpdirname)
     return model_path
 
 
 @pytest.mark.parametrize(""model_name"", [""HuggingFaceTB/SmolLM-135M-Instruct""])
 def test_simple_vllm(model_name):
-
     model_path = download_model(model_name)
 
     prompter = LLM(
-        prompt_func=lambda row: f""write me a poem"",
+        prompt_func=lambda row: ""write me a poem"",
         model_name=model_path,
         backend=""vllm"",
         max_tokens=50,