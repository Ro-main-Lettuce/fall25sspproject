@@ -265,12 +265,20 @@ def create_transaction_for_custodial_wallet(
         """"""Create a transaction using a Solana custodial wallet.
         
         Args:
-            locator: Wallet locator string
+            locator: Wallet locator string (email:address, phoneNumber:address, or userId:address)
             transaction: Encoded transaction data
         
         Returns:
             Transaction creation response
         """"""
+        # Format locator to use correct wallet type
+        if ""@"" in locator:
+            locator = f""email:{locator}:solana-mpc-wallet""
+        elif locator.startswith(""+""):
+            locator = f""phoneNumber:{locator}:solana-mpc-wallet""
+        else:
+            locator = f""userId:{locator}:solana-mpc-wallet""
+        
         endpoint = f""/wallets/{quote(locator)}/transactions""
         payload = {
             ""params"": {