@@ -108,20 +108,16 @@ def find_cache_hit(prompt_messages, completion_overrides):
     return None
 
 
-_time_travel_active = None
-
 def check_time_travel_active():
-    global _time_travel_active
-    if _time_travel_active is not None:
-        return _time_travel_active
+    script_dir = os.path.dirname(os.path.abspath(__file__))
+    parent_dir = os.path.dirname(script_dir)
+    config_file_path = os.path.join(parent_dir, "".agentops_time_travel.yaml"")
+
     try:
-        config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "".agentops_time_travel.yaml"")
         with open(config_file_path, ""r"") as config_file:
             config = yaml.safe_load(config_file)
-            _time_travel_active = config.get(""Time_Travel_Debugging_Active"", False)
-            return _time_travel_active
-    except (FileNotFoundError, RecursionError):
-        _time_travel_active = False
+            return config.get(""Time_Travel_Debugging_Active"", False)
+    except FileNotFoundError:
         return False
 
 