@@ -158,10 +158,7 @@ def test_custodial_wallet_raw_transaction(custodial_api, test_email, solana_conn
     )
     
     # Create versioned transaction directly
-    versioned_transaction = VersionedTransaction(
-        message=message,
-        signatures=[]  # No signatures, let API handle signing
-    )
+    versioned_transaction = VersionedTransaction.new_unsigned(message)
     
     # Serialize and encode
     serialized = base58.b58encode(bytes(versioned_transaction)).decode()