@@ -432,6 +432,7 @@ def test_guardrail_span_attributes(self):
 
     def test_guardrail_span_attributes_without_optional_fields(self):
         """"""Test extraction of attributes from a GuardrailSpanData object without optional fields""""""
+
         # Create a simple class instead of MagicMock to avoid automatic attribute creation
         class GuardrailSpanData:
             def __init__(self):