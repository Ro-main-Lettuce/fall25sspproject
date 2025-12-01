@@ -1,12 +1,12 @@
-# Google ADK Example: Human Approval Workflow with AgentOps
-# This notebook demonstrates a complete human approval workflow using the Google ADK (Agent Development Kit), integrated with AgentOps for observability.
+# Google ADK Example: Automated Approval Workflow with AgentOps
+# This notebook demonstrates a complete automated approval workflow using the Google ADK (Agent Development Kit), integrated with AgentOps for observability.
 #
 # **Key Features:**
 # - **Sequential Agent Processing:** The workflow uses multiple agents chained together to handle different stages of the approval process.
-# - **External Tool Integration:** An agent interacts with an external tool that simulates (or in this version, directly prompts for) human approval.
+# - **External Tool Integration:** An agent interacts with an external tool that provides automated approval decisions based on amount and reason analysis.
 # - **Session State Management:** Information is passed between agents and persisted using session state.
 # - **AgentOps Observability:** All agent actions, tool calls, and LLM interactions are traced and can be viewed in your AgentOps dashboard.
-# - **Interactive Human Input:** The approval step now requires direct input from the user.
+# - **Automated Decision Making:** The approval system automatically approves or rejects requests based on configurable business rules.
 # ## 1. Setup and Dependencies
 # First, let's install the necessary libraries if they are not already present and import them.
 # %pip install google-adk agentops python-dotenv nest_asyncio asyncio
@@ -31,14 +31,19 @@
 AGENTOPS_API_KEY = os.getenv(""AGENTOPS_API_KEY"") or ""your_agentops_api_key_here""
 
 # Initialize AgentOps - Just 2 lines!
-agentops.init(AGENTOPS_API_KEY, trace_name=""adk-human-approval-notebook"", auto_start_session=False)
+agentops.init(
+    AGENTOPS_API_KEY,
+    trace_name=""adk-automated-approval-notebook"",
+    auto_start_session=False,
+    tags=[""google-adk"", ""automated-approval"", ""agentops-example""],
+)
 
 # Define some constants for our application.
-APP_NAME = ""human_approval_app_notebook""
+APP_NAME = ""automated_approval_app_notebook""
 USER_ID = ""test_user_notebook_123""
-SESSION_ID = ""approval_session_notebook_456""
+SESSION_ID = ""automated_approval_session_notebook_456""
 MODEL_NAME = ""gemini-1.5-flash""
-agentops.start_trace(trace_name=APP_NAME, tags=[""google_adk"", ""notebook""])
+tracer = agentops.start_trace(trace_name=APP_NAME, tags=[""google_adk"", ""notebook""])
 
 
 # ## 3. Define Schemas
@@ -53,23 +58,51 @@ class ApprovalDecision(BaseModel):
     comments: str = Field(description=""Additional comments from the approver"")
 
 
-# ## 4. External Approval Tool (with Human Interaction)
-# This tool now directly prompts the user for an approval decision. In a real-world scenario, this might involve sending a notification to an approver and waiting for their response through a UI or API.
+# ## 4. External Approval Tool (Automated Decision Making)
+# This tool automatically makes approval decisions based on configurable business rules. It analyzes the amount and reason to determine whether to approve or reject the request. In a real-world scenario, this could be integrated with more sophisticated rule engines or ML models for decision making.
 async def external_approval_tool(amount: float, reason: str) -> str:
     """"""
-    Prompts for human approval and returns the decision as a JSON string.
+    Automated approval system that returns approval decisions based on amount and reason analysis.
     """"""
-    print(""🔔 HUMAN APPROVAL REQUIRED:"")
+    print(""🤖 AUTOMATED APPROVAL SYSTEM:"")
     print(f""   Amount: ${amount:,.2f}"")
     print(f""   Reason: {reason}"")
+
+    # Automated decision logic
     decision = """"
-    while decision.lower() not in [""approved"", ""rejected""]:
-        decision = input(""   Enter decision (approved/rejected): "").strip().lower()
-        if decision.lower() not in [""approved"", ""rejected""]:
-            print(""   Invalid input. Please enter 'approved' or 'rejected'."")
-    comments = input(""   Enter comments (optional): "").strip()
+    comments = """"
+
+    reason_lower = reason.lower()
+    high_priority_keywords = [""critical"", ""urgent"", ""emergency"", ""security"", ""compliance"", ""license""]
+    business_keywords = [""conference"", ""training"", ""team"", ""software"", ""equipment"", ""travel""]
+
+    # Check for high priority keywords first (overrides amount limits)
+    if any(keyword in reason_lower for keyword in high_priority_keywords):
+        decision = ""approved""
+        comments = ""Auto-approved: High priority business need identified""
+
+    # Auto-approve small amounts
+    elif amount <= 1000:
+        decision = ""approved""
+        comments = ""Auto-approved: Amount under $1,000 threshold""
+
+    # Auto-reject very large amounts without high priority justification
+    elif amount > 10000:
+        decision = ""rejected""
+        comments = ""Auto-rejected: Amount exceeds $10,000 limit without high priority justification""
+
+    # Medium amounts: analyze reason keywords
+    else:
+        if any(keyword in reason_lower for keyword in business_keywords):
+            decision = ""approved""
+            comments = ""Auto-approved: Standard business expense""
+        else:
+            # Default to approval for reasonable amounts with unclear reasons
+            decision = ""approved""
+            comments = ""Auto-approved: Amount within reasonable range""
+
     print(f""   Decision: {decision.upper()}"")
