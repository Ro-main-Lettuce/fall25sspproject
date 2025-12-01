@@ -8,6 +8,9 @@
 from typing_extensions import Annotated
 
 import bentoml
+from bentoml._bentoml_sdk.service.factory import Service
+from bentoml._bentoml_sdk.service.openapi import generate_spec
+from bentoml._bentoml_sdk.service.openapi.specification import OpenAPISpecification
 from bentoml.validators import DataframeSchema
 from bentoml.validators import DType
 from bentoml.validators import Shape
@@ -142,12 +145,14 @@ def pandas_func(
 
 
 def test_api_decorator_openapi_overrides():
-    from bentoml._internal.service.factory import Service
-    from bentoml._internal.service.openapi import generate_spec
-    from bentoml._internal.service.openapi.specification import OpenAPISpecification
+    import typing as t
+
+    @bentoml.service(name=""test_overriden_service"")  # type: ignore[misc]
+    class TestOverridenService:  # type: ignore[misc]
+        def __init__(self) -> None:
+            self._service = t.cast(Service[t.Any], self)
+            self._service.config = {""name"": ""test_overriden_service""}
 
-    @bentoml.service(name=""test_overriden_service"")
-    class TestOverridenService(Service):
         @bentoml.api(
             openapi_overrides={
                 ""description"": ""My custom description"",
@@ -188,12 +193,14 @@ def predict(self, data: str) -> str:
 
 
 def test_api_decorator_parameter_overrides():
-    from bentoml._internal.service.factory import Service
-    from bentoml._internal.service.openapi import generate_spec
-    from bentoml._internal.service.openapi.specification import OpenAPISpecification
+    import typing as t
+
+    @bentoml.service(name=""test_parameter_service"")  # type: ignore[misc]
+    class TestParameterService:  # type: ignore[misc]
+        def __init__(self) -> None:
+            self._service = t.cast(Service[t.Any], self)
+            self._service.config = {""name"": ""test_parameter_service""}
 
-    @bentoml.service(name=""test_parameter_service"")
-    class TestParameterService(Service):
         @bentoml.api(
             openapi_overrides={
                 ""parameters"": [
@@ -244,12 +251,14 @@ def list_items(self, data: str) -> str:
 
 
 def test_api_decorator_response_overrides():
-    from bentoml._internal.service.factory import Service
-    from bentoml._internal.service.openapi import generate_spec
-    from bentoml._internal.service.openapi.specification import OpenAPISpecification
+    import typing as t
+
+    @bentoml.service(name=""test_response_service"")  # type: ignore[misc]
+    class TestResponseService:  # type: ignore[misc]
+        def __init__(self) -> None:
+            self._service = t.cast(Service[t.Any], self)
+            self._service.config = {""name"": ""test_response_service""}
 
-    @bentoml.service(name=""test_response_service"")
-    class TestResponseService(Service):
         @bentoml.api(
             openapi_overrides={
                 ""responses"": {
@@ -331,16 +340,13 @@ def process_data(self, data: str) -> str:
 
 
 def test_api_decorator_multiple_overrides():
-    from bentoml._internal.service import Service
-    from bentoml._internal.service.openapi import generate_spec
-    from bentoml._internal.service.openapi.specification import OpenAPISpecification
+    import typing as t
 
-    @bentoml.service(name=""test_multi_endpoint_service"")
-    class TestMultiEndpointService(Service):
-        def __init__(self):
-            super().__init__(
-                config={""name"": ""test_multi_endpoint_service""}, inner=self.__class__
-            )
+    @bentoml.service(name=""test_multi_endpoint_service"")  # type: ignore[misc]
+    class TestMultiEndpointService:  # type: ignore[misc]
+        def __init__(self) -> None:
+            self._service = t.cast(Service[t.Any], self)
+            self._service.config = {""name"": ""test_multi_endpoint_service""}
 
         @bentoml.api(
             openapi_overrides={
@@ -414,12 +420,15 @@ def test_api_decorator_invalid_overrides():
 
     import pytest
 
-    from bentoml._internal.service.factory import Service
-    from bentoml._internal.service.openapi import generate_spec
+    from bentoml._bentoml_sdk.service.openapi import generate_spec
 
     # Test invalid field name
-    @bentoml.service(name=""test_invalid_field_service"")
-    class TestInvalidFieldService(Service):
+    @bentoml.service(name=""test_invalid_field_service"")  # type: ignore[misc]
+    class TestInvalidFieldService:  # type: ignore[misc]
+        def __init__(self) -> None:
+            self._service = t.cast(Service[t.Any], self)
+            self._service.config = {""name"": ""test_invalid_field_service""}
+
         @bentoml.api(
             openapi_overrides={
                 ""invalid_field"": ""some value"",  # Invalid OpenAPI field name
@@ -434,7 +443,7 @@ def predict(self: t.Any, data: str) -> str:
 
     # Test invalid field value type
     @bentoml.service(name=""test_invalid_value_service"")
-    class TestInvalidValueService(Service):
+    class TestInvalidValueService:
         @bentoml.api(
             openapi_overrides={
                 ""parameters"": ""not a list"",  # Parameters must be a list
@@ -449,7 +458,7 @@ def predict(self: t.Any, data: str) -> str:
 
     # Test invalid nested schema
     @bentoml.service(name=""test_invalid_schema_service"")
-    class TestInvalidSchemaService(Service):
+    class TestInvalidSchemaService:
         @bentoml.api(
             openapi_overrides={
                 ""responses"": {
@@ -474,7 +483,7 @@ def predict(self: t.Any, data: str) -> str:
 
     # Test invalid response code
     @bentoml.service(name=""test_invalid_response_service"")
-    class TestInvalidResponseService(Service):
+    class TestInvalidResponseService:
         @bentoml.api(
             openapi_overrides={
                 ""responses"": {