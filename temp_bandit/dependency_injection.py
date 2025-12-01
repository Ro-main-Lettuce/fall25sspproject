@@ -12,7 +12,7 @@
 from fast_depends import inject
 from fast_depends.dependencies import model
 
-from autogen.agentchat import Agent
+from ..agentchat import Agent
 
 if TYPE_CHECKING:
     from ..agentchat.conversable_agent import ConversableAgent
@@ -157,11 +157,19 @@ def _string_metadata_to_description_field(func: Callable[..., Any]) -> Callable[
     type_hints = get_type_hints(func, include_extras=True)
 
     for _, annotation in type_hints.items():
+        # Check if the annotation itself has metadata (using __metadata__)
         if hasattr(annotation, ""__metadata__""):
             metadata = annotation.__metadata__
             if metadata and isinstance(metadata[0], str):
-                # Replace string metadata with DescriptionField
+                # Replace string metadata with Field
                 annotation.__metadata__ = (Field(description=metadata[0]),)
+        # For Python < 3.11, annotations like `Optional` are stored as `Union`, so metadata
+        # would be in the first element of __args__ (e.g., `__args__[0]` for `int` in `Optional[int]`)
+        elif hasattr(annotation, ""__args__"") and hasattr(annotation.__args__[0], ""__metadata__""):
+            metadata = annotation.__args__[0].__metadata__
+            if metadata and isinstance(metadata[0], str):
+                # Replace string metadata with Field
+                annotation.__args__[0].__metadata__ = (Field(description=metadata[0]),)
     return func
 
 