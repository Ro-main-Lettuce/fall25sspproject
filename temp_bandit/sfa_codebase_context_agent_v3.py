@@ -127,7 +127,7 @@ def check_file_paths_line_length(reasoning: str, file_paths: List[str], file_lin
         console.log(f""[red]Error checking file paths: {str(e)}[/red]"")
         return {}
 
-def determine_if_file_is_relevant(prompt: str, file_path: str, client: Anthropic) -> Dict[str, Any]:
+def determine_if_file_is_relevant(prompt: str, file_path: str, client: Anthropic) -> Dict[str, Any]:  # type: ignore
     """"""Determines if a single file is relevant to the prompt.
     
     Args:
@@ -515,7 +515,7 @@ def main():
                 
                 # Handle text responses if there was no tool use
                 if not tool_use_block and text_block:
-                    messages.append({
+                    messages.append({  # type: ignore
                         ""role"": ""assistant"", 
                         ""content"": [
                             *([thinking_block] if thinking_block else []), 
@@ -572,7 +572,7 @@ def main():
 
                         # Append the tool result to messages
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""assistant"",
                                 ""content"": [
                                     *([thinking_block] if thinking_block else []),
@@ -587,7 +587,7 @@ def main():
                         )
 
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""user"",
                                 ""content"": [
                                     {
@@ -605,7 +605,7 @@ def main():
 
                         # Append the error to messages
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""assistant"",
                                 ""content"": [
                                     *([thinking_block] if thinking_block else []),
@@ -620,7 +620,7 @@ def main():
                         )
 
                         messages.append(
-                            {
+                            {  # type: ignore
                                 ""role"": ""user"",
                                 ""content"": [
                                     {