@@ -28,6 +28,8 @@ class Report(SchemaBaseModel):
     token_usage_input: int | None = None  # 入力トークン使用量
     token_usage_output: int | None = None  # 出力トークン使用量
     estimated_cost: float | None = None  # 推定コスト（USD）
+    provider: str | None = None  # LLMプロバイダー
+    model: str | None = None  # LLMモデル
 
     @property
     def is_publicly_visible(self) -> bool: