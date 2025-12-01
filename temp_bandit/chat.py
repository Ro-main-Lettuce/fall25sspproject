@@ -20,7 +20,6 @@
 from marimo._runtime.context.types import ContextNotInitializedError
 from marimo._runtime.functions import EmptyArgs, Function
 from marimo._runtime.requests import SetUIElementValueRequest
-from marimo._types.ids import UIElementId
 
 
 @dataclass
@@ -219,7 +218,7 @@ async def _send_prompt(self, args: SendMessageRequest) -> str:
             if isinstance(ctx, KernelRuntimeContext):
                 ctx._kernel.enqueue_control_request(
                     SetUIElementValueRequest(
-                        object_ids=[UIElementId(self._id)],
+                        object_ids=[self._id],
                         values=[{""messages"": self._chat_history}],
                         request=None,
                     )