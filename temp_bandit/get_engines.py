@@ -1,12 +1,12 @@
 # Copyright 2024 Marimo. All rights reserved.
 from __future__ import annotations
 
-from marimo._types.ids import VariableName
 from typing import Any, cast
 
 from marimo._data.models import DataSourceConnection
 from marimo._sql.engines import DuckDBEngine, SQLAlchemyEngine
 from marimo._sql.types import SQLEngine
+from marimo._types.ids import VariableName
 
 
 def get_engines_from_variables(