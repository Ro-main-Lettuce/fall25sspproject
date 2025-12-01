@@ -42,6 +42,7 @@
 
 LOGGER = _loggers.marimo_logger()
 
+
 PostExecutionHookType = Callable[
     [CellImpl, cell_runner.Runner, cell_runner.RunResult], None
 ]
@@ -127,7 +128,7 @@ def _broadcast_datasets(
     del run_result
     tables = get_datasets_from_variables(
         [
-            (VariableName(variable), runner.glbls[variable])  # type: ignore[arg-type]
+            (VariableName(variable), runner.glbls[variable])
             for variable in cell.defs
             if variable in runner.glbls
         ]
@@ -150,7 +151,7 @@ def _broadcast_data_source_connection(
     del run_result
     engines = get_engines_from_variables(
         [
-            (VariableName(variable), runner.glbls[variable])  # type: ignore[arg-type]
+            (VariableName(variable), runner.glbls[variable])
             for variable in cell.defs
             if variable in runner.glbls
         ]