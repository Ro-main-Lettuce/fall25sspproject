@@ -40,7 +40,18 @@ def test_item_pagination_strategy(response_json, last_records, expected):
     response = MagicMock()
     response.json.return_value = response_json
 
-    assert strategy.next_page_token(response, last_records) == expected
+    # Calculate last_page_size based on last_records
+    last_page_size = len(last_records)
+
+    assert (
+        strategy.next_page_token(
+            response=response,
+            last_page_size=last_page_size,
+            last_record=None if not last_records else last_records[-1],
+            last_page_token_value=None,
+        )
+        == expected
+    )
 
 
 @pytest.mark.parametrize(
@@ -81,4 +92,15 @@ def test_item_cursor_pagination_strategy(response_json, last_records, expected):
     response = MagicMock()
     response.json.return_value = response_json
 
-    assert strategy.next_page_token(response, last_records) == expected
+    # Calculate last_page_size based on last_records
+    last_page_size = len(last_records)
+
+    assert (
+        strategy.next_page_token(
+            response=response,
+            last_page_size=last_page_size,
+            last_record=None if not last_records else last_records[-1],
+            last_page_token_value=None,
+        )
+        == expected
+    )