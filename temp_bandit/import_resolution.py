@@ -1,9 +1,6 @@
 from __future__ import annotations
 
-from codegen.sdk.core.types import TSourceFile
-from codegen.sdk.core.types import ImportResolution
 from abc import abstractmethod
-from dataclasses import dataclass
 from typing import TYPE_CHECKING, ClassVar, Generic, Literal, Self, TypeVar, override
 
 from codegen.sdk.codebase.resolution_stack import ResolutionStack
@@ -17,6 +14,7 @@
 from codegen.sdk.core.interfaces.has_attribute import HasAttribute
 from codegen.sdk.core.interfaces.usable import Usable
 from codegen.sdk.core.statements.import_statement import ImportStatement
+from codegen.sdk.core.types import TSourceFile
 from codegen.sdk.enums import EdgeType, ImportType, NodeType
 from codegen.sdk.extensions.utils import cached_property
 from codegen.sdk.output.constants import ANGULAR_STYLE
@@ -36,6 +34,7 @@
     from codegen.sdk.core.interfaces.importable import Importable
     from codegen.sdk.core.node_id_factory import NodeId
     from codegen.sdk.core.symbol import Symbol
+    from codegen.sdk.core.types import ImportResolution
 
 
 TSourceFile = TypeVar(""TSourceFile"", bound=""SourceFile"")