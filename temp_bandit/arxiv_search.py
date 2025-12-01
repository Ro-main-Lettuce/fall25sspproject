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
 def arxiv_search(query, max_results=10, sortby=""relevance""):
     """"""Search for articles on arXiv based on the given query.
 
@@ -24,6 +24,7 @@ def arxiv_search(query, max_results=10, sortby=""relevance""):
             - 'doi': The DOI of the article (If applicable).
             - 'published': The publication date of the article in the format 'Y-M'.
     """"""
+    import arxiv
 
     def get_author(r):
         return "", "".join(a.name for a in r.authors)