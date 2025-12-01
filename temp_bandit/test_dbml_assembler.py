@@ -4,8 +4,8 @@
 from unittest.mock import Mock
 
 from airbyte_cdk.models import AirbyteCatalog, AirbyteStream, SyncMode
-from erd.dbml_assembler import DbmlAssembler, Source
 
+from erd.dbml_assembler import DbmlAssembler, Source
 from tests.builder import RelationshipBuilder
 
 _A_STREAM_NAME = ""a_stream_name""