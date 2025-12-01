@@ -1,3 +1,5 @@
+""""""Base module for request processing functionality.""""""
+
 import asyncio
 import glob
 import json
@@ -16,39 +18,59 @@
 
 from bespokelabs.curator.file_utilities import count_lines
 from bespokelabs.curator.llm.prompt_formatter import PromptFormatter
-from bespokelabs.curator.request_processor.config import (
-    BatchRequestProcessorConfig,
-    RequestProcessorConfig,
-)
+from bespokelabs.curator.request_processor.config import BatchRequestProcessorConfig, RequestProcessorConfig
 from bespokelabs.curator.request_processor.event_loop import run_in_event_loop
 from bespokelabs.curator.types.generic_response import GenericResponse
 
-logger = logger = logging.getLogger(__name__)
+logger = logging.getLogger(__name__)
 
 CACHE_MSG = ""If you want to regenerate the dataset, disable or delete the cache.""
 
 
 class BaseRequestProcessor(ABC):
-    """"""
-    Base class for all request processors.
+    """"""Base class for all request processors.
+
+    Provides core functionality for processing requests through LLM APIs, including:
+    - File descriptor limit management
+    - Request file creation and caching
+    - Response processing and dataset generation
+    - Error handling and validation
     """"""
 
     def __init__(self, config: RequestProcessorConfig):
+        """"""Initialize the request processor.
+
+        Args:
+            config: Configuration object containing processing parameters
+        """"""
         # Increase the number of open file descriptors to avoid ""Too many open files"" errors
         soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
         desired_limit = min(10_000_000, hard)
-        logger.debug(
-            f""Adjusting file descriptor limit from {soft} to {desired_limit} (hard limit: {hard})""
-        )
+        logger.debug(f""Adjusting file descriptor limit from {soft} to {desired_limit} (hard limit: {hard})"")
         resource.setrlimit(resource.RLIMIT_NOFILE, (desired_limit, hard))
         self.config = config
 
+    @property
+    @abstractmethod
+    def backend(self) -> str:
+        """"""Backend property.""""""
+        return ""base""
+
     @abstractmethod
     def requests_to_responses(self, generic_request_files: list[str]) -> None:
+        """"""Process request files and generate responses.
+
+        Args:
+            generic_request_files: List of paths to request files to process
+        """"""
         pass
 
     def check_structured_output_support(self) -> bool:
