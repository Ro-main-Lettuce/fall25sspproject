@@ -192,12 +192,7 @@ def import_service(
             if not all_services:
                 raise ImportServiceError(""No service found in the module"")
             if len(all_services) > 1:
-                service_names = []
-                for s in all_services:
-                    if hasattr(s.__class__, ""__wrapped__""):
-                        service_names.append(s.__class__.__wrapped__.__name__)
-                    else:
-                        service_names.append(s.__class__.__name__)
+                service_names = [s.inner.__name__ for s in all_services]
                 raise ImportServiceError(
                     f""Multiple services found in the module. Please specify the service ""
                     f""you'd like to use with '{module_name}:SERVICE_NAME'. ""