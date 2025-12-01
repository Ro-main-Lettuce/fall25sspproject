@@ -1,24 +1,18 @@
 import logging
 import os
-import platform
-import shutil
-import socket
 import subprocess
 import sys
-import tempfile
-import time
-import webbrowser
 from argparse import ArgumentParser
-from contextlib import closing
 from pathlib import Path
 
 
 def get_viewer_path():
+    """"""Get the path to the viewer directory.""""""
     return str(Path(__file__).parent)
 
 
 def ensure_dependencies():
-    """"""Ensure npm dependencies are installed""""""
+    """"""Ensure npm dependencies are installed.""""""
     static_dir = os.path.join(get_viewer_path(), ""static"")
     node_modules = os.path.join(static_dir, ""node_modules"")
 
@@ -42,7 +36,7 @@ def _setup_logging(level):
 
 
 def check_node_installed():
-    """"""Check if Node.js is installed and return version if found""""""
+    """"""Check if Node.js is installed and return version if found.""""""
     try:
         result = subprocess.run([""node"", ""--version""], capture_output=True, text=True, check=True)
         return result.stdout.strip()
@@ -51,6 +45,7 @@ def check_node_installed():
 
 
 def main():
+    """"""Main function to run the viewer.""""""
     parser = ArgumentParser(description=""Curator Viewer"")
     parser.add_argument(
         ""--host"",