@@ -1,11 +1,13 @@
 import os
 from xml.dom import minidom
+import json
 
 _public_res = None
-# copy the newest sdk/platforms/android-?/data/res/values/public.xml here
+
 if _public_res is None:
     _public_res = {}
     root = os.path.dirname(os.path.realpath(__file__))
+    
     xmlfile = os.path.join(root, ""public.xml"")
     if os.path.isfile(xmlfile):
         with open(xmlfile, ""r"") as fp:
@@ -18,24 +20,33 @@
                     _public_res[_type] = {}
                 _public_res[_type][_name] = _id
     else:
-        raise Exception(""need to copy the sdk/platforms/android-?/data/res/values/public.xml here"")
-
+        resfile = os.path.join(root, ""public.json"")
+        if os.path.isfile(resfile):
+            with open(resfile, ""r"") as fp:
+                _public_res = json.load(fp)
+        else:
+            _public_res = {
+                'attr': {},
+                'style': {},
+                'drawable': {},
+                'mipmap': {}
+            }
 SYSTEM_RESOURCES = {
     ""attributes"": {
-        ""forward"": {k: v for k, v in _public_res['attr'].items()},
-        ""inverse"": {v: k for k, v in _public_res['attr'].items()}
+        ""forward"": {k: v for k, v in _public_res.get('attr', {}).items()},
+        ""inverse"": {v: k for k, v in _public_res.get('attr', {}).items()}
     },
     ""styles"": {
-        ""forward"": {k: v for k, v in _public_res['style'].items()},
-        ""inverse"": {v: k for k, v in _public_res['style'].items()}
+        ""forward"": {k: v for k, v in _public_res.get('style', {}).items()},
+        ""inverse"": {v: k for k, v in _public_res.get('style', {}).items()}
     },
     ""drawables"": {
-        ""forward"": {k: v for k, v in _public_res['drawable'].items()},
-        ""inverse"": {v: k for k, v in _public_res['drawable'].items()}
+        ""forward"": {k: v for k, v in _public_res.get('drawable', {}).items()},
+        ""inverse"": {v: k for k, v in _public_res.get('drawable', {}).items()}
     },
     ""mipmaps"": {
-        ""forward"": {k: v for k, v in _public_res['mipmap'].items()},
-        ""inverse"": {v: k for k, v in _public_res['mipmap'].items()}
+        ""forward"": {k: v for k, v in _public_res.get('mipmap', {}).items()},
+        ""inverse"": {v: k for k, v in _public_res.get('mipmap', {}).items()}
     }
 }
 