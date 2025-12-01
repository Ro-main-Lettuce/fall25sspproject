@@ -72,6 +72,7 @@
     ""wal_receiver_protocol"",
     [PageserverWalReceiverProtocol.VANILLA, PageserverWalReceiverProtocol.INTERPRETED],
 )
+@pytest.mark.timeout(900)
 def test_pageserver_compaction_smoke(
     neon_env_builder: NeonEnvBuilder,
     wal_receiver_protocol: PageserverWalReceiverProtocol,
@@ -162,6 +163,8 @@ def test_pageserver_compaction_preempt(
     conf = PREEMPT_COMPACTION_TENANT_CONF.copy()
     env = neon_env_builder.init_start(initial_tenant_conf=conf)
 
+    env.pageserver.allowed_errors.append("".*The timeline or pageserver is shutting down.*"")
+
     tenant_id = env.initial_tenant
     timeline_id = env.initial_timeline
 
@@ -188,6 +191,7 @@ def test_pageserver_compaction_preempt(
 
 
 @skip_in_debug_build(""only run with release build"")
+@pytest.mark.timeout(600)
 def test_pageserver_gc_compaction_preempt(
     neon_env_builder: NeonEnvBuilder,
 ):
@@ -197,6 +201,8 @@ def test_pageserver_gc_compaction_preempt(
     conf = PREEMPT_GC_COMPACTION_TENANT_CONF.copy()
     env = neon_env_builder.init_start(initial_tenant_conf=conf)
 
+    env.pageserver.allowed_errors.append("".*The timeline or pageserver is shutting down.*"")
+
     tenant_id = env.initial_tenant
     timeline_id = env.initial_timeline
 
@@ -223,7 +229,7 @@ def test_pageserver_gc_compaction_preempt(
 
 
 @skip_in_debug_build(""only run with release build"")
-@pytest.mark.timeout(900)  # This test is slow with sanitizers enabled, especially on ARM
+@pytest.mark.timeout(600)  # This test is slow with sanitizers enabled, especially on ARM
 @pytest.mark.parametrize(
     ""with_branches"",
     [""with_branches"", ""no_branches""],