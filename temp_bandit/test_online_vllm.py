@@ -1,22 +1,20 @@
-from bespokelabs.curator import LLM
-import tempfile
-import huggingface_hub
-import pytest
-import shutil
-import time
 import os
+import shutil
 import socket
-import subprocess
-import shlex
+import tempfile
+import time
+
+import huggingface_hub
 import psutil
+import pytest
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
 
 
@@ -50,13 +48,12 @@ def kill_vllm_server():
 
 @pytest.mark.parametrize(""model_name"", [""HuggingFaceTB/SmolLM-135M-Instruct""])
 def test_online_vllm(model_name):
-
     model_path = download_model(model_name)
     host = socket.gethostname().split(""."")[0]
 
     port = 5432
 
-    pid = start_vllm_server(model_path, host, port)
+    # pid = start_vllm_server(model_path, host, port)
 
     time.sleep(60)
 