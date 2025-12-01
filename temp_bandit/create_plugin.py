@@ -1,9 +1,7 @@
 #!/usr/bin/env python3
 
-import os
 import argparse
 from pathlib import Path
-from typing import Optional
 
 def create_project_toml(plugin_dir: Path, plugin_name: str, is_evm: bool, is_solana: bool = False) -> None:
     """"""Create the pyproject.toml file for the plugin.""""""
@@ -108,8 +106,28 @@ class ExampleActionParameters(BaseModel):
     with open(goat_plugins_dir / ""parameters.py"", ""w"") as f:
         f.write(parameters_content)
 
+def convert_to_python_identifier(name: str, for_class: bool = False) -> str:
+    """"""Convert a kebab-case name to a valid Python identifier.
+    
+    Args:
+        name: The name to convert
+        for_class: If True, convert to PascalCase for class names,
+                  otherwise convert to snake_case for function/variable names
+    """"""
+    # First convert to snake_case
+    snake_case = name.replace(""-"", ""_"")
+    
+    if for_class:
+        # Convert to PascalCase for class names
+        return """".join(word.title() for word in snake_case.split(""_""))
+    
+    return snake_case
+
 def create_service_file(goat_plugins_dir: Path, plugin_name: str, is_evm: bool, is_solana: bool = False) -> None:
     """"""Create the service.py file with an empty tool.""""""
+    # Convert plugin name to valid Python identifier for class name
+    class_name = f""{convert_to_python_identifier(plugin_name, for_class=True)}Service""
+    
     # Start with common imports
     service_content = '''from goat.decorators.tool import Tool
 from .parameters import ExampleQueryParameters, ExampleActionParameters
@@ -124,9 +142,6 @@ def create_service_file(goat_plugins_dir: Path, plugin_name: str, is_evm: bool,
         service_content += '''from goat_wallets.solana import SolanaWalletClient
 
 '''
-
-    # Create the service class
-    class_name = f""{plugin_name.title()}Service""
     service_content += f'''
 class {class_name}:
     def __init__(self, api_key: str):
@@ -172,8 +187,9 @@ async def example_action(self{"", wallet_client: EVMWalletClient"" if is_evm else
 
 def create_init_file(goat_plugins_dir: Path, plugin_name: str, is_evm: bool, is_solana: bool = False) -> None:
     """"""Create the __init__.py file with plugin class.""""""
-    # Convert hyphens to underscores for class names
-    class_base = plugin_name.replace(""-"", ""_"").title()
+    # Convert plugin name to valid Python identifiers
+    python_name = convert_to_python_identifier(plugin_name)
+    class_base = convert_to_python_identifier(plugin_name, for_class=True)
     class_name = f""{class_base}Service""
     plugin_class = f""{class_base}Plugin""
     options_class = f""{class_base}PluginOptions""
@@ -197,13 +213,14 @@ def supports_chain(self, chain) -> bool:
         return {supports_chain}
 
 
-def {plugin_name}(options: {options_class}) -> {plugin_class}:
+def {python_name}(options: {options_class}) -> {plugin_class}:
     return {plugin_class}(options)
 '''.format(
         class_name=class_name,
         plugin_class=plugin_class,
         options_class=options_class,
         plugin_name=plugin_name,
+        python_name=python_name,
         supports_chain=""chain['type'] == 'evm'"" if is_evm else ""chain['type'] == 'solana'"" if is_solana else ""True""
     )
 
@@ -246,6 +263,10 @@ def main():
     is_evm = args.evm
     is_solana = args.solana
     
+    # Convert plugin name to valid Python identifiers (used throughout the script)
+    python_name = convert_to_python_identifier(plugin_name)
+    class_base = convert_to_python_identifier(plugin_name, for_class=True)
+    
     # Create base plugin directory (relative to python root)
     plugin_dir = Path(__file__).parent.parent / ""src"" / ""plugins"" / plugin_name
     plugin_dir.mkdir(parents=True, exist_ok=True)
@@ -263,6 +284,9 @@ def main():
     create_init_file(goat_plugins_dir, plugin_name, is_evm, is_solana)
     
     # Create README.md
+    # Convert plugin name for Python usage
+    python_name = convert_to_python_identifier(plugin_name)
+    
     # Determine chain support text
     chain_support = 'EVM chain support' if is_evm else 'Solana chain support' if is_solana else 'Chain-agnostic support'
     
@@ -289,13 +313,13 @@ def main():
 ## Usage
 
 ```python
-from goat_plugins.{plugin_name} import {plugin_name}, {plugin_name.title()}PluginOptions
+from goat_plugins.{plugin_name} import {python_name}, {class_base}PluginOptions
 
 # Initialize the plugin
-options = {plugin_name.title()}PluginOptions(
+options = {class_base}PluginOptions(
     api_key=""your-api-key""
 )
-plugin = {plugin_name}(options)
+plugin = {python_name}(options)
 ```
 
 ## Features