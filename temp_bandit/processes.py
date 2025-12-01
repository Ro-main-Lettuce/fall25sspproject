@@ -53,7 +53,7 @@ def get_num_workers() -> int:
     return (os.cpu_count() or 1) * 2 + 1
 
 
-def _is_address_responsive(
+def _can_bind_at_port(
     address_family: socket.AddressFamily | int, address: str, port: int
 ) -> bool:
     """"""Check if a given address and port are responsive.
@@ -68,9 +68,14 @@ def _is_address_responsive(
     """"""
     try:
         with closing(socket.socket(address_family, socket.SOCK_STREAM)) as sock:
-            return sock.connect_ex((address, port)) == 0
+            sock.bind((address, port))
+    except OverflowError:
+        return False
+    except PermissionError:
+        return False
     except OSError:
         return False
+    return True
 
 
 def is_process_on_port(port: int) -> bool:
@@ -82,9 +87,9 @@ def is_process_on_port(port: int) -> bool:
     Returns:
         Whether a process is running on the given port.
     """"""
-    return _is_address_responsive(  # Test IPv4 localhost (127.0.0.1)
+    return not _can_bind_at_port(  # Test IPv4 localhost (127.0.0.1)
         socket.AF_INET, ""127.0.0.1"", port
-    ) or _is_address_responsive(
+    ) or not _can_bind_at_port(
         socket.AF_INET6, ""::1"", port
     )  # Test IPv6 localhost (::1)
 
@@ -99,8 +104,15 @@ def change_port(port: int, _type: str) -> int:
     Returns:
         The new port.
 
+    Raises:
+        Exit: If the port is invalid or if the new port is occupied.
     """"""
     new_port = port + 1
+    if new_port < 0 or new_port > 65535:
+        console.error(
+            f""The {_type} port: {port} is invalid. It must be between 0 and 65535.""
+        )
+        raise click.exceptions.Exit(1)
     if is_process_on_port(new_port):
         return change_port(new_port, _type)
     console.info(