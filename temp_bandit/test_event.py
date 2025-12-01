@@ -483,3 +483,47 @@ def get_handler(self, arg: Var[str]):
 
     w = Wrapper()
     _ = rx.input(on_change=w.get_handler)
+
+
+def test_decentralized_event_with_args():
+    """"""Test the decentralized event.""""""
+
+    class S(BaseState):
+        field: Field[str] = field("""")
+
+    @event
+    def e(s: S, arg: str):
+        s.field = arg
+
+    _ = rx.input(on_change=e(""foo""))
+
+
+def test_decentralized_event_no_args():
+    """"""Test the decentralized event with no args.""""""
+
+    class S(BaseState):
+        field: Field[str] = field("""")
+
+    @event
+    def e(s: S):
+        s.field = ""foo""
+
+    _ = rx.input(on_change=e())
+    _ = rx.input(on_change=e)
+
+
+class GlobalState(BaseState):
+    """"""Global state for testing decentralized events.""""""
+
+    field: Field[str] = field("""")
+
+
+@event
+def f(s: GlobalState, arg: str):
+    s.field = arg
+
+
+def test_decentralized_event_global_state():
+    """"""Test the decentralized event with a global state.""""""
+    _ = rx.input(on_change=f(""foo""))
+    _ = rx.input(on_change=f)