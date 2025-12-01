@@ -156,7 +156,7 @@ async def new_create_async(
         context = handle_context(context, validation_context)
 
         response_model, new_kwargs = handle_response_model(
-            response_model=response_model, mode=mode, **kwargs
+            response_model=response_model, mode=mode, context=context, **kwargs
         )  # type: ignore
         new_kwargs = handle_templating(new_kwargs, mode=mode, context=context)
 
@@ -187,7 +187,7 @@ def new_create_sync(
         context = handle_context(context, validation_context)
         # print(f""instructor.patch: patched_function {func.__name__}"")
         response_model, new_kwargs = handle_response_model(
-            response_model=response_model, mode=mode, **kwargs
+            response_model=response_model, mode=mode, context=context, **kwargs
         )  # type: ignore
 
         new_kwargs = handle_templating(new_kwargs, mode=mode, context=context)