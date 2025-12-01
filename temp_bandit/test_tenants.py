@@ -390,6 +390,7 @@ def test_create_churn_during_restart(neon_env_builder: NeonEnvBuilder):
     # Tenant creation requests which arrive out of order will generate complaints about
     # generation nubmers out of order.
     env.pageserver.allowed_errors.append("".*Generation .+ is less than existing .+"")
+    env.storage_controller.allowed_errors.append("".*due to stale generation.*"")
 
     # Timeline::flush_and_shutdown cannot tell if it is hitting a failure because of
     # an incomplete attach, or some other problem.  In the field this should be rare,