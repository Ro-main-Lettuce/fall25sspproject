@@ -467,9 +467,9 @@ async def edit_file_contents(
 
             # Calculate new hash
             new_hash = self.calculate_hash(final_content)
-            
+
             validator_result = self._run_validator(file_path)
-            
+
             return {
                 ""result"": ""ok"",
                 ""file_hash"": new_hash,
@@ -592,14 +592,14 @@ async def insert_text_file_contents(
 
             # Calculate new hash
             new_hash = self.calculate_hash(final_content)
-            
+
             validator_result = self._run_validator(file_path)
-            
+
             return {
                 ""result"": ""ok"",
                 ""hash"": new_hash,
                 ""reason"": None,
-                ""validator_result"": validator_result
+                ""validator_result"": validator_result,
             }
 
         except FileNotFoundError:
@@ -746,9 +746,9 @@ async def delete_text_file_contents(
 
             # Calculate new hash
             new_hash = self.calculate_hash(final_content)
-            
+
             validator_result = self._run_validator(request.file_path)
-            
+
             return {
                 request.file_path: {
                     ""result"": ""ok"",
@@ -774,36 +774,40 @@ async def delete_text_file_contents(
                     ""hash"": None,
                 }
             }
+
     def _run_validator(self, file_path: str) -> Optional[Dict[str, Any]]:
         """"""Run validator command on the updated file if configured.
-        
+
         Args:
             file_path (str): Path to the file to validate
-            
+
         Returns:
             Optional[Dict[str, Any]]: Validation result or None if validation was not run
         """"""
-        logger.debug(f""Running validator with command: {self.validator_command} on file: {file_path}"")
+        logger.debug(
+            f""Running validator with command: {self.validator_command} on file: {file_path}""
+        )
         if not self.validator_command:
             logger.debug(""No validator command configured, skipping validation"")
             return None
-            
+
         try:
             import subprocess
-            logger.debug(f""Executing subprocess.run with: {[self.validator_command, file_path]}"")
+
+            logger.debug(
+                f""Executing subprocess.run with: {[self.validator_command, file_path]}""
+            )
             result = subprocess.run(
                 [self.validator_command, file_path],
                 capture_output=True,
                 text=True,
-                check=False
+                check=False,
             )
             return {
                 ""exit_code"": result.returncode,
                 ""stdout"": result.stdout,
-                ""stderr"": result.stderr
+                ""stderr"": result.stderr,
             }
         except Exception as e:
             logger.error(f""Error running validator command: {str(e)}"")
-            return {
-                ""error"": str(e)
-            }
+            return {""error"": str(e)}