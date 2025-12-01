@@ -104,8 +104,7 @@ def handle_templating(
 
     new_kwargs = kwargs.copy()
 
-    if mode in {Mode.GENAI_TOOLS, Mode.GENAI_STRUCTURED_OUTPUTS} and ""system"" in new_kwargs:
-        new_kwargs[""system""] = apply_template(new_kwargs[""system""], context)
+
 
     # Handle Cohere's message field
     if ""message"" in new_kwargs:
@@ -128,29 +127,9 @@ def handle_templating(
         return
 
     if ""messages"" in new_kwargs:
-        if mode in {Mode.GENAI_TOOLS, Mode.GENAI_STRUCTURED_OUTPUTS}:
-            templated_messages = []
-            for message in messages:
-                if isinstance(message, dict) and message.get(""role"") == ""system"":
-                    templated_msg = message.copy()
-                    if isinstance(message.get(""content""), str):
-                        templated_msg[""content""] = apply_template(message[""content""], context)
-                    elif isinstance(message.get(""content""), list):
-                        templated_content = []
-                        for item in message[""content""]:
-                            if isinstance(item, str):
-                                templated_content.append(apply_template(item, context))
-                            else:
-                                templated_content.append(item)
-                        templated_msg[""content""] = templated_content
-                    templated_messages.append(templated_msg)
-                else:
-                    templated_messages.append(process_message(message, context, Mode.TOOLS))
-            new_kwargs[""messages""] = templated_messages
-        else:
-            new_kwargs[""messages""] = [
-                process_message(message, context, mode) for message in messages
-            ]
+        new_kwargs[""messages""] = [
+            process_message(message, context, mode) for message in messages
+        ]
 
     elif ""contents"" in new_kwargs:
         new_kwargs[""contents""] = [