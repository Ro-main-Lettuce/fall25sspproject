@@ -9,7 +9,7 @@
 from connector_ops.utils import Connector  # type: ignore
 
 from pipelines import main_logger
-from pipelines.helpers.utils import IGNORED_FILE_EXTENSIONS, METADATA_FILE_NAME
+from pipelines.helpers.utils import IGNORED_FILE_EXTENSIONS, IGNORED_FILE_NAMES, METADATA_FILE_NAME
 
 
 def get_connector_modified_files(connector: Connector, all_modified_files: Set[Path]) -> FrozenSet[Path]:
@@ -52,7 +52,7 @@ def _is_connector_modified_indirectly(connector: Connector, modified_files: Set[
 
 def _is_ignored_file(file_path: Union[str, Path]) -> bool:
     """"""Check if the provided file has an ignored extension.""""""
-    return Path(file_path).suffix in IGNORED_FILE_EXTENSIONS
+    return Path(file_path).suffix in IGNORED_FILE_EXTENSIONS or Path(file_path).name in IGNORED_FILE_NAMES
 
 
 def get_modified_connectors(modified_files: Set[Path], all_connectors: Set[Connector], dependency_scanning: bool) -> Set[Connector]: