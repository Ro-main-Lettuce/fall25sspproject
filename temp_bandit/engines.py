@@ -3,13 +3,13 @@
 
 from typing import TYPE_CHECKING, Any, Optional
 
-from marimo._types.ids import VariableName
 from marimo import _loggers
 from marimo._data.get_datasets import get_datasets_from_duckdb
 from marimo._data.models import DataTable, DataTableColumn, DataType
 from marimo._dependencies.dependencies import DependencyManager
 from marimo._sql.types import SQLEngine
 from marimo._sql.utils import wrapped_sql
+from marimo._types.ids import VariableName
 
 LOGGER = _loggers.marimo_logger()
 