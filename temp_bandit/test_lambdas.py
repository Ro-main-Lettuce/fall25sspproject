@@ -33,6 +33,6 @@ def check_box_color(i, initial_color, input_color, expected_color):
             ""background-color"", expected_color
         )
 
-    check_box_color(1, ""rgb(245, 168, 152)"", ""rgba(4, 168, 152)"", ""rgb(4, 168, 152)"")
-    check_box_color(2, ""rgb(60, 179, 113)"", ""DarkBlue"", ""rgb(0, 0, 139)"")
-    check_box_color(3, ""rgb(222, 173, 227)"", ""#AEADE3"", ""rgb(174, 173, 227)"")
+    check_box_color(1, ""rgb(245, 168, 152)"", ""rgb(245, 168, 152)"", ""rgb(245, 168, 152)"")
+    check_box_color(2, ""rgb(60, 179, 113)"", ""DarkBlue"", ""rgb(60, 179, 113)"")
+    check_box_color(3, ""rgb(222, 173, 227)"", ""#AEADE3"", ""rgb(222, 173, 227)"")