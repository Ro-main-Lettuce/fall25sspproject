@@ -10,11 +10,11 @@ class Logger(BaseModel):
     _printer: Printer = PrivateAttr(default_factory=Printer)
     default_color: str = Field(default=""bold_yellow"")
 
-    def log(self, level, message, color=None):
+    def log(self, level, message, color=None) -> None:
         if color is None:
             color = self.default_color
         if self.verbose:
             timestamp = datetime.now().strftime(""%Y-%m-%d %H:%M:%S"")
             self._printer.print(
-                f""
[{timestamp}][{level.upper()}]: {message}"", color=color
+                f""
[{timestamp}][{level.upper()}]: {message}"", color=color,
             )