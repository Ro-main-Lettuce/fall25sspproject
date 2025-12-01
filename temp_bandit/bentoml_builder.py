@@ -12,6 +12,7 @@
 from ...exceptions import BentoMLException
 from ...grpc.utils import LATEST_PROTOCOL_VERSION
 from ..configuration import is_editable_bentoml
+from ..utils.pkg import ensure_uv
 from ..utils.pkg import source_locations
 
 if sys.version_info >= (3, 11):
@@ -157,7 +158,7 @@ def build_git_repo(url: str, ref: str, subdirectory: str | None, dst_path: str)
                 f""Failed to clone git repository {url}: {e.stderr}""
             ) from e
         source_dir = os.path.join(dest_dir, subdirectory) if subdirectory else dest_dir
-        build_cmd = [sys.executable, ""-m"", ""uv"", ""build"", ""--sdist""]
+        build_cmd = [sys.executable, ""-m"", ensure_uv(), ""build"", ""--sdist""]
         subprocess.check_call(build_cmd, cwd=source_dir)
         sdist = next(Path(source_dir).glob(""dist/*.tar.gz""))
         logger.info(f""Built sdist {sdist.name}"")