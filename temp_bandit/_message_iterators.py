@@ -7,10 +7,10 @@
 from collections.abc import Iterator
 from typing import IO, TYPE_CHECKING, cast
 
-import pendulum
 import pydantic
 from typing_extensions import final
 
+from airbyte_cdk.utils.datetime_helpers import ab_datetime_now
 from airbyte_protocol.models import (
     AirbyteMessage,
     AirbyteRecordMessage,
@@ -39,15 +39,22 @@ def _new_stream_success_message(stream_name: str) -> AirbyteMessage:
         type=Type.TRACE,
         trace=AirbyteTraceMessage(
             type=TraceType.STREAM_STATUS,
-            stream=stream_name,
-            emitted_at=pendulum.now().float_timestamp,
+            emitted_at=ab_datetime_now().timestamp(),
             stream_status=AirbyteStreamStatusTraceMessage(
                 stream_descriptor=StreamDescriptor(
                     name=stream_name,
                 ),
                 status=AirbyteStreamStatus.COMPLETE,
+                reasons=None,
             ),
+            estimate=None,
+            error=None,
         ),
+        log=None,
+        record=None,
+        state=None,
+        catalog=None,
+        control=None,
     )
 
 