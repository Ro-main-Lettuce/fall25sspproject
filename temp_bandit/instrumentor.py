@@ -70,8 +70,7 @@ def _uninstrument(self, **kwargs):
                 unwrap(wrap_config)
             except Exception as e:
                 logger.debug(
-                    f""Failed to unwrap {wrap_config.package}.""
-                    f""{wrap_config.class_name}.{wrap_config.method_name}: {e}""
+                    f""Failed to unwrap {wrap_config.package}.{wrap_config.class_name}.{wrap_config.method_name}: {e}""
                 )
 
         # Perform custom unwrapping
@@ -89,7 +88,7 @@ def _wrap_methods(self):
                 wrap(wrap_config, self._tracer)
             except (AttributeError, ModuleNotFoundError) as e:
                 logger.debug(
-                    f""Could not wrap {wrap_config.package}."" f""{wrap_config.class_name}.{wrap_config.method_name}: {e}""
+                    f""Could not wrap {wrap_config.package}.{wrap_config.class_name}.{wrap_config.method_name}: {e}""
                 )
 
     @abstractmethod