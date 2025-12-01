@@ -1,5 +1,6 @@
 import os
 import ssl
+from datetime import datetime, timedelta
 
 import pytest
 import requests
@@ -151,3 +152,63 @@ def cert_reloaded():
     requests.get(addr, verify=str(env.ssl_ca_file)).raise_for_status()
     cur_cert = ssl.get_server_certificate((""localhost"", port))
     assert cur_cert == sk_cert
+
+
+def test_server_and_cert_metrics(neon_env_builder: NeonEnvBuilder):
+    """"""
+    Test metrics exported from http/https server and tls cert reloader.
+    """"""
+    neon_env_builder.use_https_pageserver_api = True
+    neon_env_builder.pageserver_config_override = ""ssl_cert_reload_period='100 ms'""
+    env = neon_env_builder.init_start()
+
+    env.pageserver.allowed_errors.append("".*Error reloading certificate.*"")
+
+    ps_client = env.pageserver.http_client()
+
+    # 1. Test connection started metric.
+    filter_https = {""scheme"": ""https""}
+    old_https_conn_count = (
+        ps_client.get_metric_value(""http_server_connection_started_total"", filter_https) or 0
+    )
+
+    addr = f""https://localhost:{env.pageserver.service_port.https}/v1/status""
+    requests.get(addr, verify=str(env.ssl_ca_file)).raise_for_status()
+
+    new_https_conn_count = (
+        ps_client.get_metric_value(""http_server_connection_started_total"", filter_https) or 0
+    )
+    # The counter should increase after the request,
+    # but it may increase by more than one because of storcon requests.
+    assert new_https_conn_count > old_https_conn_count
+
+    # 2. Test tls connection error.
+    # Request without specified CA cert file should fail.
+    with pytest.raises(requests.exceptions.SSLError):
+        requests.get(addr)
+
+    tls_error_cnt = (
+        ps_client.get_metric_value(""http_server_connection_errors_total"", {""type"": ""tls""}) or 0
+    )
+    assert tls_error_cnt == 1
+
+    # 3. Test expiration time metric.
+    expiration_time = datetime.fromtimestamp(
+        ps_client.get_metric_value(""tls_certs_expiration_time_seconds"") or 0
+    )
+    now = datetime.now()
+    # neon_local generates certs valid for 100 years.
+    # Compare with +-1 year to not care about leap years.
+    assert now + timedelta(days=365 * 99) < expiration_time < now + timedelta(days=365 * 101)
+
+    # 4. Test cert reload failed metric.
+    reload_error_cnt = ps_client.get_metric_value(""tls_certs_reload_failed_total"")
+    assert reload_error_cnt == 0
+
+    os.remove(env.pageserver.workdir / ""server.crt"")
+
+    def reload_failed():
+        reload_error_cnt = ps_client.get_metric_value(""tls_certs_reload_failed_total"") or 0
+        assert reload_error_cnt > 0
+
+    wait_until(reload_failed)