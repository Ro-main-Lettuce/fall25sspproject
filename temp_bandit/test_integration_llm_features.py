@@ -75,7 +75,9 @@ def test_lite_agent_with_xml_extraction(self, mock_completion):
         )
 
         with patch.object(lite_agent, '_invoke_loop') as mock_invoke:
-            mock_invoke.return_value = response_with_xml
+            from crewai.agents.agent_action import AgentFinish
+            mock_agent_finish = AgentFinish(output=response_with_xml, text=response_with_xml)
+            mock_invoke.return_value = mock_agent_finish
             
             result = lite_agent.kickoff(""Analyze this problem"")
             