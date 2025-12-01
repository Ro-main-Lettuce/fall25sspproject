@@ -281,6 +281,7 @@ def event_chain(tmp_path_factory) -> Generator[AppHarness, None, None]:
         app_source=EventChain,
     ) as harness:
         yield harness
+    os.environ.pop(""REFLEX_REACT_STRICT_MODE"", None)
 
 
 @pytest.fixture
@@ -317,6 +318,7 @@ def event_chain_strict(tmp_path_factory) -> Generator[AppHarness, None, None]:
         app_source=EventChain,
     ) as harness:
         yield harness
+    os.environ.pop(""REFLEX_REACT_STRICT_MODE"", None)
 
 
 @pytest.fixture