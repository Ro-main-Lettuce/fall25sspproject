@@ -1,8 +1,10 @@
 import importlib
-import pytest
 import sys
 import warnings
 
+import pytest
+
+
 def test_crew_import_with_numpy():
     """"""Test that crewai can be imported even with NumPy compatibility issues.""""""
     try: