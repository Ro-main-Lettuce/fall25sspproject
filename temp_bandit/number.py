@@ -289,13 +289,13 @@ def __rpow__(self, other: number_types) -> NumberVar:
 
         return number_exponent_operation(+other, self)
 
-    def __neg__(self):
+    def __neg__(self) -> NumberVar:
         """"""Negate the number.
 
         Returns:
             The number negation operation.
         """"""
-        return number_negate_operation(self)
+        return number_negate_operation(self)  # pyright: ignore [reportReturnType]
 
     def __invert__(self):
         """"""Boolean NOT the number.