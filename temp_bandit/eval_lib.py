@@ -630,6 +630,12 @@ def build_agent(
     ai=BATCH_AGENT_FLAGS,
 )
 
+def load_state(agent_kwargs: dict) -> dict:
+  path = agent_kwargs.pop('path')
+  if 'tag' in agent_kwargs:
+    logging.warning('`tag` is no longer used, deleting from agent config')
+    del agent_kwargs['tag']
+  return saving.load_state_from_disk(path)
 
 def get_player(
     type: str,
@@ -643,7 +649,7 @@ def get_player(
     return dolphin.Human()
   elif type == 'cpu':
     return dolphin.CPU(character, level)
-
+  raise ValueError(f'Unknown player type: {type}')
 
 def update_character(player: dolphin.AI, config: dict):
   allowed_characters = config['dataset']['allowed_characters']