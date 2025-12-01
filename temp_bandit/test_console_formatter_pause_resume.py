@@ -114,3 +114,38 @@ def test_pause_resume_state_initialization(self):
         
         assert hasattr(formatter, '_live_paused')
         assert not formatter._live_paused
+
+    def test_stop_live_with_active_session(self):
+        """"""Test stopping Live session when one is active.""""""
+        formatter = ConsoleFormatter()
+        
+        mock_live = MagicMock(spec=Live)
+        formatter._live = mock_live
+        
+        formatter.stop_live()
+        
+        mock_live.stop.assert_called_once()
+        assert formatter._live is None
+
+    def test_stop_live_with_no_session(self):
+        """"""Test stopping Live session when none exists.""""""
+        formatter = ConsoleFormatter()
+        
+        formatter._live = None
+        
+        formatter.stop_live()
+        
+        assert formatter._live is None
+
+    def test_stop_live_multiple_calls(self):
+        """"""Test multiple calls to stop_live are safe.""""""
+        formatter = ConsoleFormatter()
+        
+        mock_live = MagicMock(spec=Live)
+        formatter._live = mock_live
+        
+        formatter.stop_live()
+        formatter.stop_live()
+        
+        mock_live.stop.assert_called_once()
+        assert formatter._live is None