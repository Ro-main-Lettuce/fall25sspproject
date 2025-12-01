@@ -68,6 +68,7 @@ class Mode(enum.Enum):
     WRITER_JSON = ""writer_json""
     BEDROCK_TOOLS = ""bedrock_tools""
     BEDROCK_JSON = ""bedrock_json""
+    BEDROCK_MISTRAL_JSON = ""bedrock_mistral_json""
     PERPLEXITY_JSON = ""perplexity_json""
     OPENROUTER_STRUCTURED_OUTPUTS = ""openrouter_structured_outputs""
 
@@ -113,6 +114,7 @@ def json_modes(cls) -> set[""Mode""]:
             cls.FIREWORKS_JSON,
             cls.WRITER_JSON,
             cls.BEDROCK_JSON,
+            cls.BEDROCK_MISTRAL_JSON,
             cls.PERPLEXITY_JSON,
             cls.OPENROUTER_STRUCTURED_OUTPUTS,
             cls.MISTRAL_STRUCTURED_OUTPUTS,