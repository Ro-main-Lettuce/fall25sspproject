@@ -2,8 +2,8 @@
 Example demonstrating the new LLM generations and logprobs functionality.
 """"""
 
-from crewai import Agent, Task, Crew, LLM
-from crewai.utilities.xml_parser import extract_xml_content, extract_multiple_xml_tags
+from crewai import Agent, Task, LLM
+from crewai.utilities.xml_parser import extract_xml_content
 
 
 def example_multiple_generations():
@@ -133,7 +133,7 @@ def example_logprobs_analysis():
             print(f""Available logprobs data: {len(logprobs)} choices"")
             
         if usage:
-            print(f""
Token usage:"")
+            print(""
Token usage:"")
             print(f""Prompt tokens: {usage.get('prompt_tokens', 'N/A')}"")
             print(f""Completion tokens: {usage.get('completion_tokens', 'N/A')}"")
             print(f""Total tokens: {usage.get('total_tokens', 'N/A')}"")