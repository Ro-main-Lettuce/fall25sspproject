@@ -12,8 +12,6 @@
 
 from rich.console import Console
 from rich.live import Live
-from rich.panel import Panel
-from rich.progress import ProgressBar
 from rich.spinner import Spinner
 from rich.text import Text
 
@@ -29,6 +27,7 @@ class InstallationStage(Enum):
     COMPLETE = (""Installation complete!"", 1.0)
 
     def __init__(self, message: str, progress: float):
+        """"""Initialize the InstallationStage with a message and progress.""""""
         self.message = message
         self.progress = progress
 
@@ -52,7 +51,7 @@ def create_progress_bar(self, completed: float = 0) -> Text:
         bar.append(""█"" * filled, style=""green"")
         bar.append(""▒"" * (width - filled), style=""dim white"")
         bar.append("" │"", style=""dim white"")
-        bar.append(f""
╰"", style=""dim white"")
+        bar.append(""
╰"", style=""dim white"")
         bar.append(""─"" * (width + 2), style=""dim white"")
         bar.append(""╯"", style=""dim white"")
         return bar
@@ -74,9 +73,7 @@ def create_success_text(self) -> Text:
         """"""Create the success message with links.""""""
         text = Text()
         text.append(""✨ Curator installed successfully!

"", style=""bold green"")
-        text.append(
-            ""Start building production-ready synthetic data pipelines:

"", style=""dim white""
-        )
+        text.append(""Start building production-ready synthetic data pipelines:

"", style=""dim white"")
         text.append(""   📚 "", style="""")
         text.append(""docs.bespokelabs.ai"", style=""dim cyan link https://docs.bespokelabs.ai"")
         text.append(""
   📦 "", style="""")
@@ -85,16 +82,20 @@ def create_success_text(self) -> Text:
             style=""dim cyan link https://github.com/bespokelabsai/curator"",
         )
         text.append(""
   💬 "", style="""")
-        text.append(
-            ""discord.gg/KqpXvpzVBS"", style=""dim cyan link https://discord.com/invite/KqpXvpzVBS""
-        )
+        text.append(""discord.gg/KqpXvpzVBS"", style=""dim cyan link https://discord.com/invite/KqpXvpzVBS"")
         return text
 
 
 class PackageInstaller:
     """"""Class to handle the package installation process.""""""
 
     def __init__(self, package_name: str, version: Optional[str] = None):
+        """"""Initialize the PackageInstaller with the package name and optional version.
+
+        Args:
+            package_name: The name of the package to install
+            version: Optional specific version to install
+        """"""
         self.package_spec = f""{package_name}=={version}"" if version else package_name
         self.ui = InstallationUI(package_name)
 
@@ -121,7 +122,7 @@ def parse_pip_output(self, line: str) -> Tuple[InstallationStage, float]:
                     percent = float(line.split(""%"")[0].split()[-1])
                     # Scale download progress between 20% and 60%
                     return InstallationStage.DOWNLOADING, 0.2 + (percent / 100.0 * 0.4)
-                except:
+                except Exception:
                     pass
             return InstallationStage.DOWNLOADING, InstallationStage.DOWNLOADING.progress
         elif ""installing"" in line:
@@ -133,9 +134,7 @@ def parse_pip_output(self, line: str) -> Tuple[InstallationStage, float]:
 
     def install(self) -> None:
         """"""Execute the installation with progress tracking and UI updates.""""""
-        spinner = Spinner(
-            ""dots2"", text=self.ui.create_loading_text(InstallationStage.PREPARING, 0), style=""green""
-        )
+        spinner = Spinner(""dots2"", text=self.ui.create_loading_text(InstallationStage.PREPARING, 0), style=""green"")
 
         with Live(spinner, console=self.ui.console, refresh_per_second=30) as live:
             try:
@@ -169,8 +168,7 @@ def install(self) -> None:
 
 
 def enhanced_install(package_name: str, version: Optional[str] = None) -> None:
-    """"""
-    Enhance pip installation with a professional progress UI.
+    """"""Enhance pip installation with a professional progress UI.
 
     Args:
         package_name: Name of the package to install