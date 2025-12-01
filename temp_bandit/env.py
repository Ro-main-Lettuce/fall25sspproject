@@ -15,6 +15,7 @@
 import rich.pretty
 
 from bentoml._internal.utils.pkg import PackageNotFoundError
+from bentoml._internal.utils.pkg import ensure_uv
 from bentoml._internal.utils.pkg import get_pkg_version
 from bentoml.exceptions import CLIException
 
@@ -133,10 +134,10 @@ def env_command(ctx: click.Context, output: t.Literal[""md"", ""bash""]) -> None:  #
     }
 
     if is_windows:
-        from ctypes import windll
+        from ctypes import windll  # type: ignore
 
         # https://stackoverflow.com/a/1026626
-        is_admin: bool = windll.shell32.IsUserAnAdmin() != 0
+        is_admin: bool = bool(windll.shell32.IsUserAnAdmin())  # type: ignore
         info_dict[""is_window_admin""] = str(is_admin)
     else:
         info_dict[""uid_gid""] = f""{os.geteuid()}:{os.getegid()}""
@@ -165,6 +166,6 @@ def env_command(ctx: click.Context, output: t.Literal[""md"", ""bash""]) -> None:  #
         info_dict[""conda_packages""] = conda_packages
 
     # process info from `pip freeze`
-    pip_packages = run_cmd([sys.executable, ""-m"", ""uv"", ""pip"", ""freeze""])
+    pip_packages = run_cmd([sys.executable, ""-m"", ensure_uv(), ""pip"", ""freeze""])
     info_dict[""pip_packages""] = pip_packages
     rich.print(pretty_format(info_dict, output=output))