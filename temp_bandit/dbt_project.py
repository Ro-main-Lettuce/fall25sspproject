@@ -109,6 +109,7 @@ def test(
         materialization: str = ""table"",  # Only relevant if as_model=True
         test_vars: Optional[dict] = None,
         elementary_enabled: bool = True,
+        model_config: Optional[Dict[str, Any]] = None,
         *,
         multiple_results: Literal[False] = False,
     ) -> Dict[str, Any]:
@@ -128,6 +129,7 @@ def test(
         materialization: str = ""table"",  # Only relevant if as_model=True
         test_vars: Optional[dict] = None,
         elementary_enabled: bool = True,
+        model_config: Optional[Dict[str, Any]] = None,
         *,
         multiple_results: Literal[True],
     ) -> List[Dict[str, Any]]:
@@ -146,6 +148,7 @@ def test(
         materialization: str = ""table"",  # Only relevant if as_model=True
         test_vars: Optional[dict] = None,
         elementary_enabled: bool = True,
+        model_config: Optional[Dict[str, Any]] = None,
         *,
         multiple_results: bool = False,
     ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
@@ -161,6 +164,9 @@ def test(
         test_args = test_args or {}
         table_yaml: Dict[str, Any] = {""name"": test_id}
 
+        if model_config:
+            table_yaml.update(model_config)
+
         if columns:
             table_yaml[""columns""] = columns
 