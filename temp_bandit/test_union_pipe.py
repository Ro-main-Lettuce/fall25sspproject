@@ -1,5 +1,5 @@
 import sys
-import unittest
+import pytest
 from typing import Union
 
 import instructor
@@ -19,16 +19,16 @@ class UserWithPipe(BaseModel):
     category: str | None
 
 
-class TestUnionPipe(unittest.TestCase):
-    def test_process_generic_arg_union(self):
-        """"""Test that _process_generic_arg correctly handles Union[str, None].""""""
-        annotation = UserWithUnion.__annotations__[""category""]
-        processed = _process_generic_arg(annotation)
-        self.assertIsNotNone(processed)
+def test_process_generic_arg_union():
+    """"""Test that _process_generic_arg correctly handles Union[str, None].""""""
+    annotation = UserWithUnion.__annotations__[""category""]
+    processed = _process_generic_arg(annotation)
+    assert processed is not None
 
-    @unittest.skipIf(sys.version_info < (3, 10), ""Union pipe syntax requires Python 3.10+"")
-    def test_process_generic_arg_pipe(self):
-        """"""Test that _process_generic_arg correctly handles str | None.""""""
-        annotation = UserWithPipe.__annotations__[""category""]
-        processed = _process_generic_arg(annotation)
-        self.assertIsNotNone(processed)
+
+@pytest.mark.skipif(sys.version_info < (3, 10), reason=""Union pipe syntax requires Python 3.10+"")
+def test_process_generic_arg_pipe():
+    """"""Test that _process_generic_arg correctly handles str | None.""""""
+    annotation = UserWithPipe.__annotations__[""category""]
+    processed = _process_generic_arg(annotation)
+    assert processed is not None