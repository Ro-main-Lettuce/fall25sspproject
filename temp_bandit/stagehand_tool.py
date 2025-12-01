@@ -9,13 +9,18 @@
 Each function takes atomic instructions to increase reliability.
 """"""
 
+import logging
 import os
-from typing import Any, Type
+from functools import lru_cache
+from typing import Any, Dict, List, Optional, Type, Union
 
 from pydantic import BaseModel, Field
 
 from crewai.tools.base_tool import BaseTool
 
+# Set up logging
+logger = logging.getLogger(__name__)
+
 # Define STAGEHAND_AVAILABLE at module level
 STAGEHAND_AVAILABLE = False
 try:
@@ -25,6 +30,32 @@
     pass  # Keep STAGEHAND_AVAILABLE as False
 
 
+class StagehandResult(BaseModel):
+    """"""Result from a Stagehand operation.
+    
+    Attributes:
+        success: Whether the operation completed successfully
+        data: The result data from the operation
+        error: Optional error message if the operation failed
+    """"""
+    success: bool = Field(..., description=""Whether the operation completed successfully"")
+    data: Union[str, Dict, List] = Field(..., description=""The result data from the operation"")
+    error: Optional[str] = Field(None, description=""Optional error message if the operation failed"")
+
+
+class StagehandToolConfig(BaseModel):
+    """"""Configuration for the StagehandTool.
+    
+    Attributes:
+        api_key: OpenAI API key for Stagehand authentication
+        timeout: Maximum time in seconds to wait for operations (default: 30)
+        retry_attempts: Number of times to retry failed operations (default: 3)
+    """"""
+    api_key: str = Field(..., description=""OpenAI API key for Stagehand authentication"")
+    timeout: int = Field(30, description=""Maximum time in seconds to wait for operations"")
+    retry_attempts: int = Field(3, description=""Number of times to retry failed operations"")
+
+
 class StagehandToolSchema(BaseModel):
     """"""Schema for the StagehandTool input parameters.
     
@@ -56,7 +87,9 @@ class StagehandToolSchema(BaseModel):
     )
     instruction: str = Field(
         ...,
-        description=""An atomic instruction for Stagehand to execute. Instructions should be simple and specific to increase reliability.""
+        description=""An atomic instruction for Stagehand to execute. Instructions should be simple and specific to increase reliability."",
+        min_length=1,
+        max_length=500
     )
 
 
@@ -105,10 +138,17 @@ class StagehandTool(BaseTool):
     )
     args_schema: Type[BaseModel] = StagehandToolSchema
     
-    def __init__(self, **kwargs: Any) -> None:
+    def __init__(self, config: StagehandToolConfig | None = None, **kwargs: Any) -> None:
         """"""Initialize the StagehandTool.
         
-        The tool requires the OPENAI_API_KEY environment variable to be set.
+        Args:
+            config: Optional configuration for the tool. If not provided,
+                   will attempt to use OPENAI_API_KEY from environment.
+            **kwargs: Additional keyword arguments passed to the base class.
+        
+        Raises:
+            ImportError: If the stagehand package is not installed
+            ValueError: If no API key is provided via config or environment
         """"""
         super().__init__(**kwargs)
         
@@ -117,41 +157,148 @@ def __init__(self, **kwargs: Any) -> None:
                 ""The 'stagehand' package is required to use this tool. ""
                 ""Please install it with: pip install stagehand""
             )
