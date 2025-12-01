@@ -65,13 +65,11 @@ def single_timeline(
     assert ps_http.tenant_list() == []
 
     def attach(tenant):
-        # NB: create the new tenant in the storage controller with the correct tenant config. This
-        # will pick up the existing tenant data from remote storage. If we just attach it to the
-        # Pageserver, the storage controller will reset the tenant config to the default.
-        env.create_tenant(
-            tenant_id=tenant,
-            timeline_id=template_timeline,
-            conf=template_config,
+        env.pageserver.tenant_attach(
+            tenant,
+            config=template_config,
+            generation=100,
+            override_storage_controller_generation=True,
         )
 
     with concurrent.futures.ThreadPoolExecutor(max_workers=22) as executor: