@@ -30,7 +30,7 @@
 from .environments import _get_environment_cached
 from .exception import InteractiveTimeoutError, InvalidError, RemoteError, _CliUserExecutionError
 from .functions import _Function
-from .output import OUTPUT_ENABLED, _get_output_manager, enable_output
+from .output import _get_output_manager, enable_output
 from .running_app import RunningApp, running_app_from_layout
 from .sandbox import _Sandbox
 from .secret import _Secret
@@ -289,11 +289,12 @@ async def _run_app(
 
     app_state = api_pb2.APP_STATE_DETACHED if detach else api_pb2.APP_STATE_EPHEMERAL
 
-    if interactive and not OUTPUT_ENABLED:
+    output_mgr = _get_output_manager()
+    if interactive and output_mgr is None:
         warnings.warn(
             ""Interactive mode is disabled because no output manager is active. ""
             ""Use 'with modal.enable_output():' to enable interactive mode and see logs."",
-            stacklevel=2
+            stacklevel=2,
         )
         interactive = False
 
@@ -316,7 +317,7 @@ def heartbeat():
         tc.infinite_loop(heartbeat, sleep=HEARTBEAT_INTERVAL, log_exception=not detach)
         logs_loop: Optional[asyncio.Task] = None
 
-        if output_mgr := _get_output_manager():
+        if output_mgr is not None:
             # Defer import so this module is rich-safe
             # TODO(michael): The get_app_logs_loop function is itself rich-safe aside from accepting an OutputManager
             # as an argument, so with some refactoring we could avoid the need for this deferred import.