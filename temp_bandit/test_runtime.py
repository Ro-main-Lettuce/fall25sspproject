@@ -1645,7 +1645,10 @@ class namespace:
         assert k.globals[""V1""] == 11
 
     @staticmethod
-    @pytest.mark.xfail(sys.version_info >= (3, 13), reason=""Namespace handling changes in Python 3.13"")
+    @pytest.mark.xfail(
+        sys.version_info >= (3, 13),
+        reason=""Namespace handling changes in Python 3.13"",
+    )
     async def test_cell_zero_copy_works(
         strict_kernel: Kernel, exec_req: ExecReqProvider
     ) -> None: