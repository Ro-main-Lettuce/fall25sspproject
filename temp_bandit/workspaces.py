@@ -157,7 +157,7 @@ def deploy_source(
                 are not allowed. Defaults to `True`.
             random_name_suffix: Whether to append a random suffix to the name.
         """"""
-        source_config_dict = source.get_config().copy()
+        source_config_dict = source._hydrated_config.copy()  # noqa: SLF001 (non-public API)
         source_config_dict[""sourceType""] = source.name.replace(""source-"", """")
 
         if random_name_suffix:
@@ -205,7 +205,7 @@ def deploy_destination(
             random_name_suffix: Whether to append a random suffix to the name.
         """"""
         if isinstance(destination, Destination):
-            destination_conf_dict = destination.get_config().copy()
+            destination_conf_dict = destination._hydrated_config.copy()  # noqa: SLF001 (non-public API)
             destination_conf_dict[""destinationType""] = destination.name.replace(""destination-"", """")
             # raise ValueError(destination_conf_dict)
         else: