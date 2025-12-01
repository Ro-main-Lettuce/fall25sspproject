@@ -6,7 +6,7 @@
 from json import JSONDecodeError
 from typing import Any, Callable, TypeVar
 
-from .exceptions import InstructorRetryException, AsyncValidationError
+from .exceptions import InstructorRetryException, AsyncValidationError, ValidationError as InstructorValidationError
 from .hooks import Hooks
 from ..mode import Mode
 from ..processing.response import (
@@ -196,7 +196,7 @@ def retry_sync(
                         mode=mode,
                         stream=stream,
                     )
-                except (ValidationError, JSONDecodeError) as e:
+                except (ValidationError, JSONDecodeError, InstructorValidationError) as e:
                     logger.debug(f""Parse error: {e}"")
                     hooks.emit_parse_error(e)
 
@@ -329,6 +329,7 @@ async def retry_async(
                     ValidationError,
                     JSONDecodeError,
                     AsyncValidationError,
+                    InstructorValidationError,
                 ) as e:
                     logger.debug(f""Parse error: {e}"")
                     hooks.emit_parse_error(e)