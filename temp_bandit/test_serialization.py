@@ -1,6 +1,4 @@
 from datetime import date, datetime
-from typing import List
-from unittest.mock import Mock
 
 import pytest
 from pydantic import BaseModel
@@ -19,11 +17,11 @@ class Person(BaseModel):
     age: int
     address: Address
     birthday: date
-    skills: List[str]
+    skills: list[str]
 
 
 @pytest.mark.parametrize(
-    ""test_input,expected"",
+    (""test_input"", ""expected""),
     [
         ({""text"": ""hello world""}, {""text"": ""hello world""}),
         ({""number"": 42}, {""number"": 42}),
@@ -36,33 +34,33 @@ class Person(BaseModel):
         ({""nested"": [1, [2, 3], {4, 5}]}, {""nested"": [1, [2, 3], [4, 5]]}),
     ],
 )
-def test_basic_serialization(test_input, expected):
+def test_basic_serialization(test_input, expected) -> None:
     result = to_serializable(test_input)
     assert result == expected
 
 
 @pytest.mark.parametrize(
-    ""input_date,expected"",
+    (""input_date"", ""expected""),
     [
         (date(2024, 1, 1), ""2024-01-01""),
         (datetime(2024, 1, 1, 12, 30), ""2024-01-01T12:30:00""),
     ],
 )
-def test_temporal_serialization(input_date, expected):
+def test_temporal_serialization(input_date, expected) -> None:
     result = to_serializable({""date"": input_date})
     assert result[""date""] == expected
 
 
 @pytest.mark.parametrize(
-    ""key,value,expected_key_type"",
+    (""key"", ""value"", ""expected_key_type""),
     [
         ((""tuple"", ""key""), ""value"", str),
         (None, ""value"", str),
         (123, ""value"", str),
         (""normal"", ""value"", str),
     ],
 )
-def test_dictionary_key_serialization(key, value, expected_key_type):
+def test_dictionary_key_serialization(key, value, expected_key_type) -> None:
     result = to_serializable({key: value})
     assert len(result) == 1
     result_key = next(iter(result.keys()))
@@ -71,19 +69,19 @@ def test_dictionary_key_serialization(key, value, expected_key_type):
 
 
 @pytest.mark.parametrize(
-    ""callable_obj,expected_in_result"",
+    (""callable_obj"", ""expected_in_result""),
     [
         (lambda x: x * 2, ""lambda""),
         (str.upper, ""upper""),
     ],
 )
-def test_callable_serialization(callable_obj, expected_in_result):
+def test_callable_serialization(callable_obj, expected_in_result) -> None:
     result = to_serializable({""func"": callable_obj})
     assert isinstance(result[""func""], str)
     assert expected_in_result in result[""func""].lower()
 
 
-def test_pydantic_model_serialization():
+def test_pydantic_model_serialization() -> None:
     address = Address(street=""123 Main St"", city=""Tech City"", country=""Pythonia"")
 
     person = Person(
@@ -108,8 +106,8 @@ def test_pydantic_model_serialization():
     )
 
 
-def test_depth_limit():
-    """"""Test max depth handling with a deeply nested structure""""""
+def test_depth_limit() -> None:
+    """"""Test max depth handling with a deeply nested structure.""""""
 
     def create_nested(depth):
         if depth == 0:
@@ -124,15 +122,15 @@ def create_nested(depth):
             ""next"": {
                 ""next"": {
                     ""next"": {
-                        ""next"": ""{'next': {'next': {'next': {'next': {'next': 'value'}}}}}""
-                    }
-                }
-            }
-        }
+                        ""next"": ""{'next': {'next': {'next': {'next': {'next': 'value'}}}}}"",
+                    },
+                },
+            },
+        },
     }
 
 
-def test_exclude_keys():
+def test_exclude_keys() -> None:
     result = to_serializable({""key1"": ""value1"", ""key2"": ""value2""}, exclude={""key1""})
     assert result == {""key2"": ""value2""}
 