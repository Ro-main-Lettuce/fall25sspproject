@@ -90,10 +90,12 @@ def test_compute_catalog(neon_simple_env: NeonEnv):
     # and reconfigure the endpoint to create some test databases.
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""roles"": TEST_ROLE_NAMES,
-                ""databases"": TEST_DB_NAMES,
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""roles"": TEST_ROLE_NAMES,
+                    ""databases"": TEST_DB_NAMES,
+                },
             },
         }
     )
@@ -155,10 +157,12 @@ def test_compute_create_drop_dbs_and_roles(neon_simple_env: NeonEnv):
     # and reconfigure the endpoint to apply the changes.
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""roles"": TEST_ROLE_NAMES,
-                ""databases"": TEST_DB_NAMES,
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""roles"": TEST_ROLE_NAMES,
+                    ""databases"": TEST_DB_NAMES,
+                },
             },
         }
     )
@@ -196,12 +200,14 @@ def test_compute_create_drop_dbs_and_roles(neon_simple_env: NeonEnv):
 
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""roles"": [],
-                ""databases"": [],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""roles"": [],
+                    ""databases"": [],
+                },
+                ""delta_operations"": delta_operations,
             },
-            ""delta_operations"": delta_operations,
         }
     )
     endpoint.reconfigure()
@@ -250,9 +256,11 @@ def test_dropdb_with_subscription(neon_simple_env: NeonEnv):
     # and reconfigure the endpoint to apply the changes.
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""databases"": TEST_DB_NAMES,
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""databases"": TEST_DB_NAMES,
+                },
             },
         }
     )
@@ -306,17 +314,19 @@ def test_dropdb_with_subscription(neon_simple_env: NeonEnv):
     # and reconfigure the endpoint to apply the changes.
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""databases"": TEST_DB_NAMES_NEW,
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""databases"": TEST_DB_NAMES_NEW,
+                },
+                ""delta_operations"": [
+                    {""action"": ""delete_db"", ""name"": SUB_DB_NAME},
+                    # also test the case when we try to delete a non-existent database
+                    # shouldn't happen in normal operation,
+                    # but can occur when failed operations are retried
+                    {""action"": ""delete_db"", ""name"": ""nonexistent_db""},
+                ],
             },
-            ""delta_operations"": [
-                {""action"": ""delete_db"", ""name"": SUB_DB_NAME},
-                # also test the case when we try to delete a non-existent database
-                # shouldn't happen in normal operation,
-                # but can occur when failed operations are retried
-                {""action"": ""delete_db"", ""name"": ""nonexistent_db""},
-            ],
         }
     )
 
@@ -354,25 +364,27 @@ def test_drop_role_with_table_privileges_from_neon_superuser(neon_simple_env: Ne
 
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""roles"": [
-                    {
-                        # We need to create role via compute_ctl, because in this case it will receive
-                        # additional grants equivalent to our real environment, so we can repro some
-                        # issues.
-                        ""name"": ""neon"",
-                        # Some autocomplete-suggested hash, no specific meaning.
-                        ""encrypted_password"": ""SCRAM-SHA-256$4096:hBT22QjqpydQWqEulorfXA==$miBogcoj68JWYdsNB5PW1X6PjSLBEcNuctuhtGkb4PY=:hxk2gxkwxGo6P7GCtfpMlhA9zwHvPMsCz+NQf2HfvWk="",
-                        ""options"": [],
-                    },
-                ],
-                ""databases"": [
-                    {
-                        ""name"": TEST_DB_NAME,
-                        ""owner"": ""neon"",
-                    },
-                ],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""roles"": [
+                        {
+                            # We need to create role via compute_ctl, because in this case it will receive
+                            # additional grants equivalent to our real environment, so we can repro some
+                            # issues.
+                            ""name"": ""neon"",
+                            # Some autocomplete-suggested hash, no specific meaning.
+                            ""encrypted_password"": ""SCRAM-SHA-256$4096:hBT22QjqpydQWqEulorfXA==$miBogcoj68JWYdsNB5PW1X6PjSLBEcNuctuhtGkb4PY=:hxk2gxkwxGo6P7GCtfpMlhA9zwHvPMsCz+NQf2HfvWk="",
+                            ""options"": [],
+                        },
+                    ],
+                    ""databases"": [
+                        {
+                            ""name"": TEST_DB_NAME,
+                            ""owner"": ""neon"",
+                        },
+                    ],
+                },
             },
         }
     )
