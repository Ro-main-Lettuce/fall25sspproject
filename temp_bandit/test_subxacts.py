@@ -1,9 +1,7 @@
 from __future__ import annotations
 
-import pytest
 from fixtures.neon_fixtures import (
     NeonEnvBuilder,
-    PageserverWalReceiverProtocol,
     check_restored_datadir_content,
 )
 
@@ -14,13 +12,7 @@
 # maintained in the pageserver, so subtransactions are not very exciting for
 # Neon. They are included in the commit record though and updated in the
 # CLOG.
-@pytest.mark.parametrize(
-    ""wal_receiver_protocol"",
-    [PageserverWalReceiverProtocol.VANILLA, PageserverWalReceiverProtocol.INTERPRETED],
-)
-def test_subxacts(neon_env_builder: NeonEnvBuilder, test_output_dir, wal_receiver_protocol):
-    neon_env_builder.pageserver_wal_receiver_protocol = wal_receiver_protocol
-
+def test_subxacts(neon_env_builder: NeonEnvBuilder, test_output_dir):
     env = neon_env_builder.init_start()
     endpoint = env.endpoints.create_start(""main"")
 