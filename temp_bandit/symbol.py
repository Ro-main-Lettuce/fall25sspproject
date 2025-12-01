@@ -54,7 +54,7 @@ class Symbol(Usable[Statement[CodeBlock]], Generic[Parent, TCodeBlock]):
     """"""
 
     symbol_type: SymbolType
-    node_type: Literal[""SYMBOL""] = NodeType.SYMBOL.value
+    node_type: Literal[""SYMBOL""] = ""SYMBOL""
 
     def __init__(
         self,