-        """"""Check if the model supports structured output""""""
+        """"""Check if the model supports structured output.
+
+        Returns:
+            bool: True if structured output is supported, False otherwise
+        """"""
         return True
 
     def run(
@@ -58,15 +80,19 @@ def run(
         parse_func_hash: str,
         prompt_formatter: PromptFormatter,
     ) -> Dataset:
-        """"""
-        Uses the API to completing the specific map by calling the LLM.
+        """"""Uses the API to completing the specific map by calling the LLM.
 
         Args:
-            dataset (Dataset): Dataset that is being mapped over
-            working_dir (str): Working directory to save files (requests.jsonl, responses.jsonl, dataset.arrow)
+            dataset: Dataset that is being mapped over
+            working_dir: Working directory to save files (requests.jsonl, responses.jsonl, dataset.arrow)
+            parse_func_hash: Hash of the parse function for caching
+            prompt_formatter: Formatter for generating prompts from dataset rows
 
         Returns:
-            Dataset: Completed dataset
+            Dataset: Completed dataset with LLM responses
+
+        Raises:
+            ValueError: If model doesn't support structured output but it's requested
         """"""
         self.prompt_formatter = prompt_formatter
         self.working_dir = working_dir
@@ -76,34 +102,28 @@ def run(
         if output_dataset is not None:
             return output_dataset
 
-        logger.info(
-            f""Running {self.__class__.__name__} completions with model: {self.config.model}""
-        )
+        logger.info(f""Running {self.__class__.__name__} completions with model: {self.config.model}"")
 
         self.prompt_formatter = prompt_formatter
         if self.prompt_formatter.response_format:
             if not self.check_structured_output_support():
-                raise ValueError(
-                    f""Model {self.config.model} does not support structured output, ""
-                    f""response_format: {self.prompt_formatter.response_format}""
-                )
+                raise ValueError(f""Model {self.config.model} does not support structured output, "" f""response_format: {self.prompt_formatter.response_format}"")
         generic_request_files = self.create_request_files(dataset)
 
         self.requests_to_responses(generic_request_files)
 
         return self.create_dataset_files(parse_func_hash)
 
     def _verify_existing_request_files(self, dataset: Optional[Dataset]) -> List[int]:
-        """"""
-        Verify integrity of the cache (each request file has associated metadata, and the number of rows is correct),
-        and return the indices of request files that need to be regenerated (so that no work is repeated).
+        """"""Verify integrity of the cache and identify files needing regeneration.
+
+        Checks that each request file has associated metadata and correct number of rows.
 
         Args:
-            working_dir (str): Working directory where cache files are expected to be (requests.jsonl, metadata.json)
-            dataset (Optional[Dataset]): The dataset that we want to create requests from
+            dataset: The dataset to create requests from
 
         Returns:
-            List[int]: Indices of missing files
+            List of indices for request files that need to be regenerated
         """"""
         if isinstance(self.config, BatchRequestProcessorConfig) and dataset is not None:
             expected_num_files = ceil(len(dataset) / self.config.batch_size)
@@ -134,30 +154,24 @@ def _verify_existing_request_files(self, dataset: Optional[Dataset]) -> List[int
 
                 expected_num_jobs = metadata[""num_jobs""]
                 if num_jobs != expected_num_jobs:
-                    logger.warning(
-                        f""Request file {req_f} has {num_jobs} jobs, but metadata file {meta_f} has {expected_num_jobs} jobs""
-                    )
+                    logger.warning(f""Request file {req_f} has {num_jobs} jobs, but metadata file {meta_f} has {expected_num_jobs} jobs"")
                     incomplete_files.append(i)
 
             return incomplete_files
 
         except Exception as e:
-            logger.warning(
-                f""Cache verification failed due to {e} - regenerating all request files.""
-            )
+            logger.warning(f""Cache verification failed due to {e} - regenerating all request files."")
             incomplete_files = list(range(expected_num_files))
             return incomplete_files
 
     def create_request_files(self, dataset: Optional[Dataset]) -> list[str]:
-        """"""
-        Creates a request file if they don't already exist or use existing.
+        """"""Creates request files if they don't exist or uses existing ones.
 
         Args:
-            dataset (Dataset): The dataset to be processed.
-            working_dir (str): The directory where request files will be saved.
+            dataset: The dataset to be processed
 
         Returns:
-            list[str]: Paths to the request files that were created.
+            List of paths to the request files
         """"""
         os.makedirs(self.working_dir, exist_ok=True)
         request_files = glob.glob(os.path.join(self.working_dir, ""requests_*.jsonl""))
@@ -194,7 +208,7 @@ def create_request_files(self, dataset: Optional[Dataset]) -> list[str]:
 
         if dataset is None:
             with open(request_file, ""w"") as f:
-                generic_request = self.prompt_formatter.create_generic_request(dict(), 0)
+                generic_request = self.prompt_formatter.create_generic_request(dict(), 0)  # noqa: C408
                 generic_request.generation_params = self.config.generation_params
                 f.write(json.dumps(generic_request.model_dump(), default=str) + ""
"")
 
@@ -205,12 +219,8 @@ def create_request_files(self, dataset: Optional[Dataset]) -> list[str]:
 
         if isinstance(self.config, BatchRequestProcessorConfig):
             num_batches = ceil(len(dataset) / self.config.batch_size)
-            request_files = [
-                os.path.join(self.working_dir, f""requests_{i}.jsonl"") for i in range(num_batches)
-            ]
-            metadata_files = [
-                os.path.join(self.working_dir, f""metadata_{i}.json"") for i in range(num_batches)
-            ]
+            request_files = [os.path.join(self.working_dir, f""requests_{i}.jsonl"") for i in range(num_batches)]
+            metadata_files = [os.path.join(self.working_dir, f""metadata_{i}.json"") for i in range(num_batches)]
 
             async def create_all_request_files():
                 tasks = [
@@ -238,6 +248,14 @@ async def acreate_request_file(
         metadata_file: str,
         start_idx: int = 0,
     ) -> None:
+        """"""Asynchronously create a request file and its metadata.
+
+        Args:
+            dataset: Dataset to create requests from
+            request_file: Path to save request file
+            metadata_file: Path to save metadata file
+            start_idx: Starting index in dataset for this batch
+        """"""
         if isinstance(self.config, BatchRequestProcessorConfig):
             end_idx = min(start_idx + self.config.batch_size, len(dataset))
             dataset = dataset.select(range(start_idx, end_idx))
@@ -260,14 +278,22 @@ async def acreate_request_file(
         logger.info(f""Wrote {num_requests} requests to {request_file}."")
 
     def attempt_loading_cached_dataset(self, parse_func_hash: str) -> Optional[Dataset]:
+        """"""Attempt to load a cached dataset file.
+
+        Args:
+            parse_func_hash: Hash identifying the specific dataset
+
+        Returns:
+            Cached dataset if available and valid, None otherwise
+        """"""
         dataset_file = os.path.join(self.working_dir, f""{parse_func_hash}.arrow"")
         if os.path.exists(dataset_file):
             logger.debug(f""Loading dataset from {dataset_file}"")
             try:
                 output_dataset = Dataset.from_file(dataset_file)
                 logger.info(f""Using cached output dataset. {CACHE_MSG}"")
                 return output_dataset
-            except pyarrow.lib.ArrowInvalid as e:
+            except pyarrow.lib.ArrowInvalid:
                 os.remove(dataset_file)
                 logger.warning(
                     f""Failed to load dataset from {dataset_file}, ""
@@ -279,19 +305,16 @@ def create_dataset_files(
         self,
         parse_func_hash: str,
     ) -> Dataset:
-        """"""
-        Creates the request files if they don't already exist or use existing.
-        A single request file (requests_0.jsonl) or multiple request files
-        (requests_0.jsonl, requests_1.jsonl, etc.) are created depending on
-        batch_size.
+        """"""Creates dataset from response files.
 
         Args:
-            dataset (Dataset): The dataset to be processed.
-            working_dir (str): The directory where request files will be saved.
-            prompt_formatter (PromptFormatter): The prompt formatter to use for parsing the responses.
+            parse_func_hash: Hash identifying the dataset version
 
         Returns:
-            Dataset: Completed dataset
+            Dataset containing processed responses
+
+        Raises:
+            ValueError: If no responses found or processing fails
         """"""
         responses_files = glob.glob(os.path.join(self.working_dir, ""responses_*.jsonl""))
         if len(responses_files) == 0:
@@ -322,15 +345,9 @@ def create_dataset_files(
                             continue
 
                         try:
-                            response.response_message = (
-                                self.prompt_formatter.response_to_response_format(
-                                    response.response_message
-                                )
-                            )
-                        except (json.JSONDecodeError, ValidationError) as e:
-                            logger.warning(
-                                ""Skipping response due to error parsing response message into response format""
-                            )
+                            response.response_message = self.prompt_formatter.response_to_response_format(response.response_message)
+                        except (json.JSONDecodeError, ValidationError):
+                            logger.warning(""Skipping response due to error parsing response message into response format"")
                             failed_responses_count += 1
                             continue
 
@@ -363,23 +380,18 @@ def create_dataset_files(
                             if not isinstance(row, dict):
                                 os.remove(dataset_file)
                                 raise ValueError(
-                                    f""Got invalid row {row} of type {type(row)} from `parse_func`. ""
-                                    f""This should be type <class 'dict'>. {error_help}""
+                                    f""Got invalid row {row} of type {type(row)} from `parse_func`. "" f""This should be type <class 'dict'>. {error_help}""
                                 )
                             if not row:
                                 os.remove(dataset_file)
-                                raise ValueError(
-                                    f""Got empty row {row} from `parse_func`. {error_help}""
-                                )
+                                raise ValueError(f""Got empty row {row} from `parse_func`. {error_help}"")
                             # Add the original row index to the row so that we can sort by it later.
                             row[""__original_row_idx""] = response.generic_request.original_row_idx
                             writer.write(row)
 
             logger.info(f""Read {total_responses_count} responses."")
             error_sample_str = ""
"".join(error_sample)
-            error_sample_msg = (
-                f""Sample of the first {len(error_sample)} errors encountered: 
 {error_sample_str}""
-            )
+            error_sample_msg = f""Sample of the first {len(error_sample)} errors encountered: 
 {error_sample_str}""
             if failed_responses_count == total_responses_count:
                 writer.write({""error"": ""All requests failed""})
                 writer.finalize()
@@ -393,9 +405,7 @@ def create_dataset_files(
                 logger.warning(f""{failed_responses_count} requests failed."")
                 if self.config.require_all_responses:
                     os.remove(dataset_file)
-                    raise ValueError(
-                        f""Some requests failed and require_all_responses is True. {error_sample_msg}""
-                    )
+                    raise ValueError(f""Some requests failed and require_all_responses is True. {error_sample_msg}"")
 
             # number of responses matches number of requests
             request_files = glob.glob(os.path.join(self.working_dir, ""requests_*.jsonl""))
@@ -405,31 +415,37 @@ def create_dataset_files(
 
             if n_requests != total_responses_count:
                 logger.warning(
-                    f""{n_requests - total_responses_count} requests do not have responses. n_requests is {n_requests} and n_responses is {total_responses_count}""
+                    f""{n_requests - total_responses_count} requests do not have responses. ""
+                    f""n_requests is {n_requests} and n_responses is {total_responses_count}""
                 )
                 if self.config.require_all_responses:
                     os.remove(dataset_file)
-                    raise ValueError(
-                        f""Some requests do not have responses and require_all_responses is True.""
-                    )
+                    raise ValueError(""Some requests do not have responses and require_all_responses is True."")
 
         d = Dataset.from_file(dataset_file)
         d = d.sort(""__original_row_idx"")
         d = d.remove_columns(""__original_row_idx"")
         return d
 
 
-def parse_response_message(
-    response_message: str, response_format: Optional[BaseModel]
-) -> tuple[Optional[dict | str], Optional[list[str]]]:
+def parse_response_message(response_message: str, response_format: Optional[BaseModel]) -> tuple[Optional[dict | str], Optional[list[str]]]:
+    """"""Parse a response message into the expected format.
+
+    Args:
+        response_message: Raw response string from LLM
+        response_format: Expected format for structured responses
+
+    Returns:
+        Tuple containing:
+        - Parsed response (dict or str) or None if parsing failed
+        - List of error messages if parsing failed, None otherwise
+    """"""
     response_errors = None
     if response_format:
         try:
             response_message = json.loads(response_message)
         except json.JSONDecodeError:
-            logger.warning(
-                f""Failed to parse response as JSON: {response_message}, skipping this response.""
-            )
+            logger.warning(f""Failed to parse response as JSON: {response_message}, skipping this response."")
             response_message = None
             response_errors = [f""Failed to parse response as JSON: {response_message}""]
     return response_message, response_errors