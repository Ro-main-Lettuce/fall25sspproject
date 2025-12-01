@@ -1,6 +1,7 @@
 import threading
-from contextlib import contextmanager
-from typing import Any, Callable, Dict, List, Type, TypeVar, cast
+from collections.abc import Callable
+from contextlib import contextmanager, suppress
+from typing import Any, TypeVar, cast
 
 from blinker import Signal
 
@@ -11,8 +12,7 @@
 
 
 class CrewAIEventsBus:
-    """"""
-    A singleton event bus that uses blinker signals for event handling.
+    """"""A singleton event bus that uses blinker signals for event handling.
     Allows both internal (Flow/Crew) and external event handling.
     """"""
 
@@ -23,20 +23,19 @@ def __new__(cls):
         if cls._instance is None:
             with cls._lock:
                 if cls._instance is None:  # prevent race condition
-                    cls._instance = super(CrewAIEventsBus, cls).__new__(cls)
+                    cls._instance = super().__new__(cls)
                     cls._instance._initialize()
         return cls._instance
 
     def _initialize(self) -> None:
-        """"""Initialize the event bus internal state""""""
+        """"""Initialize the event bus internal state.""""""
         self._signal = Signal(""crewai_event_bus"")
-        self._handlers: Dict[Type[BaseEvent], List[Callable]] = {}
+        self._handlers: dict[type[BaseEvent], list[Callable]] = {}
 
     def on(
-        self, event_type: Type[EventT]
+        self, event_type: type[EventT],
     ) -> Callable[[Callable[[Any, EventT], None]], Callable[[Any, EventT], None]]:
-        """"""
-        Decorator to register an event handler for a specific event type.
+        """"""Decorator to register an event handler for a specific event type.
 
         Usage:
             @crewai_event_bus.on(AgentExecutionCompletedEvent)
@@ -53,46 +52,41 @@ def decorator(
             if event_type not in self._handlers:
                 self._handlers[event_type] = []
             self._handlers[event_type].append(
-                cast(Callable[[Any, EventT], None], handler)
+                cast(""Callable[[Any, EventT], None]"", handler),
             )
             return handler
 
         return decorator
 
     def emit(self, source: Any, event: BaseEvent) -> None:
-        """"""
-        Emit an event to all registered handlers
+        """"""Emit an event to all registered handlers.
 
         Args:
             source: The object emitting the event
             event: The event instance to emit
+
         """"""
         for event_type, handlers in self._handlers.items():
             if isinstance(event, event_type):
                 for handler in handlers:
-                    try:
+                    with suppress(Exception):
                         handler(source, event)
-                    except Exception as e:
-                        print(
-                            f""[EventBus Error] Handler '{handler.__name__}' failed for event '{event_type.__name__}': {e}""
-                        )
 
         self._signal.send(source, event=event)
 
     def register_handler(
-        self, event_type: Type[EventTypes], handler: Callable[[Any, EventTypes], None]
+        self, event_type: type[EventTypes], handler: Callable[[Any, EventTypes], None],
     ) -> None:
-        """"""Register an event handler for a specific event type""""""
+        """"""Register an event handler for a specific event type.""""""
         if event_type not in self._handlers:
             self._handlers[event_type] = []
         self._handlers[event_type].append(
-            cast(Callable[[Any, EventTypes], None], handler)
+            cast(""Callable[[Any, EventTypes], None]"", handler),
         )
 
     @contextmanager
     def scoped_handlers(self):
-        """"""
-        Context manager for temporary event handling scope.
+        """"""Context manager for temporary event handling scope.
         Useful for testing or temporary event handling.
 
         Usage: