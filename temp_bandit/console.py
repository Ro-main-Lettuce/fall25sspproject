@@ -79,7 +79,7 @@ def is_debug() -> bool:
     return _LOG_LEVEL <= LogLevel.DEBUG
 
 
-def print(msg: str, dedupe: bool = False, **kwargs):
+def print(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print a message.
 
     Args:
@@ -143,7 +143,7 @@ def error_log_file_console():
     return Console(file=env_error_log_file.open(""a"", encoding=""utf-8""))
 
 
-def print_to_log_file(msg: str, dedupe: bool = False, **kwargs):
+def print_to_log_file(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print a message to the log file.
 
     Args:
@@ -154,7 +154,7 @@ def print_to_log_file(msg: str, dedupe: bool = False, **kwargs):
     log_file_console().print(msg, **kwargs)
 
 
-def debug(msg: str, dedupe: bool = False, **kwargs):
+def debug(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print a debug message.
 
     Args:
@@ -176,7 +176,7 @@ def debug(msg: str, dedupe: bool = False, **kwargs):
         print_to_log_file(f""[purple]Debug: {msg}[/purple]"", **kwargs)
 
 
-def info(msg: str, dedupe: bool = False, **kwargs):
+def info(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print an info message.
 
     Args:
@@ -194,7 +194,7 @@ def info(msg: str, dedupe: bool = False, **kwargs):
         print_to_log_file(f""[cyan]Info: {msg}[/cyan]"", **kwargs)
 
 
-def success(msg: str, dedupe: bool = False, **kwargs):
+def success(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print a success message.
 
     Args:
@@ -212,7 +212,7 @@ def success(msg: str, dedupe: bool = False, **kwargs):
         print_to_log_file(f""[green]Success: {msg}[/green]"", **kwargs)
 
 
-def log(msg: str, dedupe: bool = False, **kwargs):
+def log(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Takes a string and logs it to the console.
 
     Args:
@@ -240,7 +240,7 @@ def rule(title: str, **kwargs):
     _console.rule(title, **kwargs)
 
 
-def warn(msg: str, dedupe: bool = False, **kwargs):
+def warn(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print a warning message.
 
     Args:
@@ -327,7 +327,7 @@ def deprecate(
             _EMITTED_DEPRECATION_WARNINGS.add(dedupe_key)
 
 
-def error(msg: str, dedupe: bool = False, **kwargs):
+def error(msg: str, *, dedupe: bool = False, **kwargs):
     """"""Print an error message.
 
     Args: