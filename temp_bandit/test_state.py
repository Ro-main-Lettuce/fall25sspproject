@@ -27,18 +27,20 @@
 from reflex.base import Base
 from reflex.constants import CompileVars, RouteVar, SocketEvent
 from reflex.event import Event, EventHandler
+from reflex.istate.manager import (
+    LockExpiredError,
+    StateManager,
+    StateManagerDisk,
+    StateManagerMemory,
+    StateManagerRedis,
+)
 from reflex.state import (
     BaseState,
     ImmutableStateError,
-    LockExpiredError,
     MutableProxy,
     OnLoadInternalState,
     RouterData,
     State,
-    StateManager,
-    StateManagerDisk,
-    StateManagerMemory,
-    StateManagerRedis,
     StateProxy,
     StateUpdate,
     _substate_key,
@@ -1777,7 +1779,7 @@ def substate_token_redis(state_manager_redis, token):
 
 @pytest.mark.asyncio
 async def test_state_manager_lock_expire(
-    state_manager_redis: StateManager, token: str, substate_token_redis: str
+    state_manager_redis: StateManagerRedis, token: str, substate_token_redis: str
 ):
     """"""Test that the state manager lock expires and raises exception exiting context.
 
@@ -1799,7 +1801,7 @@ async def test_state_manager_lock_expire(
 
 @pytest.mark.asyncio
 async def test_state_manager_lock_expire_contend(
-    state_manager_redis: StateManager, token: str, substate_token_redis: str
+    state_manager_redis: StateManagerRedis, token: str, substate_token_redis: str
 ):
     """"""Test that the state manager lock expires and queued waiters proceed.
 
@@ -1844,7 +1846,10 @@ async def _coro_waiter():
 
 @pytest.mark.asyncio
 async def test_state_manager_lock_warning_threshold_contend(
-    state_manager_redis: StateManager, token: str, substate_token_redis: str, mocker
+    state_manager_redis: StateManagerRedis,
+    token: str,
+    substate_token_redis: str,
+    mocker,
 ):
     """"""Test that the state manager triggers a warning when lock contention exceeds the warning threshold.
 
@@ -3354,7 +3359,8 @@ def test_redis_state_manager_config_knobs(tmp_path, expiration_kwargs, expected_
     with chdir(proj_root):
         # reload config for each parameter to avoid stale values
         reflex.config.get_config(reload=True)
-        from reflex.state import State, StateManager
+        from reflex.istate.manager import StateManager
+        from reflex.state import State
 
         state_manager = StateManager.create(state=State)
         assert state_manager.lock_expiration == expected_values[0]  # pyright: ignore [reportAttributeAccessIssue]
@@ -3392,7 +3398,8 @@ def test_redis_state_manager_config_knobs_invalid_lock_warning_threshold(
     with chdir(proj_root):
         # reload config for each parameter to avoid stale values
         reflex.config.get_config(reload=True)
-        from reflex.state import State, StateManager
+        from reflex.istate.manager import StateManager
+        from reflex.state import State
 
         with pytest.raises(InvalidLockWarningThresholdError):
             StateManager.create(state=State)