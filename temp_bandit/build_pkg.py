@@ -1,21 +1,44 @@
+""""""Build script for packaging the curator viewer application.
+
+This script handles the build process for the curator viewer, including npm installation,
+Next.js build compilation, and running tests. It manages copying build artifacts and
+handles file exclusions during the copy process.
+""""""
+
 import shutil
 import subprocess
 import sys
 from pathlib import Path
 
 
 def run_command(command, cwd=None):
+    """"""Execute a shell command in the specified directory.
+
+    Args:
+        command: The shell command to execute
+        cwd: The working directory to run the command in (optional)
+
+    Returns:
+        subprocess.CompletedProcess: The result of the command execution
+    """"""
     result = subprocess.run(command, shell=True, cwd=cwd, check=True)
     return result
 
 
 def npm_install():
+    """"""Install npm dependencies for the bespoke-dataset-viewer.""""""
     print(""Running npm install"")
     run_command(""npm install"", cwd=""bespoke-dataset-viewer"")
 
 
 def copy_with_excludes(source, target, excludes=None):
-    """"""Copy files/directories while excluding specified paths""""""
+    """"""Copy files/directories while excluding specified paths.
+
+    Args:
+        source: Source path to copy from
+        target: Target path to copy to
+        excludes: List of paths to exclude from copying (optional)
+    """"""
     if excludes is None:
         excludes = []
 
@@ -34,6 +57,11 @@ def ignore_patterns(path, names):
 
 
 def nextjs_build():
+    """"""Build the Next.js application and copy build artifacts.
+
+    Runs the Next.js build process and copies the resulting files to the static folder,
+    excluding specified paths like the Next.js cache directory.
+    """"""
     print(""Running Next.js build"")
     run_command(""npm run build"", cwd=""bespoke-dataset-viewer"")
     print(""Copying build artifacts to static folder"")
@@ -79,6 +107,7 @@ def nextjs_build():
 
 
 def run_pytest():
+    """"""Run pytest and exit if tests fail.""""""
     print(""Running pytest"")
     try:
         run_command(""pytest -v"")
@@ -88,6 +117,10 @@ def run_pytest():
 
 
 def main():
+    """"""Execute the full build process.
+
+    Runs npm install, builds the Next.js application, and runs tests.
+    """"""
     npm_install()
     nextjs_build()
     run_pytest()