-    print(f""   Comments: {comments if comments else 'N/A'}"")
+    print(f""   Comments: {comments}"")
     return json.dumps({""decision"": decision, ""comments"": comments, ""amount"": amount, ""reason"": reason})
 
 
@@ -97,16 +130,16 @@ async def external_approval_tool(amount: float, reason: str) -> str:
     output_key=""request_prepared"",
 )
 
-# Agent 2: Request human approval using the tool
+# Agent 2: Request automated approval using the tool
 request_approval = LlmAgent(
     model=MODEL_NAME,
-    name=""RequestHumanApprovalAgent"",
-    description=""Calls the external approval system with prepared request details"",
-    instruction=""""""You are a human approval request agent.
+    name=""RequestAutomatedApprovalAgent"",
+    description=""Calls the external automated approval system with prepared request details"",
+    instruction=""""""You are an automated approval request agent.
         Your task:
         1. Get the 'approval_amount' and 'approval_reason' from the session state
         2. Use the external_approval_tool with these values
-        3. Store the approval decision in session state with key 'human_decision'
+        3. Store the approval decision in session state with key 'automated_decision'
         4. Respond with the approval status
     Always use the exact values from the session state for the tool call.
     """""",
@@ -118,10 +151,10 @@ async def external_approval_tool(amount: float, reason: str) -> str:
 process_decision = LlmAgent(
     model=MODEL_NAME,
     name=""ProcessDecisionAgent"",
-    description=""Processes the human approval decision and provides final response"",
+    description=""Processes the automated approval decision and provides final response"",
     instruction=""""""You are a decision processing agent.
         Your task:
-        1. Check the 'human_decision' from session state
+        1. Check the 'automated_decision' from session state
         2. Parse the approval decision JSON
         3. If approved: congratulate and provide next steps
         4. If rejected: explain the rejection and suggest alternatives
@@ -135,8 +168,8 @@ async def external_approval_tool(amount: float, reason: str) -> str:
 # ## 6. Create Sequential Workflow
 # Combine the agents into a sequential workflow. The `SequentialAgent` ensures that the sub-agents are executed in the specified order.
 approval_workflow = SequentialAgent(
-    name=""HumanApprovalWorkflowNotebook"",
-    description=""Complete workflow for processing approval requests with human oversight"",
+    name=""AutomatedApprovalWorkflowNotebook"",
+    description=""Complete workflow for processing approval requests with automated decision making"",
     sub_agents=[prepare_request, request_approval, process_decision],
 )
 
@@ -191,12 +224,14 @@ async def run_approval_workflow_notebook(user_request: str, session_id: str):
 # This cell contains the main logic to run the workflow with a few test cases. Each test case will run in its own session.
 async def main_notebook():
     test_requests = [
-        ""I need approval for $750 for team lunch and celebrations"",
-        ""Please approve $3,000 for a conference ticket and travel expenses"",
-        ""I need $12,000 approved for critical software licenses renewal"",
+        ""I need approval for $750 for team lunch and celebrations"",  # Should auto-approve: under $1,000
+        ""Please approve $3,000 for a conference ticket and travel expenses"",  # Should auto-approve: business keywords
+        ""I need $12,000 approved for critical software licenses renewal"",  # Should auto-approve: high priority keywords despite high amount
+        ""Please approve $15,000 for office decoration and furniture"",  # Should auto-reject: over $10,000 without high priority keywords
+        ""I need $5,000 for urgent security system upgrade"",  # Should auto-approve: high priority keywords
     ]
     for i, request in enumerate(test_requests, 1):
-        current_session_id = f""approval_session_notebook_{456 + i - 1}""
+        current_session_id = f""automated_approval_session_notebook_{456 + i - 1}""
         # Create the session before running the workflow
         await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=current_session_id)
         print(f""Created session: {current_session_id}"")
@@ -209,3 +244,13 @@ async def main_notebook():
 except Exception as e:
     print(f""Error: {e}"")
     agentops.end_trace(end_state=""Error"")
+
+# Let's check programmatically that spans were recorded in AgentOps
+print(""
"" + ""="" * 50)
+print(""Now let's verify that our LLM calls were tracked properly..."")
+try:
+    agentops.validate_trace_spans(trace_context=tracer)
+    print(""
✅ Success! All LLM spans were properly recorded in AgentOps."")
+except agentops.ValidationError as e:
+    print(f""
❌ Error validating spans: {e}"")
+    raise