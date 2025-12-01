@@ -230,8 +230,8 @@ def test_serialize(value: Any, expected: str):
         (Color(color=""slate"", shade=1), '""var(--slate-1)""', True),
         (BaseSubclass, '""BaseSubclass""', True),
         (Path(), '"".""', True),
-        (decimal.Decimal(""123.456""), '""123.456""', True),
-        (decimal.Decimal(""-0.5""), '""-0.5""', True),
+        (decimal.Decimal(""123.456""), ""123.456"", True),
+        (decimal.Decimal(""-0.5""), ""-0.5"", True),
     ],
 )
 def test_serialize_var_to_str(value: Any, expected: str, exp_var_is_string: bool):