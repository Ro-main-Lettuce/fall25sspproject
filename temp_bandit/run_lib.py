@@ -61,8 +61,7 @@ class ActorConfig:
 @dataclasses.dataclass
 class AgentConfig:
   # TODO: merge with ActorConfig?
-  path: tp.Optional[str] = None
-  tag: tp.Optional[str] = None
+  path: tp.Optional[str] = None  # Only used for static opponents
   compile: bool = True
   jit_compile: bool = False
   name: list[str] = field(lambda: [nametags.DEFAULT_NAME])
@@ -78,8 +77,8 @@ def get_kwargs(self) -> dict:
         batch_steps=self.batch_steps,
         async_inference=self.async_inference,
     )
-    if self.path or self.tag:
-      kwargs['state'] = eval_lib.load_state(path=self.path, tag=self.tag)
+    if self.path:
+      kwargs['state'] = saving.load_state_from_disk(self.path)
     return kwargs
 
 class OpponentType(enum.Enum):
@@ -371,6 +370,8 @@ def run(config: Config):
       **config.dolphin.to_kwargs(),
   )
 
+  if config.agent.path is not None:
+    raise ValueError('Main agent path is not used, use `restore` instead')
   main_agent_kwargs = config.agent.get_kwargs()
   main_agent_kwargs['state'] = rl_state
   agent_kwargs = {PORT: main_agent_kwargs}