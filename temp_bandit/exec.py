@@ -596,6 +596,8 @@ def run_uvicorn_backend_prod(host: str, port: int, loglevel: LogLevel):
 
         # Our default args, then env args (env args win on conflicts)
         command = [
+            sys.executable,
+            ""-m"",
             ""gunicorn"",
             ""--preload"",
             ""--worker-class"",
@@ -632,6 +634,8 @@ def run_granian_backend_prod(host: str, port: int, loglevel: LogLevel):
     from reflex.utils import processes
 
     command = [
+        sys.executable,
+        ""-m"",
         ""granian"",
         *(""--log-level"", ""critical""),
         *(""--host"", host),