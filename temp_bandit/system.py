@@ -77,7 +77,6 @@ def get_sys_packages():
 def get_installed_packages():
     try:
         return {
-            # TODO: add to opt out
             ""Installed Packages"": {
                 dist.metadata.get(""Name""): dist.metadata.get(""Version"") for dist in importlib.metadata.distributions()
             }