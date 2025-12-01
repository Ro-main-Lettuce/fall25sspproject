@@ -311,30 +311,7 @@ def test_end2end():
         # First prepare the bot to get the typespec
         prepared_bot = application.prepare_bot([""Create a bot that does something please""])
         # Then update the bot to get the full ApplicationOut object
-        typespec_definitions = prepared_bot.typespec.typespec_definitions
-        if typespec_definitions is None:
-            print(""Warning: typespec_definitions is None, using fallback"")
-            typespec_definitions = """"""
-            model InputMessage {
-                content: string;
-            }
-
-            model ResponseMessage {
-                reply: string;
-            }
-
-            interface SimpleResponseBot {
-                @scenario(\""\""\""
-                Given a user input, the bot should generate a response
-                When the user input is a string, the bot should generate a response
-                When the user input is a number, the bot should generate a response
-                When the user input is a mixed input, the bot should generate a response
-                \""\""\"")
-                @llm_func(""process user input and generate response"")
-                processInput(options: InputMessage): ResponseMessage;
-            }
-            """"""
-        my_bot = application.update_bot(typespec_definitions)
+        my_bot = application.update_bot(prepared_bot.typespec.typespec_definitions)
 
         interpolator = Interpolator(os.path.join(os.path.dirname(os.path.abspath(__file__)), ""..""))
         interpolator.bake(my_bot, tempdir)