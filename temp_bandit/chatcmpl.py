@@ -157,6 +157,9 @@ async def invoke_embedding(
             'input': input_text,
         }
 
+        if model.model_entity.extra_args:
+            args.update(model.model_entity.extra_args)
+
         args.update(extra_args)
 
         try: