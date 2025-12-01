@@ -400,7 +400,7 @@ def main():
                 
                 # Handle text responses if there was no tool use
                 if not tool_use_block and text_block:
-                    messages.append({
+                    messages.append({  # type: ignore
                         ""role"": ""assistant"", 
                         ""content"": [
                             *([thinking_block] if thinking_block else []), 
@@ -452,7 +452,7 @@ def main():
 
                         # Append the tool result to messages
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""assistant"",
                                 ""content"": [
                                     *([thinking_block] if thinking_block else []),
@@ -467,7 +467,7 @@ def main():
                         )
 
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""user"",
                                 ""content"": [
                                     {
@@ -485,7 +485,7 @@ def main():
 
                         # Append the error to messages
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""assistant"",
                                 ""content"": [
                                     *([thinking_block] if thinking_block else []),
@@ -500,7 +500,7 @@ def main():
                         )
 
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""user"",
                                 ""content"": [
                                     {
@@ -518,4 +518,4 @@ def main():
 
 
 if __name__ == ""__main__"":
-    main()
\ No newline at end of file
+    main()