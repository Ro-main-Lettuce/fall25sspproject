@@ -30,7 +30,7 @@ def test_app_name_extraction():
         rsc.get_packages_names()[0],
         rsc.get_id(rsc.get_packages_names()[0], int(appnamehex, 0))[1]
     )
-    assert app_name == ['app_name', 'Evie']
+    assert app_name == ['Evie', 'Evie']
 
 
 class AXMLParserTest(unittest.TestCase):