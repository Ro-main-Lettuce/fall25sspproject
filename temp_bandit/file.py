@@ -4,19 +4,17 @@
 import resource
 import sys
 from abc import abstractmethod
-from collections.abc import Sequence
 from dataclasses import dataclass
 from datetime import datetime
 from functools import cached_property
 from os import PathLike
 from pathlib import Path
-from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, cast, Sequence
+from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar, cast
 
 from git import Commit
 from tree_sitter import Node as TSNode
 from typing_extensions import Self, override
 
-from codegen.sdk._proxy import proxy_property
 from codegen.sdk.codebase.codebase_graph import CodebaseGraph
 from codegen.sdk.codebase.range_index import RangeIndex
 from codegen.sdk.codebase.span import Range