-            
-        self.api_key = os.getenv(""OPENAI_API_KEY"")
-        if not self.api_key:
-            raise ValueError(
-                ""OPENAI_API_KEY environment variable is required for StagehandTool""
+        
+        # Use config if provided, otherwise try environment variable
+        if config is not None:
+            self.config = config
+        else:
+            api_key = os.getenv(""OPENAI_API_KEY"")
+            if not api_key:
+                raise ValueError(
+                    ""Either provide config with api_key or set OPENAI_API_KEY environment variable""
+                )
+            self.config = StagehandToolConfig(
+                api_key=api_key,
+                timeout=30,
+                retry_attempts=3
             )
     
-    def _run(self, api_method: str, instruction: str, **kwargs: Any) -> Any:
-        """"""Execute a Stagehand command using the specified API method.
+    @lru_cache(maxsize=100)
+    def _cached_run(self, api_method: str, instruction: str) -> Any:
+        """"""Execute a cached Stagehand command.
+        
+        This method is cached to improve performance for repeated operations.
         
         Args:
             api_method: The Stagehand API to use ('act', 'extract', or 'observe')
             instruction: An atomic instruction for Stagehand to execute
-            **kwargs: Additional keyword arguments passed to the Stagehand API
             
         Returns:
-            The result from the Stagehand API call
+            The raw result from the Stagehand API call
             
         Raises:
             ValueError: If an invalid api_method is provided
-            RuntimeError: If the Stagehand API call fails
+            Exception: If the Stagehand API call fails
         """"""
+        logger.debug(
+            ""Cache operation - Method: %s, Instruction length: %d"",
+            api_method,
+            len(instruction)
+        )
+        
+        # Initialize Stagehand with configuration
+        logger.info(
+            ""Initializing Stagehand (timeout=%ds, retries=%d)"",
+            self.config.timeout,
+            self.config.retry_attempts
+        )
+        st = stagehand.Stagehand(
+            api_key=self.config.api_key,
+            timeout=self.config.timeout,
+            retry_attempts=self.config.retry_attempts
+        )
+        
+        # Call the appropriate Stagehand API based on the method
+        logger.info(""Executing %s operation with instruction: %s"", api_method, instruction[:100])
         try:
-            # Initialize Stagehand with the OpenAI API key
-            st = stagehand.Stagehand(api_key=self.api_key)
-            
-            # Call the appropriate Stagehand API based on the method
             if api_method == ""act"":
-                return st.act(instruction)
+                result = st.act(instruction)
             elif api_method == ""extract"":
-                return st.extract(instruction)
+                result = st.extract(instruction)
             elif api_method == ""observe"":
-                return st.observe(instruction)
+                result = st.observe(instruction)
             else:
                 raise ValueError(f""Unknown api_method: {api_method}"")
+            
+            
+            logger.info(""Successfully executed %s operation"", api_method)
+            return result
+            
+        except Exception as e:
+            logger.warning(
+                ""Operation failed (method=%s, error=%s), will be retried on next attempt"",
+                api_method,
+                str(e)
+            )
+            raise
+
+    def _run(self, api_method: str, instruction: str, **kwargs: Any) -> StagehandResult:
+        """"""Execute a Stagehand command using the specified API method.
+        
+        Args:
+            api_method: The Stagehand API to use ('act', 'extract', or 'observe')
+            instruction: An atomic instruction for Stagehand to execute
+            **kwargs: Additional keyword arguments passed to the Stagehand API
+            
+        Returns: 
+            StagehandResult containing the operation result and status
+        """"""
+        try:
+            # Log operation context
+            logger.debug(
+                ""Starting operation - Method: %s, Instruction length: %d, Args: %s"",
+                api_method,
+                len(instruction),
+                kwargs
+            )
+            
+            # Use cached execution
+            result = self._cached_run(api_method, instruction)
+            logger.info(""Operation completed successfully"")
+            return StagehandResult(success=True, data=result)
                 
+        except stagehand.AuthenticationError as e:
+            logger.error(
+                ""Authentication failed - Method: %s, Error: %s"",
+                api_method,
+                str(e)
+            )
+            return StagehandResult(
+                success=False,
+                data={},
+                error=f""Authentication failed: {str(e)}""
+            )
+        except stagehand.APIError as e:
+            logger.error(
+                ""API error - Method: %s, Error: %s"",
+                api_method,
+                str(e)
+            )
+            return StagehandResult(
+                success=False,
+                data={},
+                error=f""API error: {str(e)}""
+            )
+        except stagehand.BrowserError as e:
+            logger.error(
+                ""Browser error - Method: %s, Error: %s"",
+                api_method,
+                str(e)
+            )
+            return StagehandResult(
+                success=False,
+                data={},
+                error=f""Browser error: {str(e)}""
+            )
         except Exception as e:
-            raise RuntimeError(f""Stagehand API call failed: {str(e)}"")
+            logger.error(
+                ""Unexpected error - Method: %s, Error type: %s, Message: %s"",
+                api_method,
+                type(e).__name__,
+                str(e)
+            )
+            return StagehandResult(
+                success=False,
+                data={},
+                error=f""Unexpected error: {str(e)}""
+            )