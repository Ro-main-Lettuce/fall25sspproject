@@ -27,6 +27,9 @@ class W2Form(BaseModel):
     wages_tips_other_compensation: float | None = Field(
         None, description=""Wages, tips, and other compensation (Box 1)""
     )
+    federal_income_tax_withheld: float | None = Field(
+        None, description=""Federal income tax withheld (Box 2)""
+    )
     social_security_wages: float | None = Field(
         None, description=""Social security wages (Box 3)""
     )
@@ -39,8 +42,5 @@ class W2Form(BaseModel):
     medicare_tax_withheld: float | None = Field(
         None, description=""Medicare tax withheld (Box 6)""
     )
-    federal_income_tax_withheld: float | None = Field(
-        None, description=""Federal income tax withheld (Box 2)""
-    )
 
     tax_year: int | None = Field(None, description=""Tax year for which the W2 form is issued"")