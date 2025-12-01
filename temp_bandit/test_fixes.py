@@ -40,7 +40,6 @@ def test_error_handling():
     """"""Test error handling with structured logging""""""
     print(""Testing error handling..."")
     
-    import logging
     logging.basicConfig(level=logging.ERROR)
     
     with crewai_event_bus.scoped_handlers():