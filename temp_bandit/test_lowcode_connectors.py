@@ -2,6 +2,7 @@
 from __future__ import annotations
 
 from pathlib import Path
+import sys
 
 import pytest
 from airbyte import get_source
@@ -17,6 +18,10 @@
     ],
 )
 @pytest.mark.xfail(condition=is_windows(), reason=""Test expected to fail on Windows."")
+@pytest.mark.skipif(
+    sys.version_info >= (3, 12),
+    reason=""Test fails in Python 3.12 as pokeAPI interface is blocked for bots/CI runners"",
+)
 def test_nocode_execution(connector_name: str, config: dict) -> None:
     source = get_source(
         name=connector_name,