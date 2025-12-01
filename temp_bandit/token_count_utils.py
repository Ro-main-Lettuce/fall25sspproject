@@ -11,17 +11,20 @@
 
 import tiktoken
 
-try:
-    from autogen.agentchat.contrib.img_utils import num_tokens_from_gpt_image
+from .agentchat.contrib.img_utils import num_tokens_from_gpt_image
+from .import_utils import optional_import_block
 
-    img_util_imported = True
-except ImportError:
+# if PIL is not imported, we will redefine num_tokens_from_gpt_image to return 0 tokens for images
+# Otherwise, it would raise an ImportError
+with optional_import_block() as result:
+    import PIL  # noqa: F401
+
+pil_imported = result.is_successful
+if not pil_imported:
 
     def num_tokens_from_gpt_image(*args, **kwargs):
         return 0
 
-    img_util_imported = False
-
 
 logger = logging.getLogger(__name__)
 logger.img_dependency_warned = False  # member variable to track if the warning has been logged
@@ -180,7 +183,7 @@ def _num_token_from_messages(messages: Union[list, dict], model=""gpt-3.5-turbo-0
                         num_tokens += len(encoding.encode(part[""text""]))
                     if ""image_url"" in part:
                         assert ""url"" in part[""image_url""]
-                        if not img_util_imported and not logger.img_dependency_warned:
+                        if not pil_imported and not logger.img_dependency_warned:
                             logger.warning(
                                 ""img_utils or PIL not imported. Skipping image token count.""
                                 ""Please install autogen with [lmm] option."",