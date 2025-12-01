@@ -6,8 +6,12 @@
 
 from crewai.utilities.logger import Logger
 
+""""""Controls request rate limiting for API calls.""""""
+
 
 class RPMController(BaseModel):
+    """"""Manages requests per minute limiting.""""""
+
     max_rpm: Optional[int] = Field(default=None)
     logger: Logger = Field(default_factory=lambda: Logger(verbose=False))
     _current_rpm: int = PrivateAttr(default=0)