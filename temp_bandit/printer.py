@@ -1,7 +1,11 @@
+""""""Utility for colored console output.""""""
+
 from typing import Optional
 
 
 class Printer:
+    """"""Handles colored console output formatting.""""""
+
     def print(self, content: str, color: Optional[str] = None):
         if color == ""purple"":
             self._print_purple(content)
@@ -17,6 +21,16 @@ def print(self, content: str, color: Optional[str] = None):
             self._print_yellow(content)
         elif color == ""bold_yellow"":
             self._print_bold_yellow(content)
+        elif color == ""cyan"":
+            self._print_cyan(content)
+        elif color == ""bold_cyan"":
+            self._print_bold_cyan(content)
+        elif color == ""magenta"":
+            self._print_magenta(content)
+        elif color == ""bold_magenta"":
+            self._print_bold_magenta(content)
+        elif color == ""green"":
+            self._print_green(content)
         else:
             print(content)
 
@@ -40,3 +54,18 @@ def _print_yellow(self, content):
 
     def _print_bold_yellow(self, content):
         print(""\033[1m\033[93m {}\033[00m"".format(content))
+
+    def _print_cyan(self, content):
+        print(""\033[96m {}\033[00m"".format(content))
+
+    def _print_bold_cyan(self, content):
+        print(""\033[1m\033[96m {}\033[00m"".format(content))
+
+    def _print_magenta(self, content):
+        print(""\033[35m {}\033[00m"".format(content))
+
+    def _print_bold_magenta(self, content):
+        print(""\033[1m\033[35m {}\033[00m"".format(content))
+
+    def _print_green(self, content):
+        print(""\033[32m {}\033[00m"".format(content))