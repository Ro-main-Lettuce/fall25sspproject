@@ -2,6 +2,7 @@
 import atexit
 import dataclasses
 import logging
+import os
 from typing import Dict, Mapping, Optional, Iterator
 
 import fancyflags as ff
@@ -27,7 +28,7 @@ def controller_type(self) -> melee.ControllerType:
     return melee.ControllerType.GCN_ADAPTER
 
   def menuing_kwargs(self) -> Dict:
-      return {}
+    return {}
 
 @dataclasses.dataclass
 class CPU(Player):
@@ -38,7 +39,7 @@ def controller_type(self) -> melee.ControllerType:
     return melee.ControllerType.STANDARD
 
   def menuing_kwargs(self) -> Dict:
-      return dict(character_selected=self.character, cpu_level=self.level)
+    return dict(character_selected=self.character, cpu_level=self.level)
 
 @dataclasses.dataclass
 class AI(Player):
@@ -48,7 +49,7 @@ def controller_type(self) -> melee.ControllerType:
     return melee.ControllerType.STANDARD
 
   def menuing_kwargs(self) -> Dict:
-      return dict(character_selected=self.character)
+    return dict(character_selected=self.character)
 
 def is_menu_state(gamestate: melee.GameState) -> bool:
   return gamestate.menu_state not in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]
@@ -146,7 +147,6 @@ def __init__(
 
     logging.info('Connecting to console...')
     if not console.connect():
-      import os
       logging.error(
           f""PID {os.getpid()}: failed to connect to the console""
           f"" {console.temp_dir} on port {slippi_port}"")