@@ -101,3 +101,19 @@ def test_config_validation():
     # Test missing authentication
     with pytest.raises(ValueError):
         SnowflakeConfig(account=""test_account"", user=""test_user"")
+
+
+def test_synchronous_query_execution(snowflake_tool, mock_snowflake_connection):
+    with patch.object(snowflake_tool, ""_create_connection"") as mock_create_conn:
+        mock_create_conn.return_value = mock_snowflake_connection
+
+        results = snowflake_tool._run(
+            query=""SELECT * FROM test_table"", timeout=300
+        )
+
+        assert len(results) == 2
+        assert results[0][""col1""] == 1
+        assert results[0][""col2""] == ""value1""
+        mock_snowflake_connection.cursor.assert_called_once()
+
+        assert not asyncio.iscoroutine(results)