@@ -19,9 +19,8 @@
     input_guardrail,
 )
 
-# Initialize agentops and import the guardrail decorator
+# Initialize agentops
 import agentops
-from agentops import guardrail
 
 # Load API keys
 import os
@@ -36,7 +35,7 @@
 agentops.init(api_key=os.environ[""AGENTOPS_API_KEY""], tags=[""agentops-example""])
 
 
-# OpenAI Agents SDK guardrail example with agentops guardrails decorator for observability
+# OpenAI Agents SDK guardrail example with AgentOps observability
 class MathHomeworkOutput(BaseModel):
     is_math_homework: bool
     reasoning: str
@@ -50,7 +49,6 @@ class MathHomeworkOutput(BaseModel):
 
 
 @input_guardrail
-@guardrail(spec=""input"")  # Specify guardrail type as input or output
 async def math_guardrail(
     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
 ) -> GuardrailFunctionOutput: