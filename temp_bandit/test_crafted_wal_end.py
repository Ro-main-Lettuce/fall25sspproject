@@ -1,9 +1,13 @@
 from __future__ import annotations
 
+from typing import TYPE_CHECKING
+
 import pytest
 from fixtures.log_helper import log
 from fixtures.neon_cli import WalCraft
-from fixtures.neon_fixtures import NeonEnvBuilder, PageserverWalReceiverProtocol
+
+if TYPE_CHECKING:
+    from fixtures.neon_fixtures import NeonEnvBuilder
 
 # Restart nodes with WAL end having specially crafted shape, like last record
 # crossing segment boundary, to test decoding issues.
@@ -19,17 +23,10 @@
         ""wal_record_crossing_segment_followed_by_small_one"",
     ],
 )
-@pytest.mark.parametrize(
-    ""wal_receiver_protocol"",
-    [PageserverWalReceiverProtocol.VANILLA, PageserverWalReceiverProtocol.INTERPRETED],
-)
 def test_crafted_wal_end(
     neon_env_builder: NeonEnvBuilder,
     wal_type: str,
-    wal_receiver_protocol: PageserverWalReceiverProtocol,
 ):
-    neon_env_builder.pageserver_wal_receiver_protocol = wal_receiver_protocol
-
     env = neon_env_builder.init_start()
     env.create_branch(""test_crafted_wal_end"")
     env.pageserver.allowed_errors.extend(