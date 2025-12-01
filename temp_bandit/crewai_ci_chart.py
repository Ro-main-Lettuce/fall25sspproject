@@ -10,16 +10,15 @@
     if main_task.lower() == ""exit"":
         break
 
-    code_interpreter_tools = ComposioToolSet().get_tools([App.CODEINTERPRETER])
+    code_interpreter_tools = ComposioToolSet().get_tools(apps=[App.CODEINTERPRETER])
 
     code_interpreter_agent = Agent(
         role=""Python Code Interpreter Agent"",
         goal=f""""""Run I a code to get achieve a task given by the user"""""",
         backstory=""""""You are an agent that helps users run Python code."""""",
         verbose=True,
-        tools=code_interpreter_tools,
+        tools=list(code_interpreter_tools), # type: ignore
         llm=llm,
-        memory=True,
     )
 
     code_interpreter_task = Task(