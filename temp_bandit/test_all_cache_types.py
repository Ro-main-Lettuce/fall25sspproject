@@ -13,15 +13,16 @@
 import sys
 from pathlib import Path
 
-import airbyte as ab
 import pytest
-from airbyte import get_source
-from airbyte._util.venv_util import get_bin_dir
 from sqlalchemy import text
 from viztracer import VizTracer
 
+import airbyte as ab
+from airbyte import get_source
+from airbyte._util.venv_util import get_bin_dir
 from airbyte.results import ReadResult
 
+
 # Product count is always the same, regardless of faker scale.
 NUM_PRODUCTS = 100
 
@@ -140,7 +141,7 @@ def test_faker_read(
         read_result = source_faker_seed_a.read(
             new_generic_cache, write_strategy=""replace"", force_full_refresh=True
         )
-    configured_count = source_faker_seed_a._config[""count""]
+    configured_count = source_faker_seed_a.get_config()[""count""]
 
     # Check row counts match:
     assert len(list(read_result.cache.streams[""users""])) == FAKER_SCALE_A