@@ -13,6 +13,7 @@
 )
 
 from autogen.agentchat import ConversableAgent
+from autogen.events.base_event import BaseEvent
 from autogen.io import IOStream
 
 from ...base import (
@@ -226,15 +227,14 @@ def create_message(self) -> list[IOMessage]:
         return retval
 
 
-class IOStreamAdapter(IOStream):  # Explicitly inherit from IOStream
+class IOStreamAdapter:  # Implement IOStream Protocol
     def __init__(self, ui: UI) -> None:
         """"""Initialize the adapter with a ChatableIO object.
 
         Args:
             ui (ChatableIO): The ChatableIO object to adapt
 
         """"""
-        super().__init__()  # Initialize the IOStream base class
         self.ui = ui
         self.current_message = CurrentMessage(ui._workflow_uuid)
 