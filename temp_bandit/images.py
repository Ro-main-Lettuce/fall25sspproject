@@ -7,8 +7,11 @@
 import sys
 import typing as t
 from pathlib import Path
+from typing import cast
 
 import attrs
+from pip_requirements_parser import RequirementsFile  # type: ignore
+from pip_requirements_parser.requirement import InstallRequirement  # type: ignore
 
 from bentoml._internal.bento.bento import ImageInfo
 from bentoml._internal.bento.build_config import BentoBuildConfig
@@ -18,10 +21,14 @@
 from bentoml._internal.configuration import get_quiet_mode
 from bentoml._internal.container.frontend.dockerfile import CONTAINER_METADATA
 from bentoml._internal.container.frontend.dockerfile import CONTAINER_SUPPORTED_DISTROS
+from bentoml._internal.utils.pkg import ensure_uv
 from bentoml._internal.utils.pkg import get_local_bentoml_dependency
 from bentoml.exceptions import BentoMLConfigException
 from bentoml.exceptions import BentoMLException
 
+# Type hints for pip_requirements_parser
+RequirementsList = list[InstallRequirement]
+
 if sys.version_info >= (3, 11):
     import tomllib
 else:
@@ -32,18 +39,18 @@
 DEFAULT_PYTHON_VERSION = f""{sys.version_info.major}.{sys.version_info.minor}""
 
 
-@attrs.define
+@attrs.define(slots=True)  # type: ignore
 class Image:
     """"""A class defining the environment requirements for bento.""""""
 
     base_image: str
     python_version: str = DEFAULT_PYTHON_VERSION
-    commands: t.List[str] = attrs.field(factory=list)
+    commands: list[str] = attrs.field(factory=list, init=False)  # type: ignore
     lock_python_packages: bool = True
     python_requirements: str = """"
-    post_commands: t.List[str] = attrs.field(factory=list)
-    scripts: t.Dict[str, str] = attrs.field(factory=dict, init=False)
-    _after_pip_install: bool = attrs.field(init=False, default=False, repr=False)
+    post_commands: list[str] = attrs.field(factory=list, init=False)  # type: ignore
+    scripts: dict[str, str] = attrs.field(factory=dict, init=False)  # type: ignore
+    _after_pip_install: bool = attrs.field(init=False, default=False)  # type: ignore
 
     def requirements_file(self, file_path: str) -> t.Self:
         """"""Add a requirements file to the image. Supports chaining call.
@@ -137,19 +144,19 @@ def freeze(self, platform_: str | None = None) -> ImageInfo:
     def _freeze_python_requirements(self, platform_: str | None = None) -> str:
         from tempfile import TemporaryDirectory
 
-        from pip_requirements_parser import RequirementsFile
-
         with TemporaryDirectory(prefix=""bento-reqs-"") as parent:
             requirements_in = Path(parent).joinpath(""requirements.in"")
             requirements_in.write_text(self.python_requirements)
             # XXX: RequirementsFile.from_string() does not work due to bugs
-            requirements_file = RequirementsFile.from_file(str(requirements_in))
+            reqs: RequirementsFile = RequirementsFile.from_file(str(requirements_in))  # type: ignore
             has_bentoml_req = any(
-                req.name and req.name.lower() == ""bentoml"" and req.link is not None
-                for req in requirements_file.requirements
+                cast(InstallRequirement, req).name
+                and cast(InstallRequirement, req).name.lower() == ""bentoml""
+                and cast(InstallRequirement, req).link is not None
+                for req in cast(list[InstallRequirement], reqs.requirements)  # type: ignore
             )
             with requirements_in.open(""w"") as f:
-                f.write(requirements_file.dumps(preserve_one_empty_line=True))
+                f.write(cast(str, reqs.dumps(preserve_one_empty_line=True)))
                 if not has_bentoml_req:
                     req = get_bentoml_requirement() or get_local_bentoml_dependency()
                     f.write(f""{req}
"")
@@ -177,7 +184,7 @@ def _freeze_python_requirements(self, platform_: str | None = None) -> str:
                     DEFAULT_LOCK_PLATFORM,
                 )
                 lock_args.extend([""--python-platform"", DEFAULT_LOCK_PLATFORM])
-            cmd = [sys.executable, ""-m"", ""uv"", ""pip"", ""compile"", *lock_args]
+            cmd = [sys.executable, ""-m"", ensure_uv(), ""pip"", ""compile"", *lock_args]
             try:
                 subprocess.check_call(
                     cmd,
@@ -190,11 +197,11 @@ def _freeze_python_requirements(self, platform_: str | None = None) -> str:
             return requirements_in.with_suffix("".lock"").read_text()
 
 
-@attrs.define
+@attrs.define(slots=True)  # type: ignore
 class PythonImage(Image):
     base_image: str = """"
     distro: str = ""debian""
-    _original_base_image: str = attrs.field(init=False, default="""")
+    _original_base_image: str = attrs.field(init=False, default="""")  # type: ignore
 
     def __attrs_post_init__(self) -> None:
         self._original_base_image = self.base_image