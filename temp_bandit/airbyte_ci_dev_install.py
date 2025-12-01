@@ -22,9 +22,9 @@ def check_command_exists(command: str, not_found_message: str) -> None:
 def main() -> None:
     # Check if Python 3.10 is on the path
     check_command_exists(
-        ""python3.10"",
+        ""python3.11"",
         """"""python3.10 not found on the path.
-Please install Python 3.10 using pyenv:
+Please install Python 3.11 using pyenv:
 1. Install pyenv if not already installed:
    brew install pyenv
 2. Install Python 3.10 using pyenv:
@@ -34,21 +34,17 @@ def main() -> None:
 
     # Check if pipx is installed
     check_command_exists(
-        ""pipx"",
-        """"""pipx not found. Please install pipx:
-1. Ensure Python 3.6 or later is installed.
-2. Install pipx using Python:
-   python3 -m pip install --user pipx
-3. Add pipx to your PATH:
-   python3 -m pipx ensurepath
+        ""uv"",
+        """"""uv not found. Please install uv: `brew install uv`
+
 After installation, restart your terminal or source your shell
-configuration file to ensure the pipx command is available."""""",
+configuration file to ensure the uv command is available."""""",
     )
-    print(""pipx is already installed."")
+    print(""uv is already installed."")
 
     # Install airbyte-ci development version
-    subprocess.run([""pipx"", ""install"", ""--editable"", ""--force"", ""--python=python3.11"", ""airbyte-ci/connectors/pipelines/""])
-    print(""Development version of airbyte-ci installed....."")
+    subprocess.run([""uv"", ""tool"", ""install"", ""--editable"", ""--force"", ""--python=python3.11"", ""airbyte-ci/connectors/pipelines/""])
+    print(""Development version of airbyte-ci installed successfully."")
 
 
 if __name__ == ""__main__"":