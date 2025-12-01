@@ -1,14 +1,13 @@
-from codegen.extensions.lsp.types import File
 import logging
 import pprint
-from dataclasses import dataclass
 from pathlib import Path
 
 from attr import asdict
 from lsprotocol import types
-from lsprotocol.types import CreateFile, CreateFileOptions, DeleteFile, Position, Range, RenameFile, TextEdit
+from lsprotocol.types import CreateFile, CreateFileOptions, DeleteFile, Position, Range, TextEdit
 from pygls.workspace import TextDocument, Workspace
 
+from codegen.extensions.lsp.types import File
 from codegen.sdk.codebase.io.file_io import FileIO
 from codegen.sdk.codebase.io.io import IO
 