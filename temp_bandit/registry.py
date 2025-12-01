@@ -134,7 +134,7 @@ def get_cell(self, object_id: UIElementId) -> CellId_t:
 
     def resolve_lens(
         self, object_id: UIElementId, value: LensValue[T]
-    ) -> tuple[str, LensValue[T]]:
+    ) -> tuple[UIElementId, LensValue[T]]:
         """"""Resolve a lens, if any, to an object id and value update
 
         Returns (resolved object id, resolved value)