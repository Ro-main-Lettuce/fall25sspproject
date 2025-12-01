@@ -113,6 +113,10 @@ class Config:
     sl: Optional[Literal[0, 100, 200, 300]] = None
     ql: Optional[Literal[0, 100, 200, 300, 400, 500, 600]] = None
     isEnterprise: Optional[bool] = False
+    requireVersionIncrementsInPullRequests: Optional[bool] = Field(
+        True,
+        description=""When false, version increment checks will be skipped for this connector"",
+    )
 
 
 class GitInfo(BaseModel):