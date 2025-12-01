@@ -7,8 +7,8 @@
 
 import dpath
 import google.generativeai as genai  # type: ignore  # missing library stubs or py.typed marker
-from airbyte_protocol.models import (  # type: ignore  # missing library stubs or py.typed marker
-    AirbyteCatalog,  # type: ignore  # missing library stubs or py.typed marker
+from airbyte_cdk.models import (
+    AirbyteCatalog,
 )
 from markdown_it import MarkdownIt
 from pydbml.renderer.dbml.default import (  # type: ignore  # missing library stubs or py.typed marker