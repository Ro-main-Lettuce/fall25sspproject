@@ -484,19 +484,21 @@ def get_app_name(self):
         :rtype: :class:`str`
         """"""
 
-        app_name = self.get_attribute_value('application', 'label')
-        if app_name is None:
-            activities = self.get_main_activities()
-            main_activity_name = None
-            if len(activities) > 0:
-                main_activity_name = activities.pop()
-            app_name = self.get_attribute_value(
-                'activity', 'label', name=main_activity_name
-            )
+        try:
+            app_name = self.get_attribute_value('application', 'label')
+            if app_name is None:
+                activities = self.get_main_activities()
+                main_activity_name = None
+                if len(activities) > 0:
+                    main_activity_name = activities.pop()
+                app_name = self.get_attribute_value(
+                    'activity', 'label', name=main_activity_name
+                )
+        except Exception as e:
+            log.warning(""Exception during app name resolution: %s"", e)
+            app_name = None
 
         if app_name is None:
-            # No App name set
-            # TODO return packagename instead?
             log.warning(""It looks like that no app name is set for the main activity!"")
             return """"
 
@@ -506,6 +508,9 @@ def get_app_name(self):
                 # TODO: What should be the correct return value here?
                 return app_name
 
+            if not getattr(res_parser, 'analyzed', False):
+                res_parser._analyse()
+
             res_id, package = res_parser.parse_id(app_name)
 
             # If the package name is the same as the APK package,
@@ -523,9 +528,14 @@ def get_app_name(self):
                     return app_name
 
             try:
-                app_name = res_parser.get_resolved_res_configs(
+                resolved_configs = res_parser.get_resolved_res_configs(
                     res_id,
-                    ARSCResTableConfig.default_config())[0][1]
+                    ARSCResTableConfig.default_config())
+                if resolved_configs:
+                    app_name = resolved_configs[0][1]
+                    log.debug(""Successfully resolved app name: %s"", app_name)
+                else:
+                    log.warning(""No resolved configs found for resource ID 0x%x"", res_id)
             except Exception as e:
                 log.warning(""Exception selecting app name: %s"" % e)
         return app_name
@@ -932,6 +942,17 @@ def get_attribute_value(
         for value in self.get_all_attribute_value(
                 tag_name, attribute, format_value, **attribute_filter):
             if value is not None:
+                if value.startswith('@'):
+                    try:
+                        from pyaxmlparser.arscparser import ARSCParser
+                        res_id, package = ARSCParser.parse_id(value)
+                        resolved = self.get_resolved_res_configs(res_id)
+                        if resolved:
+                            for config, resolved_value in resolved:
+                                if isinstance(resolved_value, str) and resolved_value.strip():
+                                    return resolved_value
+                    except Exception as e:
+                        log.debug(""Failed to resolve resource %s: %s"", value, e)
                 return value
 
     def get_value_from_tag(self, tag, attribute):