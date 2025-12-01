@@ -8,7 +8,8 @@ class RequestersRouterGroup(group.RouterGroup):
     async def initialize(self) -> None:
         @self.route('', methods=['GET'])
         async def _() -> quart.Response:
-            return self.success(data={'requesters': self.ap.model_mgr.get_available_requesters_info()})
+            model_type = quart.request.args.get('type', '')
+            return self.success(data={'requesters': self.ap.model_mgr.get_available_requesters_info(model_type)})
 
         @self.route('/<requester_name>', methods=['GET'])
         async def _(requester_name: str) -> quart.Response: