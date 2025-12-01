@@ -18,7 +18,7 @@
 timestamp_regex = re.compile((r""^\d{4}-\d?\d-\d?\d""  # date
                               r""(\s|T)""  # separator
                               r""\d?\d:\d?\d:\d?\d(.\d+)?""  # time
-                              r"".*$""))  # timezone
+                              r"".*?$""))  # optional timezone
 # fmt: on
 
 # In Json schema, numbers with a zero fractional part are considered integers. E.G. 1.0 is considered a valid integer