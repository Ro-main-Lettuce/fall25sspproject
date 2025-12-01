@@ -13,15 +13,6 @@
 from agentops.config import Config
 from agentops.session.session import Session, SessionState
 
-# class TestNonInitializedSessions:
-#     def setup_method(self):
-#         self.api_key = ""11111111-1111-4111-8111-111111111111""
-#         self.event_type = ""test_event_type""
-#
-#     def test_non_initialized_doesnt_start_session(self, mock_req):
-#         session = agentops.start_session()
-#         assert session is None
-
 
 class TestSessionStart:
     def test_session_start(self):