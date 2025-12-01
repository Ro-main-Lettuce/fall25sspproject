@@ -1,18 +1,17 @@
-from codegen.sdk.typescript.external.types import PackageJsonData
 import concurrent.futures
 import json
 import logging
 import os
 import shutil
 import subprocess
 import uuid
-from dataclasses import dataclass
 from enum import Enum
 
 import pyjson5
 import requests
 
 from codegen.sdk.core.external.dependency_manager import DependencyManager
+from codegen.sdk.typescript.external.types import PackageJsonData
 from codegen.sdk.utils import shadow_files
 
 logger = logging.getLogger(__name__)