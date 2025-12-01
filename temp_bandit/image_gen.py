@@ -10,22 +10,30 @@ class ImageGenState(rx.State):
     image_url: str = """"
     processing: bool = False
 
-    @rx.event
-    def get_image(self, form_data):
+    @rx.event(background=True)
+    async def get_image(self, form_data):
         """"""Get the image from the prompt.""""""
         prompt = form_data[""prompt""]
         if prompt == """":
             return
-        self.processing = True
-        yield
+        async with self:
+            self.processing = True
+            yield
         input = {""prompt"": prompt}
 
-        output = replicate.run(
-            ""black-forest-labs/flux-schnell"",
-            input=input,
-        )
-        self.image_url = str(output[0])
-        self.processing = False
+        try:
+            output = await replicate.async_run(
+                ""black-forest-labs/flux-schnell"",
+                input=input,
+            )
+            async with self:
+                self.image_url = str(output[0])
+        except Exception:
+            async with self:
+                self.image_url = """"
+        finally:
+            async with self:
+                self.processing = False
 
 
 def image_gen() -> rx.Component: