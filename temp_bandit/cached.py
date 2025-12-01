@@ -28,13 +28,20 @@ def normalize(obj):
                 elif k == ""cache_control"":
                     # ignore cache_control field used to control caching
                     pass
+                elif k == ""event_callback"":
+                    pass
+                elif callable(v):
+                    pass
                 elif hasattr(v, ""cache_key""):
                     normalized_dict[k] = v.cache_key
                 else:
                     normalized_dict[k] = normalize(v)
             return normalized_dict
         case _ if hasattr(obj, ""to_dict"") and callable(getattr(obj, ""to_dict"")):
             return normalize(obj.to_dict())
+        case _ if callable(obj):
+            # ignore callable objects as they are not JSON serializable
+            return ""__CALLABLE_PLACEHOLDER__""
         case _:
             return obj
 