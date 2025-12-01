@@ -12,27 +12,26 @@
 from typing import Any, Optional, Union
 from urllib.parse import urljoin, urlparse
 
-import markdownify
-import requests
-from bs4 import BeautifulSoup
+from .import_utils import optional_import_block, require_optional_import
+
+with optional_import_block():
+    import markdownify
+    import requests
+    from bs4 import BeautifulSoup
 
 # Optional PDF support
-IS_PDF_CAPABLE = False
-try:
+with optional_import_block() as result:
     import pdfminer
     import pdfminer.high_level
 
-    IS_PDF_CAPABLE = True
-except ModuleNotFoundError:
-    pass
+IS_PDF_CAPABLE = result.is_successful
 
 # Other optional dependencies
-try:
+with optional_import_block():
     import pathvalidate
-except ModuleNotFoundError:
-    pass
 
 
+@require_optional_import([""markdownify"", ""requests"", ""bs4"", ""pdfminer"", ""pathvalidate""], ""websurfer"")
 class SimpleTextBrowser:
     """"""(In preview) An extremely simple text-based web browser comparable to Lynx. Suitable for Agentic use.""""""
 
@@ -45,6 +44,16 @@ def __init__(
         bing_api_key: Optional[Union[str, None]] = None,
         request_kwargs: Optional[Union[dict[str, Any], None]] = None,
     ):
+        """"""Initialize the browser with the given parameters.
+
+        Args:
+            start_page (Optional[str], optional): The initial page to load. Defaults to None.
+            viewport_size (Optional[int], optional): The number of characters to display per page. Defaults to 1024 * 8.
+            downloads_folder (Optional[Union[str, None]], optional): The folder to save downloads to. Defaults to None.
+            bing_base_url (str, optional): The base URL for Bing searches. Defaults to ""https://api.bing.microsoft.com/v7.0/search"".
+            bing_api_key (Optional[Union[str, None]], optional): The API key for Bing searches. Defaults to None.
+            request_kwargs (Optional[Union[dict[str, Any], None]], optional): Additional keyword arguments to pass to the requests library. Defaults to None.
+        """"""
         self.start_page: str = start_page if start_page else ""about:blank""
         self.viewport_size = viewport_size  # Applies only to the standard uri types
         self.downloads_folder = downloads_folder
@@ -65,6 +74,11 @@ def address(self) -> str:
         return self.history[-1]
 
     def set_address(self, uri_or_path: str) -> None:
+        """"""Set the address of the current page.
+
+        Args:
+            uri_or_path (str): The URI or path to set as the current page.
+        """"""
         self.history.append(uri_or_path)
 
         # Handle special URIs
@@ -99,13 +113,19 @@ def _set_page_content(self, content: str) -> None:
             self.viewport_current_page = len(self.viewport_pages) - 1
 
     def page_down(self) -> None:
+        """"""Move the viewport down by one page.""""""
         self.viewport_current_page = min(self.viewport_current_page + 1, len(self.viewport_pages) - 1)
 
     def page_up(self) -> None:
+        """"""Move the viewport up by one page.""""""
         self.viewport_current_page = max(self.viewport_current_page - 1, 0)
 
     def visit_page(self, path_or_uri: str) -> str:
-        """"""Update the address, visit the page, and return the content of the viewport.""""""
+        """"""Update the address, visit the page, and return the content of the viewport.
+
+        Args:
+            path_or_uri (str): The URI or path to visit.
+        """"""
         self.set_address(path_or_uri)
         return self.viewport
 