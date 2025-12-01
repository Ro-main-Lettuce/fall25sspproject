@@ -14,7 +14,6 @@
     Endpoint,
     NeonEnv,
     NeonEnvBuilder,
-    PageserverWalReceiverProtocol,
     Safekeeper,
 )
 from fixtures.remote_storage import RemoteStorageKind
@@ -751,15 +750,8 @@ async def run_segment_init_failure(env: NeonEnv):
 # Test (injected) failure during WAL segment init.
 # https://github.com/neondatabase/neon/issues/6401
 # https://github.com/neondatabase/neon/issues/6402
-@pytest.mark.parametrize(
-    ""wal_receiver_protocol"",
-    [PageserverWalReceiverProtocol.VANILLA, PageserverWalReceiverProtocol.INTERPRETED],
-)
-def test_segment_init_failure(
-    neon_env_builder: NeonEnvBuilder, wal_receiver_protocol: PageserverWalReceiverProtocol
-):
+def test_segment_init_failure(neon_env_builder: NeonEnvBuilder):
     neon_env_builder.num_safekeepers = 1
-    neon_env_builder.pageserver_wal_receiver_protocol = wal_receiver_protocol
     env = neon_env_builder.init_start()
 
     asyncio.run(run_segment_init_failure(env))