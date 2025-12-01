@@ -20,8 +20,7 @@
 
 import docker
 
-from autogen import oai
-
+from . import oai
 from .types import UserMessageImageContentPart, UserMessageTextContentPart
 
 SENTINEL = object()