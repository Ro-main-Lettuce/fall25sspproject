@@ -1,4 +1,3 @@
-from dataclasses import dataclass
 from typing import TYPE_CHECKING, Generic, Self, TypeVar
 
 from codegen.sdk.core.autocommit import reader
@@ -9,11 +8,8 @@
 from codegen.shared.decorators.docs import apidoc
 
 if TYPE_CHECKING:
-    from codegen.sdk.core.class_definition import Class
     from codegen.sdk.core.detached_symbols.parameter import Parameter
     from codegen.sdk.core.expressions.type import Type
-    from codegen.sdk.core.external_module import ExternalModule
-    from codegen.sdk.core.function import Function
     from codegen.sdk.core.symbol import Symbol
 
 