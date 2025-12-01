@@ -24,7 +24,10 @@ def accepts_mime_type(mime_type: KnownMimeType) -> KnownMimeType:
 
         # The following would fail type checking but not at runtime
         # This test is just to verify the runtime behavior
-        assert accepts_mime_type(cast(KnownMimeType, ""unknown/type"")) == ""unknown/type""
+        assert (
+            accepts_mime_type(cast(KnownMimeType, ""unknown/type""))
+            == ""unknown/type""
+        )
 
     def test_mime_bundle(self) -> None:
         # Test that MimeBundle can be used as a type annotation
@@ -46,7 +49,7 @@ def accepts_mime_bundle(bundle: MimeBundle) -> MimeBundle:
     def test_mime_bundle_or_tuple(self) -> None:
         # Test that MimeBundleOrTuple can be used as a type annotation
         def accepts_mime_bundle_or_tuple(
-            bundle_or_tuple: MimeBundleOrTuple
+            bundle_or_tuple: MimeBundleOrTuple,
         ) -> MimeBundleOrTuple:
             return bundle_or_tuple
 