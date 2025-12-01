@@ -16,6 +16,7 @@
 import ray
 
 from slippi_ai import train_lib
+from slippi_ai import saving
 from slippi_ai import flag_utils, eval_lib
 from slippi_ai import dolphin as dolphin_lib
 
@@ -130,8 +131,7 @@ def __init__(
     self.agent_kwargs = agent_kwargs
     self.stop_requested = threading.Event()
 
-    agent_path = self.agent_kwargs['path']
-    agent_state = eval_lib.load_state(path=agent_path)
+    agent_state = eval_lib.load_state(self.agent_kwargs)
     agent_config = flag_utils.dataclass_from_dict(
         train_lib.Config, agent_state['config'])
 
@@ -331,7 +331,7 @@ def _reload_models(self):
 
     for agent in agents:
       path = os.path.join(self._models_path, agent)
-      state = eval_lib.load_state(path=path)
+      state = saving.load_state_from_disk(path)
       state = {k: state[k] for k in ['step', 'config', 'rl_config'] if k in state}
       self._models[agent] = state
 