@@ -15,4 +15,4 @@ def test_bans_stream_record_extractor(
     test_url = f""https://{config['subdomain']}.zendesk.com/api/v2/chat/bans""
     requests_mock.get(test_url, json=bans_stream_record)
     test_response = requests.get(test_url)
-    assert ZendeskChatBansRecordExtractor().extract_records(test_response) == bans_stream_record_extractor_expected_output
+    assert list(ZendeskChatBansRecordExtractor().extract_records(test_response)) == bans_stream_record_extractor_expected_output