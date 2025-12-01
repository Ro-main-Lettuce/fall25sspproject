@@ -9,6 +9,14 @@ def _file_gen(reader):
 
 # Instead of requiring counting lines, we can store metadata file that has the number of requests in each file
 def count_lines(filename):
+    """"""Count the number of lines in a file.
+
+    Args:
+        filename: Path to the file to count lines in.
+
+    Returns:
+        int: The number of lines in the file.
+    """"""
     f = open(filename, ""rb"")
     f_gen = _file_gen(f.raw.read)
     return sum(buf.count(b""
"") for buf in f_gen)