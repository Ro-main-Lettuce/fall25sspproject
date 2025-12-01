@@ -6,18 +6,20 @@
 from crewai.telemetry import Telemetry
 
 
-def test_telemetry_disabled_with_otel_sdk_disabled():
-    """"""Test that telemetry is disabled when OTEL_SDK_DISABLED is set to true.""""""
-    with patch.dict(os.environ, {""OTEL_SDK_DISABLED"": ""true""}):
-        telemetry = Telemetry()
-        assert telemetry.ready is False
-
-
-def test_telemetry_disabled_with_crewai_disable_telemetry():
-    """"""Test that telemetry is disabled when CREWAI_DISABLE_TELEMETRY is set to true.""""""
-    with patch.dict(os.environ, {""CREWAI_DISABLE_TELEMETRY"": ""true""}):
-        telemetry = Telemetry()
-        assert telemetry.ready is False
+@pytest.mark.parametrize(""env_var,value,expected_ready"", [
+    (""OTEL_SDK_DISABLED"", ""true"", False),
+    (""OTEL_SDK_DISABLED"", ""TRUE"", False),
+    (""CREWAI_DISABLE_TELEMETRY"", ""true"", False),
+    (""CREWAI_DISABLE_TELEMETRY"", ""TRUE"", False),
+    (""OTEL_SDK_DISABLED"", ""false"", True),
+    (""CREWAI_DISABLE_TELEMETRY"", ""false"", True),
+])
+def test_telemetry_environment_variables(env_var, value, expected_ready):
+    """"""Test telemetry state with different environment variable configurations.""""""
+    with patch.dict(os.environ, {env_var: value}):
+        with patch(""crewai.telemetry.telemetry.TracerProvider""):
+            telemetry = Telemetry()
+            assert telemetry.ready is expected_ready
 
 
 def test_telemetry_enabled_by_default():