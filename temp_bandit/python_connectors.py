@@ -168,7 +168,7 @@ async def install_testing_environment(
         )
         if self.common_test_dependencies:
             container_with_test_deps = container_with_test_deps.with_user(""root"").with_exec(
-                [""pip"", ""install"", f'{"" "".join(self.common_test_dependencies)}']
+                [""pip"", ""install""] + self.common_test_dependencies
             )
 
         container_with_test_deps = (