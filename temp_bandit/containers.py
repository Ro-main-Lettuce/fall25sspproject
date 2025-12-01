@@ -11,7 +11,6 @@
 
 import schema as s
 import yaml
-from deepmerge.merger import Merger
 from simple_di import Provide
 from simple_di import providers
 
@@ -21,6 +20,7 @@
 from ..resource import CpuResource
 from ..utils import split_with_quotes
 from ..utils.filesystem import validate_or_create_dir
+from ..utils.merge import deep_merge
 from ..utils.unflatten import unflatten
 from . import expand_env_var
 from . import load_config
@@ -43,14 +43,9 @@
 
     SerializationStrategy = t.Literal[""EXPORT_BENTO"", ""LOCAL_BENTO"", ""REMOTE_BENTO""]
 
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
 
 logger = logging.getLogger(__name__)
 