@@ -2,7 +2,7 @@
 
 from __future__ import annotations
 
-from typing import TypedDict
+from typing import Any, TypedDict
 
 from reflex.components.component import NoSSRComponent
 from reflex.event import EventHandler, no_args_event_spec, passthrough_event_spec
@@ -50,12 +50,6 @@ class ReactPlayer(NoSSRComponent):
     # Mutes the player
     muted: Var[bool]
 
-    # Set the width of the player: ex:640px
-    width: Var[str]
-
-    # Set the height of the player: ex:640px
-    height: Var[str]
-
     # Called when media is loaded and ready to play. If playing is set to true, media will play immediately.
     on_ready: EventHandler[no_args_event_spec]
 
@@ -103,3 +97,23 @@ class ReactPlayer(NoSSRComponent):
 
     # Called when picture-in-picture mode is disabled.
     on_disable_pip: EventHandler[no_args_event_spec]
+
+    def _render(self, props: dict[str, Any] | None = None):
+        """"""Render the component. Adds width and height set to None because
+        react-player will set them to some random value that overrides the
+        css width and height.
+
+        Args:
+            props: The props to pass to the component.
+
+        Returns:
+            The rendered component.
+        """"""
+        return (
+            super()
+            ._render(props)
+            .add_props(
+                width=Var.create(None),
+                height=Var.create(None),
+            )
+        )