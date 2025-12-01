@@ -13,7 +13,7 @@
 def short_term_memory():
     """"""Fixture to create a ShortTermMemory instance""""""
     try:
-        import chromadb
+        import chromadb  # noqa: F401
         HAS_CHROMADB = True
     except ImportError:
         HAS_CHROMADB = False
@@ -39,7 +39,7 @@ def short_term_memory():
 
 def test_save_and_search(short_term_memory):
     try:
-        import chromadb
+        import chromadb  # noqa: F401
         HAS_CHROMADB = True
     except ImportError:
         HAS_CHROMADB = False