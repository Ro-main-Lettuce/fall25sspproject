@@ -77,7 +77,9 @@ def get_token_by_ticker(self, ticker: str) -> Optional[str]:
         """"""Get token address by ticker symbol""""""
         try:
             if ticker.lower() in [""s"", ""S""]:
-                return ""0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE""
+                return self.WRAPPED_SONIC
+            elif ticker.lower() in [""eth"", ""ETH""]:
+                return self.WRAPPED_ETH
                 
             response = requests.get(
                 f""https://api.dexscreener.com/latest/dex/search?q={ticker}""
@@ -93,15 +95,7 @@ def get_token_by_ticker(self, ticker: str) -> Optional[str]:
             ]
             sonic_pairs.sort(key=lambda x: x.get(""fdv"", 0), reverse=True)
 
-            sonic_pairs = [
-                pair
-                for pair in sonic_pairs
-                if pair.get(""baseToken"", {}).get(""symbol"", """").lower() == ticker.lower()
-            ]
-
-            if sonic_pairs:
-                return sonic_pairs[0].get(""baseToken"", {}).get(""address"")
-            return None
+            return sonic_pairs[0].get(""baseToken"", {}).get(""address"") if sonic_pairs else None
 
         except Exception as error:
             logger.error(f""Error fetching token address: {str(error)}"")