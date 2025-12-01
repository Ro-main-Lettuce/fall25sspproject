@@ -8,7 +8,7 @@
 
 
 @pytest.mark.parametrize(
-    ""env_var,value,expected_ready"",
+    (""env_var"", ""value"", ""expected_ready""),
     [
         (""OTEL_SDK_DISABLED"", ""true"", False),
         (""OTEL_SDK_DISABLED"", ""TRUE"", False),
@@ -18,15 +18,15 @@
         (""CREWAI_DISABLE_TELEMETRY"", ""false"", True),
     ],
 )
-def test_telemetry_environment_variables(env_var, value, expected_ready):
+def test_telemetry_environment_variables(env_var, value, expected_ready) -> None:
     """"""Test telemetry state with different environment variable configurations.""""""
     with patch.dict(os.environ, {env_var: value}):
         with patch(""crewai.telemetry.telemetry.TracerProvider""):
             telemetry = Telemetry()
             assert telemetry.ready is expected_ready
 
 
-def test_telemetry_enabled_by_default():
+def test_telemetry_enabled_by_default() -> None:
     """"""Test that telemetry is enabled by default.""""""
     with patch.dict(os.environ, {}, clear=True):
         with patch(""crewai.telemetry.telemetry.TracerProvider""):
@@ -43,7 +43,7 @@ def test_telemetry_enabled_by_default():
     side_effect=Exception(""Test exception""),
 )
 @pytest.mark.vcr(filter_headers=[""authorization""])
-def test_telemetry_fails_due_connect_timeout(export_mock, logger_mock):
+def test_telemetry_fails_due_connect_timeout(export_mock, logger_mock) -> None:
     error = Exception(""Test exception"")
     export_mock.side_effect = error
 