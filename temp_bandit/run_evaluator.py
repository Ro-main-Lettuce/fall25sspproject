@@ -11,6 +11,7 @@
   import fancyflags as ff
 
   from slippi_ai import eval_lib, dolphin, utils, evaluators, flag_utils
+  from slippi_ai import saving
 
   default_dolphin_config = dolphin.DolphinConfig(
       infinite_time=False,
@@ -45,11 +46,9 @@
 
   def main(_):
     p1_agent_kwargs: dict = AGENT.value.copy()
-    state = eval_lib.load_state(
-        path=p1_agent_kwargs.pop('path'),
-        tag=p1_agent_kwargs.pop('tag'))
+    p1_state = eval_lib.load_state(p1_agent_kwargs)
     p1_agent_kwargs.update(
-        state=state,
+        state=p1_state,
         batch_steps=NUM_AGENT_STEPS.value,
     )
 
@@ -63,9 +62,7 @@ def main(_):
 
       if isinstance(p2, dolphin.AI):
         p2_agent_kwargs: dict = OPPONENT.value['ai']
-        p2_state = eval_lib.load_state(
-            path=p2_agent_kwargs.pop('path'),
-            tag=p2_agent_kwargs.pop('tag'))
+        p2_state = eval_lib.load_state(p2_agent_kwargs)
         p2_agent_kwargs.update(
             state=p2_state,
             batch_steps=NUM_AGENT_STEPS.value,