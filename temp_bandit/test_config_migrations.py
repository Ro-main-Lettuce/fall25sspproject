@@ -19,9 +19,10 @@ def load_config(path: str) -> Mapping[str, Any]:
 
 def revert_config(path: str) -> None:
     migrated_config = load_config(path)
-    del migrated_config[""credentials""]
+    migrated_config_dict = dict(migrated_config)
+    del migrated_config_dict[""credentials""]
     with open(path, ""w"") as f:
-        f.write(json.dumps(migrated_config))
+        f.write(json.dumps(migrated_config_dict))
 
 
 @pytest.mark.parametrize(
@@ -35,9 +36,10 @@ def revert_config(path: str) -> None:
 )
 def test_config_migrations(config_file_path, run_revert):
     args = [""check"", ""--config"", config_file_path]
+    config_path = AirbyteEntrypoint.extract_config(args)
     source = SourceAirtable(
         catalog=MagicMock(),
-        config=AirbyteEntrypoint.extract_config(args),
+        config=SourceAirtable.read_config(config_path) if config_path else None,
         state=MagicMock(),
     )
 