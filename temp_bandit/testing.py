@@ -378,7 +378,7 @@ def _wait_for_servers(self, backend: bool, frontend: bool):
                 raise RuntimeError(msg)
 
             for proc in process.children(recursive=True):
-                with contextlib.suppress(psutil.NoSuchProcess):
+                with contextlib.suppress(psutil.NoSuchProcess, psutil.AccessDenied):
                     if ncs := proc.net_connections():
                         for net_conn in ncs:
                             if net_conn.status == psutil.CONN_LISTEN: