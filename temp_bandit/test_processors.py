@@ -101,8 +101,8 @@ def _build_mocked_snowflake_processor_with_key_pair(
     sql_config = SnowflakeConfig(
         account=""foo"",
         username=""foo"",
-        private_key_path=""/path/to/private_key.p8"",
-        private_key_passphrase=SecretString(""passphrase""),
+        private_key_file=""/path/to/private_key.p8"",
+        private_key_file_pwd=SecretString(""passphrase""),
         warehouse=""foo"",
         database=""foo"",
         role=""foo"",