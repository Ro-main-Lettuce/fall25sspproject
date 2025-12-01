@@ -29,7 +29,7 @@
 )
 from marimo._server.router import APIRouter
 from marimo._server.uvicorn_utils import close_uvicorn
-from marimo._types.ids import ConsumerId, UIElementId
+from marimo._types.ids import ConsumerId
 
 if TYPE_CHECKING:
     from starlette.requests import Request
@@ -63,9 +63,7 @@ async def set_ui_element_values(
     body = await parse_request(request, cls=UpdateComponentValuesRequest)
     app_state.require_current_session().put_control_request(
         SetUIElementValueRequest(
-            object_ids=[
-                UIElementId(element_id) for element_id in body.object_ids
-            ],
+            object_ids=body.object_ids,
             values=body.values,
             token=str(uuid4()),
             request=HTTPRequest.from_request(request),