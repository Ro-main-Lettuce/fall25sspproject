@@ -37,11 +37,8 @@ class Kura:
     summarization, embedding, clustering, meta-clustering, and visualization.
     This class coordinates the entire pipeline and manages checkpointing.
 
-    For cleaner output without progress bars:
-        kura = Kura(disable_progress=True)
-
-    Or to disable Rich console entirely:
-        kura = Kura(console=None)
+    Note: This class-based approach is deprecated.
+    Please use the procedural API functions instead.
 
     Attributes:
         embedding_model: Model for converting text to vector embeddings
@@ -86,6 +83,13 @@ def __init__(
             dimensionality reduction) are now defined as properties in their respective base classes
             rather than constructor arguments.
         """"""
+        from warnings import warn
+
+        warn(
+            ""Kura is deprecated. Please use the procedural API functions instead."",
+            DeprecationWarning,
+        )
+
         # Initialize Rich console if available and not provided
         if console is None and RICH_AVAILABLE and not disable_progress and Console:
             self.console = Console()