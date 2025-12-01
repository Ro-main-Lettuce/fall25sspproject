@@ -4,6 +4,7 @@
 
 import collections.abc
 import dataclasses
+import decimal
 import inspect
 import json
 import re
@@ -1558,7 +1559,7 @@ def is_tuple_type(t: GenericType) -> bool:
 
 
 def _determine_value_of_array_index(
-    var_type: GenericType, index: int | float | None = None
+    var_type: GenericType, index: int | float | decimal.Decimal | None = None
 ):
     """"""Determine the value of an array index.
 