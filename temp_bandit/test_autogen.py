@@ -176,7 +176,7 @@ def simple_workflow(ui: UI, params: dict[str, Any]) -> str:
         name=name,
     )
 
-    result = wf.run(
+    result = wf.run_workflow(
         name=name,
         ui=ui,
     )
@@ -276,7 +276,7 @@ def test(
     ) -> None:
         monkeypatch.setattr(""builtins.input"", InputMock([response] * 7))
 
-        result = wf.run(
+        result = wf.run_workflow(
             name=""test_workflow"",
             ui=ConsoleUI().create_workflow_ui(workflow_uuid=uuid4().hex),
             initial_message=""What is the weather in Zagreb right now?"",