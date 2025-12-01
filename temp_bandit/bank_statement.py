@@ -5,10 +5,10 @@
 
 
 class Address(BaseModel):
-    street: str = Field(..., description=""Street address"")
-    city: str = Field(..., description=""City"")
-    state: str = Field(..., description=""State/Province code or name"")
-    zip_code: str = Field(..., description=""Postal code"", min_length=5, max_length=10)
+    street: str | None = Field(None, description=""Street address"")
+    city: str | None = Field(None, description=""City"")
+    state: str | None = Field(None, description=""State/Province code or name"")
+    zip_code: str | None = Field(None, description=""Postal code"", min_length=2, max_length=10)
 
 
 class BankTransaction(BaseModel):