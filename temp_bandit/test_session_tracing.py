@@ -3,27 +3,10 @@
 
 import agentops
 
-
 pytestmark = [pytest.mark.skip]
 
 
-@pytest.fixture
-def session_generator():
-    """"""Fixture that provides a session generator with automatic cleanup""""""
-    sessions = []
-    
-    def create_session(tags=None):
-        if tags is None:
-            tags = [""test-session""]
-        session = agentops.start_session(tags=tags)
-        sessions.append(session)
-        return session
-    
-    yield create_session
-    
-    # Cleanup all sessions created during the test
-    for session in sessions:
-        session.end()
+
 
 
 def test_basic_span_propagation(session_generator):