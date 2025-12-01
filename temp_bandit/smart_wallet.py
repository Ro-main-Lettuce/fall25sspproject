@@ -97,14 +97,41 @@ def __init__(
         super().__init__()
         self._address = address
         self._client = api_client
+        
+        # Validate chain
+        if chain not in [""base-sepolia"", ""ethereum"", ""polygon"", ""avalanche"", ""arbitrum""]:
+            raise ValueError(f""Invalid chain: {chain}"")
         self._chain = chain
+        
+        # Validate signer
+        if isinstance(signer, str):
+            if not signer.startswith(""0x""):
+                raise ValueError(""Invalid custodial signer address"")
+        elif isinstance(signer, dict):
+            if not all(k in signer for k in [""secretKey"", ""address""]):
+                raise ValueError(""Invalid keypair signer: missing secretKey or address"")
+            if not signer[""address""].startswith(""0x""):
+                raise ValueError(""Invalid keypair signer address"")
+        else:
+            raise ValueError(""Invalid signer type"")
         self._signer = signer
         
         # Initialize Web3 providers
-        self._w3 = Web3(HTTPProvider(provider_url))
+        try:
+            self._w3 = Web3(HTTPProvider(provider_url))
+            if not self._w3.is_connected():
+                raise ValueError(""Could not connect to provider"")
+        except Exception as e:
+            raise ValueError(f""Invalid provider URL: {e}"")
+            
         if ens_provider_url:
-            ens_w3 = Web3(HTTPProvider(ens_provider_url))
-            self._ens = ENS.from_web3(ens_w3)
+            try:
+                ens_w3 = Web3(HTTPProvider(ens_provider_url))
+                if not ens_w3.is_connected():
+                    raise ValueError(""Could not connect to ENS provider"")
+                self._ens = ENS.from_web3(ens_w3)
+            except Exception as e:
+                raise ValueError(f""Invalid ENS provider URL: {e}"")
         else:
             self._ens = None
         