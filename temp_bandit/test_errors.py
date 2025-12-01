@@ -51,9 +51,7 @@ def test_import_star_error(self) -> None:
         assert error.describe() == ""Cannot use import * in this context""
 
     def test_delete_nonlocal_error(self) -> None:
-        error = DeleteNonlocalError(
-            name=""test_var"", cells=(""cell1"", ""cell2"")
-        )
+        error = DeleteNonlocalError(name=""test_var"", cells=(""cell1"", ""cell2""))
 
         # Test properties
         assert error.type == ""delete-nonlocal""
@@ -149,34 +147,42 @@ def test_marimo_internal_error(self) -> None:
 class TestErrorUtilityFunctions:
     def test_is_unexpected_error(self) -> None:
         # These errors are expected/intentional
-        assert not is_unexpected_error(MarimoAncestorPreventedError(
-            msg="""", raising_cell=""cell1"", blamed_cell=None
-        ))
-        assert not is_unexpected_error(MarimoAncestorStoppedError(
-            msg="""", raising_cell=""cell1""
-        ))
+        assert not is_unexpected_error(
+            MarimoAncestorPreventedError(
+                msg="""", raising_cell=""cell1"", blamed_cell=None
+            )
+        )
+        assert not is_unexpected_error(
+            MarimoAncestorStoppedError(msg="""", raising_cell=""cell1"")
+        )
         assert not is_unexpected_error(MarimoInterruptionError())
 
         # These errors are unexpected
-        assert is_unexpected_error(MarimoExceptionRaisedError(
-            msg="""", exception_type="""", raising_cell=None
-        ))
+        assert is_unexpected_error(
+            MarimoExceptionRaisedError(
+                msg="""", exception_type="""", raising_cell=None
+            )
+        )
         assert is_unexpected_error(MarimoSyntaxError(msg=""""))
         assert is_unexpected_error(UnknownError(msg=""""))
 
     def test_is_sensitive_error(self) -> None:
         # These errors are not sensitive
-        assert not is_sensitive_error(MarimoAncestorPreventedError(
-            msg="""", raising_cell=""cell1"", blamed_cell=None
-        ))
-        assert not is_sensitive_error(MarimoAncestorStoppedError(
-            msg="""", raising_cell=""cell1""
-        ))
+        assert not is_sensitive_error(
+            MarimoAncestorPreventedError(
+                msg="""", raising_cell=""cell1"", blamed_cell=None
+            )
+        )
+        assert not is_sensitive_error(
+            MarimoAncestorStoppedError(msg="""", raising_cell=""cell1"")
+        )
         assert not is_sensitive_error(MarimoInternalError(error_id=""""))
 
         # These errors are sensitive
-        assert is_sensitive_error(MarimoExceptionRaisedError(
-            msg="""", exception_type="""", raising_cell=None
-        ))
+        assert is_sensitive_error(
+            MarimoExceptionRaisedError(
+                msg="""", exception_type="""", raising_cell=None
+            )
+        )
         assert is_sensitive_error(MarimoSyntaxError(msg=""""))
         assert is_sensitive_error(UnknownError(msg=""""))