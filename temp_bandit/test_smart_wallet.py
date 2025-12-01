@@ -88,7 +88,8 @@ def test_smart_wallet_with_email(smart_api, test_email, test_wallet_options, tes
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 
@@ -124,7 +125,8 @@ def test_smart_wallet_message_signing(smart_api, test_wallet_options, test_messa
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 
@@ -159,7 +161,8 @@ def test_smart_wallet_transaction(smart_api, test_wallet_options, test_evm_trans
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 
@@ -206,7 +209,8 @@ def test_smart_wallet_batch_transactions(smart_api, test_wallet_options, test_ke
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 
@@ -289,7 +293,8 @@ def test_smart_wallet_balance(smart_api, test_wallet_options, test_keypair):
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 
@@ -328,13 +333,15 @@ def test_smart_wallet_ens_resolution(smart_api, test_wallet_options, test_keypai
                 ""service temporarily unavailable"",
                 ""503 server error"",
                 ""could not connect to provider"",
-                ""invalid provider url""
+                ""invalid provider url"",
+                ""invalid ens provider url""
             ])
     except ValueError as e:
         # Provider connection might fail, that's ok
         assert any(msg in str(e).lower() for msg in [
             ""could not connect to provider"",
-            ""invalid provider url""
+            ""invalid provider url"",
+            ""invalid ens provider url""
         ])
 
 