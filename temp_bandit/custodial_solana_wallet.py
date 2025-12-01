@@ -117,10 +117,7 @@ def send_transaction(self, transaction: SolanaTransaction) -> Dict[str, str]:
         )
         
         # Create versioned transaction directly
-        versioned_transaction = VersionedTransaction(
-            message=message,
-            signatures=[]  # No signatures, let API handle signing
-        )
+        versioned_transaction = VersionedTransaction.new_unsigned(message)
         
         # Serialize and encode transaction
         serialized = base58.b58encode(bytes(versioned_transaction)).decode()