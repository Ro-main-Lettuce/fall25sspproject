@@ -1,6 +1,6 @@
 from codegen.sdk.codebase.factory.get_session import get_codebase_session
-from codegen.shared.enums.programming_language import ProgrammingLanguage
 from codegen.sdk.python.symbol_groups.dict import PyDict
+from codegen.shared.enums.programming_language import ProgrammingLanguage
 
 
 def test_dict_merge(tmpdir) -> None:
@@ -11,17 +11,17 @@ def test_dict_merge(tmpdir) -> None:
 """"""
     with get_codebase_session(tmpdir=tmpdir, files={""test.py"": content}, programming_language=ProgrammingLanguage.PYTHON) as codebase:
         file = codebase.get_file(""test.py"")
-        
+
         dict1_symbol = file.get_symbol(""dict1"")
         dict2_symbol = file.get_symbol(""dict2"")
-        
+
         dict1 = dict1_symbol.value
         dict2 = dict2_symbol.value
-        
+
         # Verify we have PyDict instances
         assert isinstance(dict1, PyDict)
         assert isinstance(dict2, PyDict)
-        
+
         # Merge the dictionaries
         merged_dict = dict1.merge(dict2)
 