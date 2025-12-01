@@ -78,6 +78,8 @@ def get_span_kind(span: Any) -> SpanKind:
         return SpanKind.CONSUMER
     elif span_type in [""FunctionSpanData"", ""GenerationSpanData"", ""ResponseSpanData""]:
         return SpanKind.CLIENT
+    elif span_type in [""HandoffSpanData"", ""GuardrailSpanData""]:
+        return SpanKind.INTERNAL
     else:
         return SpanKind.INTERNAL
 