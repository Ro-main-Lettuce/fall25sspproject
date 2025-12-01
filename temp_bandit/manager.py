@@ -2,9 +2,8 @@
 from codegen.sdk.core.autocommit.types import PendingFiles
 from collections.abc import Iterator
 from contextlib import contextmanager
-from dataclasses import dataclass
 from pathlib import Path
-from typing import TYPE_CHECKING, Optional, Union
+from typing import TYPE_CHECKING, Union
 
 from codegen.sdk.core.autocommit.constants import (
     REMOVED,