@@ -415,13 +427,15 @@ def test_drop_role_with_table_privileges_from_neon_superuser(neon_simple_env: Ne
     # Drop role via compute_ctl
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""delta_operations"": [
-                {
-                    ""action"": ""delete_role"",
-                    ""name"": TEST_GRANTEE,
-                },
-            ],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""delta_operations"": [
+                    {
+                        ""action"": ""delete_role"",
+                        ""name"": TEST_GRANTEE,
+                    },
+                ],
+            },
         }
     )
     endpoint.reconfigure()
@@ -444,13 +458,15 @@ def test_drop_role_with_table_privileges_from_neon_superuser(neon_simple_env: Ne
 
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""delta_operations"": [
-                {
-                    ""action"": ""delete_role"",
-                    ""name"": ""readonly2"",
-                },
-            ],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""delta_operations"": [
+                    {
+                        ""action"": ""delete_role"",
+                        ""name"": ""readonly2"",
+                    },
+                ],
+            },
         }
     )
     endpoint.reconfigure()
@@ -475,25 +491,27 @@ def test_drop_role_with_table_privileges_from_non_neon_superuser(neon_simple_env
     endpoint = env.endpoints.create_start(""main"")
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""cluster"": {
-                ""roles"": [
-                    {
-                        # We need to create role via compute_ctl, because in this case it will receive
-                        # additional grants equivalent to our real environment, so we can repro some
-                        # issues.
-                        ""name"": TEST_GRANTOR,
-                        # Some autocomplete-suggested hash, no specific meaning.
-                        ""encrypted_password"": ""SCRAM-SHA-256$4096:hBT22QjqpydQWqEulorfXA==$miBogcoj68JWYdsNB5PW1X6PjSLBEcNuctuhtGkb4PY=:hxk2gxkwxGo6P7GCtfpMlhA9zwHvPMsCz+NQf2HfvWk="",
-                        ""options"": [],
-                    },
-                ],
-                ""databases"": [
-                    {
-                        ""name"": TEST_DB_NAME,
-                        ""owner"": TEST_GRANTOR,
-                    },
-                ],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""cluster"": {
+                    ""roles"": [
+                        {
+                            # We need to create role via compute_ctl, because in this case it will receive
+                            # additional grants equivalent to our real environment, so we can repro some
+                            # issues.
+                            ""name"": TEST_GRANTOR,
+                            # Some autocomplete-suggested hash, no specific meaning.
+                            ""encrypted_password"": ""SCRAM-SHA-256$4096:hBT22QjqpydQWqEulorfXA==$miBogcoj68JWYdsNB5PW1X6PjSLBEcNuctuhtGkb4PY=:hxk2gxkwxGo6P7GCtfpMlhA9zwHvPMsCz+NQf2HfvWk="",
+                            ""options"": [],
+                        },
+                    ],
+                    ""databases"": [
+                        {
+                            ""name"": TEST_DB_NAME,
+                            ""owner"": TEST_GRANTOR,
+                        },
+                    ],
+                },
             },
         }
     )
@@ -507,13 +525,15 @@ def test_drop_role_with_table_privileges_from_non_neon_superuser(neon_simple_env
 
     endpoint.respec_deep(
         **{
-            ""skip_pg_catalog_updates"": False,
-            ""delta_operations"": [
-                {
-                    ""action"": ""delete_role"",
-                    ""name"": TEST_GRANTEE,
-                },
-            ],
+            ""spec"": {
+                ""skip_pg_catalog_updates"": False,
+                ""delta_operations"": [
+                    {
+                        ""action"": ""delete_role"",
+                        ""name"": TEST_GRANTEE,
+                    },
+                ],
+            },
         }
     )
     endpoint.reconfigure()