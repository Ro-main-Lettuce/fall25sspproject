@@ -1,3 +1,4 @@
+from typing import NoReturn
 from unittest.mock import Mock
 
 from crewai.utilities.events.base_events import BaseEvent
@@ -8,11 +9,11 @@ class TestEvent(BaseEvent):
     pass
 
 
-def test_specific_event_handler():
+def test_specific_event_handler() -> None:
     mock_handler = Mock()
 
     @crewai_event_bus.on(TestEvent)
-    def handler(source, event):
+    def handler(source, event) -> None:
         mock_handler(source, event)
 
     event = TestEvent(type=""test_event"")
@@ -21,11 +22,11 @@ def handler(source, event):
     mock_handler.assert_called_once_with(""source_object"", event)
 
 
-def test_wildcard_event_handler():
+def test_wildcard_event_handler() -> None:
     mock_handler = Mock()
 
     @crewai_event_bus.on(BaseEvent)
-    def handler(source, event):
+    def handler(source, event) -> None:
         mock_handler(source, event)
 
     event = TestEvent(type=""test_event"")
@@ -34,10 +35,11 @@ def handler(source, event):
     mock_handler.assert_called_once_with(""source_object"", event)
 
 
-def test_event_bus_error_handling(capfd):
+def test_event_bus_error_handling(capfd) -> None:
     @crewai_event_bus.on(BaseEvent)
-    def broken_handler(source, event):
-        raise ValueError(""Simulated handler failure"")
+    def broken_handler(source, event) -> NoReturn:
+        msg = ""Simulated handler failure""
+        raise ValueError(msg)
 
     event = TestEvent(type=""test_event"")
     crewai_event_bus.emit(""source_object"", event)