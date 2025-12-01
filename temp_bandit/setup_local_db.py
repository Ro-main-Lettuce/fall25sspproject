@@ -1,6 +1,5 @@
 import os
 import sys
-from flask import Flask
 
 os.environ[""SQLALCHEMY_DATABASE_URI""] = ""sqlite:////tmp/test.db""
 os.environ[""FLASK_APP""] = ""app.py""