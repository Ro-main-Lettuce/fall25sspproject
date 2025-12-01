@@ -4,13 +4,13 @@
 from typing import List, Set, Union
 
 import yaml
-from airbyte_cdk.sources.declarative.parsers.manifest_reference_resolver import (
-    ManifestReferenceResolver,
-)
-from airbyte_protocol.models import (  # type: ignore  # missing library stubs or py.typed marker
+from airbyte_cdk.models import (
     AirbyteCatalog,
     AirbyteStream,
 )
+from airbyte_cdk.sources.declarative.parsers.manifest_reference_resolver import (
+    ManifestReferenceResolver,
+)
 from pydbml import Database  # type: ignore  # missing library stubs or py.typed marker
 from pydbml.classes import (  # type: ignore  # missing library stubs or py.typed marker
     Column,