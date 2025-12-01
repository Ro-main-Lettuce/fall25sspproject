@@ -106,7 +106,7 @@ def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
                 tx_params[""paymasterInput""] = paymaster_input
 
             tx_hash = self._web3.eth.send_transaction(tx_params)
-            return self._wait_for_receipt(HexStr(tx_hash.hex()))
+            return self._wait_for_receipt(HexStr(tx_hash.to_0x_hex()))
 
         # Contract call
         function_name = transaction.get(""functionName"")
@@ -134,7 +134,7 @@ def send_transaction(self, transaction: EVMTransaction) -> Dict[str, str]:
         # Send the transaction
         tx_hash = contract_function(*args).transact(tx_params)
 
-        return self._wait_for_receipt(HexStr(tx_hash.hex()))
+        return self._wait_for_receipt(HexStr(tx_hash.to_0x_hex()))
 
     def read(self, request: EVMReadRequest) -> EVMReadResult:
         """"""Read data from a smart contract.""""""