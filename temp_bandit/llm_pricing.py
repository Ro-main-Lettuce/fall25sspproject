@@ -24,7 +24,7 @@ class LLMPricing:
         },
     }
 
-    DEFAULT_PRICE = {""input"": 0.01, ""output"": 0.03}  # デフォルト価格（不明なモデル用）
+    DEFAULT_PRICE = {""input"": 0, ""output"": 0}  # 不明なモデルは 0 = 情報なし
 
     @classmethod
     def calculate_cost(cls, provider: str, model: str, token_usage_input: int, token_usage_output: int) -> float: