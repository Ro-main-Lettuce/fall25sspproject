@@ -1,12 +1,12 @@
 # Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
 #
 # SPDX-License-Identifier: Apache-2.0
-import arxiv
 
-from autogen.coding.func_with_reqs import with_requirements
 
+from ......coding.func_with_reqs import with_requirements
 
-@with_requirements([""arxiv""], [""arxiv""])
+
+@with_requirements([""arxiv""])
 def arxiv_download(id_list: list, download_dir=""./""):
     """"""Downloads PDF files from ArXiv based on a list of arxiv paper IDs.
 
@@ -17,6 +17,8 @@ def arxiv_download(id_list: list, download_dir=""./""):
     Returns:
         list: A list of paths to the downloaded PDF files.
     """"""
+    import arxiv
+
     paths = []
     for paper in arxiv.Client().results(arxiv.Search(id_list=id_list)):
         path = paper.download_pdf(download_dir, filename=paper.get_short_id() + "".pdf"")