@@ -1,4 +1,17 @@
 # Copyright (c) 2023 Airbyte, Inc., all rights reserved.
+""""""Java connector executor with automatic JRE management.
+
+This module provides the JavaExecutor class for running Java-based Airbyte connectors.
+It automatically downloads and manages Zulu JRE installations in ~/.airbyte/java directory
+and handles connector tar file extraction and execution.
+
+Fallback Logic:
+- When use_java_tar=False: Java execution is explicitly disabled, fallback to Docker
+- When use_java_tar=None and Docker available: Use Docker as the more stable option
+- When use_java_tar=None and Docker unavailable: Use Java with automatic JRE download
+- When use_java_tar is truthy: Use Java executor with specified or auto-detected tar file
+""""""
+
 from __future__ import annotations
 
 import os