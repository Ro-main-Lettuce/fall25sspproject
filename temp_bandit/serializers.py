@@ -400,19 +400,6 @@ def serialize_decimal(value: decimal.Decimal) -> float:
     return float(value)
 
 
-@serializer(to=str)
-def serialize_decimal_to_str(value: decimal.Decimal) -> str:
-    """"""Serialize a Decimal to a string.
-
-    Args:
-        value: The Decimal to serialize.
-
-    Returns:
-        The serialized Decimal as a string.
-    """"""
-    return str(value)
-
-
 @serializer(to=str)
 def serialize_color(color: Color) -> str:
     """"""Serialize a color.