@@ -16,7 +16,7 @@
 
 """"""
 Usage:
-DEFAULT_PG_VERSION=16 BUILD_TYPE=debug NEON_ENV_BUILDER_USE_OVERLAYFS_FOR_SNAPSHOTS=1 INTERACTIVE=true \
+DEFAULT_PG_VERSION=17 BUILD_TYPE=debug NEON_ENV_BUILDER_USE_OVERLAYFS_FOR_SNAPSHOTS=1 INTERACTIVE=true \
     ./scripts/pytest --timeout 0 test_runner/performance/pageserver/interactive/test_many_small_tenants.py
 """"""
 