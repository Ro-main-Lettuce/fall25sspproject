@@ -4,34 +4,55 @@
 
 
 import json
+import os
+import tempfile
+from pathlib import Path
 from typing import Any, Mapping
+from unittest import TestCase
 
 import pytest
 from source_amazon_seller_partner.config_migrations import MigrateAccountType, MigrateReportOptions, MigrateStreamNameOption
 from source_amazon_seller_partner.source import SourceAmazonSellerPartner
 
 from airbyte_cdk.models import OrchestratorType, Type
 from airbyte_cdk.sources import Source
+from airbyte_cdk.test.state_builder import StateBuilder
 
 
-CMD = ""check""
-SOURCE: Source = SourceAmazonSellerPartner()
-
+MIGRATIONS_TEST_DIRECTORY = Path(__file__).parent / ""test_migrations""
 
-def load_config(config_path: str) -> Mapping[str, Any]:
-    with open(config_path, ""r"") as config:
+CMD = ""check""
+SOURCE: Source = SourceAmazonSellerPartner(
+    None,
+    {
+        ""replication_start_date"": ""2021-07-01T00:00:00Z"",
+        ""refresh_token"": ""<refresh_token>"",
+        ""lwa_app_id"": ""<lwa_app_id>"",
+        ""lwa_client_secret"": ""<lwa_client_secret>"",
+        ""aws_access_key"": ""<aws_access_key>"",
+        ""aws_secret_key"": ""<aws_secret_key>"",
+        ""role_arn"": ""<role_arn>"",
+        ""aws_environment"": ""PRODUCTION"",
+        ""region"": ""US"",
+    },
+    StateBuilder().build(),
+)
+
+
+def load_config(config_path: Path) -> Mapping[str, Any]:
+    with config_path.open() as config:
         return json.load(config)
 
 
 class TestMigrateAccountType:
-    test_not_migrated_config_path = ""unit_tests/test_migrations/account_type_migration/not_migrated_config.json""
-    test_migrated_config_path = ""unit_tests/test_migrations/account_type_migration/migrated_config.json""
+    test_not_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""account_type_migration/not_migrated_config.json""
+    test_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""account_type_migration/migrated_config.json""
 
     def test_migrate_config(self, capsys):
         config = load_config(self.test_not_migrated_config_path)
         assert ""account_type"" not in config
         migration_instance = MigrateAccountType()
-        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path], SOURCE)
+        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path.as_posix()], SOURCE)
         control_msg = json.loads(capsys.readouterr().out)
         assert control_msg[""type""] == Type.CONTROL.value
         assert control_msg[""control""][""type""] == OrchestratorType.CONNECTOR_CONFIG.value
@@ -46,8 +67,8 @@ def test_should_not_migrate(self):
 
 
 class TestMigrateReportOptions:
-    test_not_migrated_config_path = ""unit_tests/test_migrations/report_options_migration/not_migrated_config.json""
-    test_migrated_config_path = ""unit_tests/test_migrations/report_options_migration/migrated_config.json""
+    test_not_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""report_options_migration/not_migrated_config.json""
+    test_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""report_options_migration/migrated_config.json""
 
     @pytest.mark.parametrize(
         (""input_config"", ""expected_report_options_list""),
@@ -69,7 +90,7 @@ def test_migrate_config(self, capsys):
         config = load_config(self.test_not_migrated_config_path)
         assert ""report_options_list"" not in config
         migration_instance = MigrateReportOptions()
-        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path], SOURCE)
+        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path.as_posix()], SOURCE)
         control_msg = json.loads(capsys.readouterr().out)
         assert control_msg[""type""] == Type.CONTROL.value
         assert control_msg[""control""][""type""] == OrchestratorType.CONNECTOR_CONFIG.value
@@ -87,16 +108,16 @@ def test_should_not_migrate(self):
 
 
 class TestMigrateStreamNameOption:
-    test_not_migrated_config_path = ""unit_tests/test_migrations/stream_name_option_migration/not_migrated_config.json""
-    test_migrated_config_path = ""unit_tests/test_migrations/stream_name_option_migration/migrated_config.json""
+    test_not_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""stream_name_option_migration/not_migrated_config.json""
+    test_migrated_config_path = MIGRATIONS_TEST_DIRECTORY / ""stream_name_option_migration/migrated_config.json""
 
     def test_migrate_config(self, capsys):
         config = load_config(self.test_not_migrated_config_path)
         for options_list in config[""report_options_list""]:
             assert ""report_name"" not in options_list
 
         migration_instance = MigrateStreamNameOption()
-        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path], SOURCE)
+        migration_instance.migrate([CMD, ""--config"", self.test_not_migrated_config_path.as_posix()], SOURCE)
         control_msg = json.loads(capsys.readouterr().out)
         assert control_msg[""type""] == Type.CONTROL.value
         assert control_msg[""control""][""type""] == OrchestratorType.CONNECTOR_CONFIG.value