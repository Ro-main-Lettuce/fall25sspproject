@@ -36,6 +36,7 @@ def parse_subscript(node: TSNode, file_node_id, ctx, parent):
         return PyGenericType(node, file_node_id, ctx, parent)
     return SubscriptExpression(node, file_node_id, ctx, parent)
 
+
 PyExpressionMap = {
     ""string"": PyString,
     ""dictionary"": PyDict,