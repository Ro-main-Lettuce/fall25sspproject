@@ -0,0 +1,25 @@
+#!/usr/bin/env python3
+import re
+import os
+import glob
+
+def fix_file(filename):
+    with open(filename, 'r') as file:
+        content = file.read()
+    
+    # Fix adapter declarations
+    pattern = r'(const \w+Adapter = new \w+Adapter\({[^}]*})\s*
\s*'
+    replacement = r'\1)
'
+    content = re.sub(pattern, replacement, content)
+    
+    with open(filename, 'w') as file:
+        file.write(content)
+
+# Find all page.tsx files
+files = glob.glob('apps/laboratory/app/library/**/page.tsx', recursive=True)
+
+for file in files:
+    fix_file(file)
+    print(f""Fixed {file}"")
+
+print(f""Updated {len(files)} files"") 
\ No newline at end of file