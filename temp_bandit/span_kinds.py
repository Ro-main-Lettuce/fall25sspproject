@@ -13,7 +13,6 @@ class AgentOpsSpanKindValues(Enum):
     AGENT = ""agent""
     TOOL = ""tool""
     LLM = ""llm""
-    TEAM = ""team""
     CHAIN = ""chain""
     TEXT = ""text""
     GUARDRAIL = ""guardrail""
@@ -42,7 +41,6 @@ class SpanKind:
     AGENT = AgentOpsSpanKindValues.AGENT.value
     TOOL = AgentOpsSpanKindValues.TOOL.value
     LLM = AgentOpsSpanKindValues.LLM.value
-    TEAM = AgentOpsSpanKindValues.TEAM.value
     UNKNOWN = AgentOpsSpanKindValues.UNKNOWN.value
     CHAIN = AgentOpsSpanKindValues.CHAIN.value
     TEXT = AgentOpsSpanKindValues.TEXT.value