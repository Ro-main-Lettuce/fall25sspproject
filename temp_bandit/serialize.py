@@ -5,7 +5,7 @@
 import hashlib
 import json
 from pathlib import Path
-from typing import Optional, cast
+from typing import Any, Optional, Union, cast
 
 from marimo import __version__, _loggers
 from marimo._messaging.cell_output import CellChannel, CellOutput
@@ -44,10 +44,22 @@ def serialize_session_view(view: SessionView) -> NotebookSessionV1:
         # Convert output
         if cell_op.output:
             if cell_op.output.channel == CellChannel.MARIMO_ERROR:
-                for error in cast(list[MarimoError], cell_op.output.data):
+                for error in cast(
+                    list[Union[MarimoError, dict[str, Any]]],
+                    cell_op.output.data,
+                ):
                     # Handle both dictionary and object errors
-                    error_type = error.get(""type"", ""Unknown"") if isinstance(error, dict) else error.type
-                    error_value = error.get(""msg"", """") if isinstance(error, dict) else error.describe()
+                    # Errors can be a dictionary if they are serialized
+                    error_type = (
+                        error.get(""type"", ""Unknown"")
+                        if isinstance(error, dict)
+                        else error.type
+                    )
+                    error_value = (
+                        error.get(""msg"", """")
+                        if isinstance(error, dict)
+                        else error.describe()
+                    )
                     outputs.append(
                         ErrorOutput(
                             type=""error"",