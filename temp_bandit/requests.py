@@ -20,13 +20,12 @@
 
 from marimo._config.config import MarimoConfig
 from marimo._data.models import DataTableSource
-from marimo._types.ids import CellId_t
+from marimo._types.ids import CellId_t, UIElementId
 
 if TYPE_CHECKING:
     from starlette.datastructures import URL
     from starlette.requests import HTTPConnection
 
-UIElementId = str
 CompletionRequestId = str
 FunctionCallId = str
 