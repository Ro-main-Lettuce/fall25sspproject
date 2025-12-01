@@ -15,7 +15,6 @@
 import fs
 import rich
 import yaml
-from deepmerge.merger import Merger
 from pathspec import PathSpec
 from rich.console import Console
 from simple_di import Provide
@@ -25,6 +24,7 @@
 from ..bento.bento import Bento
 from ..bento.build_config import BentoBuildConfig
 from ..configuration import is_editable_bentoml
+from ..utils.merge import deep_merge
 from ..utils.pkg import source_locations
 
 if t.TYPE_CHECKING:
@@ -57,14 +57,9 @@
 
 logger = logging.getLogger(__name__)
 
-config_merger = Merger(
-    # merge dicts
-    type_strategies=[(dict, ""merge"")],
-    # override all other types
-    fallback_strategies=[""override""],
-    # override conflicting types
-    type_conflict_strategies=[""override""],
-)
+config_merger = {
+    ""merge"": deep_merge,
+}
 
 
 @attr.define