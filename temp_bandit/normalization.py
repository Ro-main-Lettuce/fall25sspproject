@@ -16,7 +16,7 @@ class BuildOrPullNormalization(Step):
 
     context: ConnectorContext
 
-    def __init__(self, context: ConnectorContext, normalization_image: str, build_platform: Platform) -> None:
+    def __init__(self: ""BuildOrPullNormalization"", context: ConnectorContext, normalization_image: str, build_platform: Platform) -> None:
         """"""Initialize the step to build or pull the normalization image.
 
         Args:
@@ -29,10 +29,10 @@ def __init__(self, context: ConnectorContext, normalization_image: str, build_pl
         self.normalization_image = normalization_image
 
     @property
-    def title(self) -> str:
+    def title(self: ""BuildOrPullNormalization"") -> str:
         return f""Build {self.normalization_image}"" if self.use_dev_normalization else f""Pull {self.normalization_image}""
 
-    async def _run(self) -> StepResult:
+    async def _run(self: ""BuildOrPullNormalization"") -> StepResult:
         if self.use_dev_normalization:
             build_normalization_container = normalization.with_normalization(self.context, self.build_platform)
         else: