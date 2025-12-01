@@ -1,7 +1,5 @@
-from codegen.sdk.code_generation.types import ContextMock
 import json
 import logging
-from dataclasses import dataclass
 from pathlib import Path
 
 from git import Repo
@@ -12,6 +10,7 @@
 from semantic_release.cli.config import GlobalCommandLineOptions
 
 import codegen
+from codegen.sdk.code_generation.types import ContextMock
 
 logger = logging.getLogger(__name__)
 