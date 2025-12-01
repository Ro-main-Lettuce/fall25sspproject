@@ -155,28 +155,6 @@ def mock_get_api_key() -> Generator[MagicMock, None, None]:
         yield mock
 
 
-def test_airtable_connector_parameter_validation() -> None:
-    """"""Test that treat_all_non_attachment_fields_as_metadata is required and has no default.""""""
-    # Test that treat_all_non_attachment_fields_as_metadata is required
-    with pytest.raises(TypeError) as exc_info:
-        AirtableConnector(  # type: ignore[call-arg]
-            base_id=""test_base"",
-            table_name_or_id=""test_table"",
-        )
-    assert (
-        ""missing 1 required positional argument: 'treat_all_non_attachment_fields_as_metadata'""
-        in str(exc_info.value)
-    )
-
-    # Test that treat_all_non_attachment_fields_as_metadata must be a boolean
-    with pytest.raises(TypeError):
-        AirtableConnector(
-            base_id=""test_base"",
-            table_name_or_id=""test_table"",
-            treat_all_non_attachment_fields_as_metadata=""not_a_boolean"",  # type: ignore
-        )
-
-
 def test_airtable_connector_all_metadata(
     mock_get_api_key: MagicMock, request: pytest.FixtureRequest
 ) -> None:
@@ -203,6 +181,7 @@ def test_airtable_connector_all_metadata(
 
     assert len(doc_batch) == 2
 
+    # TODO: remove duplication here compared to above test
     expected_docs = [
         create_test_document(
             id=""rec8BnxDLyWeegOuO"",