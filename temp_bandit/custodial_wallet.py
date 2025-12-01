@@ -1,8 +1,10 @@
 import asyncio
 from typing import Dict
 import base58
-from solana.transaction import Transaction, TransactionInstruction
+from solders.instruction import Instruction
+from solders.keypair import Keypair
 from solders.pubkey import Pubkey
+from solders.message import Message
 from solana.rpc.async_api import AsyncClient as AsyncSolanaClient
 from goat.classes.wallet_client_base import Balance, Signature
 from goat_wallets.solana import SolanaWalletClient, SolanaTransaction
@@ -91,19 +93,26 @@ async def send_transaction(self, transaction: SolanaTransaction) -> Dict[str, st
         Returns:
             Dict containing the transaction hash
         """"""
-        # Create transaction message
-        message = Transaction()
-        message.recent_blockhash = str(Pubkey.default())  # Placeholder
-        message.fee_payer = Pubkey.from_string(self._address)
+        # Convert instructions to solders Instructions
+        instructions = []
+        for instruction_dict in transaction[""instructions""]:
+            # Convert dictionary to solders Instruction
+            instruction = Instruction(
+                program_id=instruction_dict[""program_id""],
+                accounts=instruction_dict[""accounts""],
+                data=instruction_dict[""data""]
+            )
+            instructions.append(instruction)
         
-        # Add instructions
-        for instruction in transaction[""instructions""]:
-            message.add(TransactionInstruction.from_legacy(instruction))
+        # Create message using solders Message
+        message = Message(
+            instructions=instructions,
+            payer=Pubkey.from_string(self._address),
+            recent_blockhash=str(Pubkey.default())  # Placeholder
+        )
         
         # Serialize and encode transaction
-        serialized = base58.b58encode(
-            bytes(message.serialize())
-        ).decode()
+        serialized = base58.b58encode(bytes(message)).decode()
         
         # Create and submit transaction
         response = await self._client.create_transaction_for_custodial_wallet(