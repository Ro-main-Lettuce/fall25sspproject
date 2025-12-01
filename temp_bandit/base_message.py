@@ -73,6 +73,14 @@ def print(self, f: Optional[Callable[..., Any]] = None) -> None:
 
     wrapper_cls = create_model(message_cls.__name__, __base__=WrapperBase)
 
+    # Preserve the original class's docstring and other attributes
+    wrapper_cls.__doc__ = message_cls.__doc__
+    wrapper_cls.__module__ = message_cls.__module__
+
+    # Copy any other relevant attributes/metadata from the original class
+    if hasattr(message_cls, ""__annotations__""):
+        wrapper_cls.__annotations__ = message_cls.__annotations__
+
     _message_classes[type_name] = wrapper_cls
 
     return wrapper_cls