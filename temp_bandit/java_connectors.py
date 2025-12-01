@@ -21,7 +21,7 @@ class BuildConnectorDistributionTar(GradleTask):
     """"""
 
     @property
-    def title(self) -> str:
+    def title(self: ""BuildConnectorDistributionTar"") -> str:
         return ""Build connector tar""
     
     gradle_task_name = ""distTar""
@@ -32,7 +32,7 @@ class BuildConnectorImages(BuildConnectorImagesBase):
     A step to build Java connector images using the distTar Gradle task.
     """"""
 
-    async def _run(self, dist_dir_path: str) -> StepResult:
+    async def _run(self: ""BuildConnectorImages"", dist_dir_path: str) -> StepResult:
         try:
             dist_path = Path(dist_dir_path)
             tar_files = list(dist_path.glob(""*.tar""))
@@ -49,7 +49,7 @@ async def _run(self, dist_dir_path: str) -> StepResult:
             return StepResult(step=self, status=StepStatus.FAILURE, stderr=str(e))
         return await super()._run(dist_tar_path)
 
-    async def _build_connector(self, platform: ""dagger.Platform"", dist_tar_path: str) -> ""dagger.Container"":
+    async def _build_connector(self: ""BuildConnectorImages"", platform: ""dagger.Platform"", dist_tar_path: str) -> ""dagger.Container"":
         """"""
         Build a Java connector image using Dagger.
         """"""