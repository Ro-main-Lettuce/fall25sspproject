@@ -145,7 +145,7 @@ def get_generated_imports():
 from codegen.sdk.python.statements.with_statement import WithStatement
 from codegen.sdk.python.symbol import PySymbol
 from codegen.sdk.python.symbol_groups.comment_group import PyCommentGroup
-from codegen.sdk.python.symbol_groups.dict import PyDict
+from codegen.sdk.python.symbol_groups.dict import merge
 from codegen.sdk.typescript.assignment import TSAssignment
 from codegen.sdk.typescript.class_definition import TSClass
 from codegen.sdk.typescript.detached_symbols.code_block import TSCodeBlock