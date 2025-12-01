@@ -59,6 +59,24 @@ class APIMethod(t.Generic[P, R]):
     doc: str | None = attrs.field(init=False)
     ctx_param: str | None = attrs.field(init=False)
     is_task: bool = attrs.field(default=False)
+    # Dictionary of user-provided overrides for the OpenAPI specification.
+    # This allows customizing any valid OpenAPI operation fields like description,
+    # tags, parameters, requestBody, responses, etc. The overrides are deep merged
+    # with the auto-generated specification, allowing partial customization while
+    # preserving auto-generated fields.
+    #
+    # Example:
+    #   openapi_overrides = {
+    #       ""description"": ""Custom API description"",
+    #       ""tags"": [""custom-tag""],
+    #       ""parameters"": [{""name"": ""version"", ""in"": ""query"", ""schema"": {""type"": ""string""}}],
+    #       ""responses"": {
+    #           ""200"": {
+    #               ""description"": ""Successful prediction"",
+    #               ""content"": {""application/json"": {""schema"": {""type"": ""object""}}}
+    #           }
+    #       }
+    #   }
     openapi_overrides: dict[str, t.Any] | None = attrs.field(default=None)
 
     @doc.default