@@ -148,8 +148,15 @@ def __init__(self, raw_buff):
                                         # Now we will read all entries!
                                         # Not sure if this is a good solution though
                                         self.buff.set_idx(ate.start)
-                                except ResParserError as e:
-                                    log.warning(""Skipping corrupted ARSC entry at res_id %x: %s"", res_id, e)
+                                except Exception as e:
+                                    log.debug(""Skipping ARSC entry at res_id %x: %s"", res_id, e)
+                                    class PlaceholderEntry:
+                                        def __init__(self, res_id):
+                                            self.mResId = res_id
+                                            self.start = self.buff.get_idx() if hasattr(self, 'buff') else 0
+                                        def is_weak(self):
+                                            return False
+                                    self.packages[package_name].append(PlaceholderEntry(res_id))
                                     continue
                     elif pkg_chunk_header.type == const.RES_TABLE_LIBRARY_TYPE:
                         log.warning(""RES_TABLE_LIBRARY_TYPE chunk is not supported"")
@@ -189,42 +196,48 @@ def _analyse(self):
                             if entry != -1:
                                 ate = self.packages[package_name][nb + 3 + nb_i]
 
-                                self.resource_values[ate.mResId][a_res_type.config] = ate
-                                self.resource_keys[package_name][a_res_type.get_type()][ate.get_value()] = ate.mResId
-
-                                if ate.get_index() != -1:
-                                    c_value[""public""].append(
-                                        (a_res_type.get_type(), ate.get_value(),
-                                         ate.mResId))
-
-                                if a_res_type.get_type() not in c_value:
-                                    c_value[a_res_type.get_type()] = []
-
-                                if a_res_type.get_type() == ""string"":
-                                    c_value[""string""].append(
-                                        self.get_resource_string(ate))
-
-                                elif a_res_type.get_type() == ""id"":
-                                    if not ate.is_complex():
-                                        c_value[""id""].append(
-                                            self.get_resource_id(ate))
-
-                                elif a_res_type.get_type() == ""bool"":
-                                    if not ate.is_complex():
-                                        c_value[""bool""].append(
-                                            self.get_resource_bool(ate))
-
-                                elif a_res_type.get_type() == ""integer"":
-                                    c_value[""integer""].append(
-                                        self.get_resource_integer(ate))
-
-                                elif a_res_type.get_type() == ""color"":
-                                    c_value[""color""].append(
-                                        self.get_resource_color(ate))
-
-                                elif a_res_type.get_type() == ""dimen"":
-                                    c_value[""dimen""].append(
-                                        self.get_resource_dimen(ate))
+                                if isinstance(ate, ARSCResTableEntry) and hasattr(ate, 'mResId'):
+                                    try:
+                                        self.resource_values[ate.mResId][a_res_type.config] = ate
+                                        self.resource_keys[package_name][a_res_type.get_type()][ate.get_value()] = ate.mResId
+
+                                        if ate.get_index() != -1:
+                                            c_value[""public""].append(
+                                                (a_res_type.get_type(), ate.get_value(),
+                                                 ate.mResId))
+
+                                        if a_res_type.get_type() not in c_value:
+                                            c_value[a_res_type.get_type()] = []
+
+                                        if a_res_type.get_type() == ""string"":
+                                            c_value[""string""].append(
+                                                self.get_resource_string(ate))
+
+                                        elif a_res_type.get_type() == ""id"":
+                                            if not ate.is_complex():
+                                                c_value[""id""].append(
+                                                    self.get_resource_id(ate))
+
+                                        elif a_res_type.get_type() == ""bool"":
+                                            if not ate.is_complex():
+                                                c_value[""bool""].append(
+                                                    self.get_resource_bool(ate))
+
+                                        elif a_res_type.get_type() == ""integer"":
+                                            c_value[""integer""].append(
+                                                self.get_resource_integer(ate))
+
+                                        elif a_res_type.get_type() == ""color"":
+                                            c_value[""color""].append(
+                                                self.get_resource_color(ate))
+
+                                        elif a_res_type.get_type() == ""dimen"":
+                                            c_value[""dimen""].append(
+                                                self.get_resource_dimen(ate))
+                                    except Exception as resource_e:
+                                        log.debug(""Failed to process resource for entry %s: %s"", ate.mResId, resource_e)
+                                else:
+                                    log.debug(""Skipping non-ARSCResTableEntry object at index %d: %s"", nb + 3 + nb_i, type(ate).__name__)
 
                                 nb_i += 1
                         nb += 3 + nb_i - 1  # -1 to account for the nb+=1 on the next line
@@ -554,7 +567,29 @@ def __init__(self, android_resources, config=None):
 
         def resolve(self, res_id):
             result = []
-            self._resolve_into_result(result, res_id, self.wanted_config)
+            if res_id not in self.resources.resource_values:
+                log.warning(""Resource ID 0x%x not found in resource_values"", res_id)
+                return result
+            
+            configs = self.resources.resource_values[res_id]
+            log.debug(""Available configurations for resource 0x%x: %s"", res_id, list(configs.keys()))
+            
+            if self.wanted_config and self.wanted_config in configs:
+                log.debug(""Found exact config match for resource 0x%x"", res_id)
+                self._resolve_into_result(result, res_id, self.wanted_config)
+                return result
+            
+            for conf in configs:
+                if conf.get_language() == '\x00\x00' and conf.get_country() == '\x00\x00':
+                    log.debug(""Using default config for resource 0x%x"", res_id)
+                    self._resolve_into_result(result, res_id, conf)
+                    return result
+            
+            if configs:
+                first_config = list(configs.keys())[0]
+                log.debug(""Using first available config for resource 0x%x: %s"", res_id, first_config)
+                self._resolve_into_result(result, res_id, first_config)
+            
             return result
 
         def _resolve_into_result(self, result, res_id, config):
@@ -726,6 +761,9 @@ def parse_id(name):
         else:
             res_id = name
 
+        if res_id.isdigit():
+            return int(res_id), package
+        
         if len(res_id) != 8:
             raise ValueError(""Numerical ID is not 8 characters long: '{}'"".format(res_id))
 