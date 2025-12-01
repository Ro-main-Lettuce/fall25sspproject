@@ -12,16 +12,292 @@
 import logging
 import os
 import time
-from typing import Any, Dict, Optional, List, Union, Callable
+from typing import Any, Dict, Optional, List, Union, Callable, Literal, TypeVar, Generic
 import json
+from datetime import datetime
+import re
+import warnings
 
 import requests
 import pydantic
 import websockets
+from pydantic import Field
+
+warnings.filterwarnings(""ignore"", message=""Field name \""json\"" in \""FirecrawlDocument\"" shadows an attribute in parent \""BaseModel\"""")
+warnings.filterwarnings(""ignore"", message=""Field name \""json\"" in \""ChangeTrackingData\"" shadows an attribute in parent \""BaseModel\"""")
+warnings.filterwarnings(""ignore"", message=""Field name \""schema\"" in \""ExtractConfig\"" shadows an attribute in parent \""BaseModel\"""")
+warnings.filterwarnings(""ignore"", message=""Field name \""schema\"" in \""ExtractParams\"" shadows an attribute in parent \""BaseModel\"""")
+
+
+def get_version():
+    try:
+        from pathlib import Path
+        package_path = os.path.dirname(__file__)
+        version_file = Path(os.path.join(package_path, '__init__.py')).read_text()
+        version_match = re.search(r""^__version__ = ['\""]([^'\""]*)['\""]"", version_file, re.M)
+        if version_match:
+            return version_match.group(1).strip()
+    except Exception:
+        print(""Failed to get version from __init__.py"")
+        return None
+
+version = get_version()
 
 logger : logging.Logger = logging.getLogger(""firecrawl"")
 
+T = TypeVar('T')
+
+class FirecrawlDocumentMetadata(pydantic.BaseModel):
+    """"""Metadata for a Firecrawl document.""""""
+    title: Optional[str] = None
+    description: Optional[str] = None
+    language: Optional[str] = None
+    keywords: Optional[str] = None
+    robots: Optional[str] = None
+    ogTitle: Optional[str] = None
+    ogDescription: Optional[str] = None
+    ogUrl: Optional[str] = None
+    ogImage: Optional[str] = None
+    ogAudio: Optional[str] = None
+    ogDeterminer: Optional[str] = None
+    ogLocale: Optional[str] = None
+    ogLocaleAlternate: Optional[List[str]] = None
+    ogSiteName: Optional[str] = None
+    ogVideo: Optional[str] = None
+    dctermsCreated: Optional[str] = None
+    dcDateCreated: Optional[str] = None
+    dcDate: Optional[str] = None
+    dctermsType: Optional[str] = None
+    dcType: Optional[str] = None
+    dctermsAudience: Optional[str] = None
+    dctermsSubject: Optional[str] = None
+    dcSubject: Optional[str] = None
+    dcDescription: Optional[str] = None
+    dctermsKeywords: Optional[str] = None
+    modifiedTime: Optional[str] = None
+    publishedTime: Optional[str] = None
+    articleTag: Optional[str] = None
+    articleSection: Optional[str] = None
+    sourceURL: Optional[str] = None
+    statusCode: Optional[int] = None
+    error: Optional[str] = None
+
+class AgentOptions(pydantic.BaseModel):
+    """"""Configuration for the agent.""""""
+    model: Literal[""FIRE-1""] = ""FIRE-1""
+    prompt: Optional[str] = None
+
+class AgentOptionsExtract(pydantic.BaseModel):
+    """"""Configuration for the agent in extract operations.""""""
+    model: Literal[""FIRE-1""] = ""FIRE-1""
+
+class ActionsResult(pydantic.BaseModel):
+    """"""Result of actions performed during scraping.""""""
+    screenshots: List[str]
+
+class FirecrawlDocument(pydantic.BaseModel, Generic[T]):
+    """"""Document retrieved or processed by Firecrawl.""""""
+    url: Optional[str] = None
+    markdown: Optional[str] = None
+    html: Optional[str] = None
+    rawHtml: Optional[str] = None
+    links: Optional[List[str]] = None
+    extract: Optional[T] = None
+    json: Optional[T] = None
+    screenshot: Optional[str] = None
+    metadata: Optional[FirecrawlDocumentMetadata] = None
+    actions: Optional[ActionsResult] = None
+    title: Optional[str] = None  # v1 search only
+    description: Optional[str] = None  # v1 search only
+
+class LocationConfig(pydantic.BaseModel):
+    """"""Location configuration for scraping.""""""
+    country: Optional[str] = None
+    languages: Optional[List[str]] = None
+
+class WebhookConfig(pydantic.BaseModel):
+    """"""Configuration for webhooks.""""""
+    url: str
+    headers: Optional[Dict[str, str]] = None
+    metadata: Optional[Dict[str, str]] = None
+    events: Optional[List[Literal[""completed"", ""failed"", ""page"", ""started""]]] = None
+
+class CommonOptions(pydantic.BaseModel):
+    """"""Parameters for scraping operations.""""""
+    formats: Optional[List[Literal[""markdown"", ""html"", ""rawHtml"", ""content"", ""links"", ""screenshot"", ""screenshot@fullPage"", ""extract"", ""json""]]] = None
+    headers: Optional[Dict[str, str]] = None
+    includeTags: Optional[List[str]] = None
+    excludeTags: Optional[List[str]] = None
+    onlyMainContent: Optional[bool] = None
+    waitFor: Optional[int] = None
+    timeout: Optional[int] = None
+    location: Optional[LocationConfig] = None
+    mobile: Optional[bool] = None
+    skipTlsVerification: Optional[bool] = None
+    removeBase64Images: Optional[bool] = None
+    blockAds: Optional[bool] = None
+    proxy: Optional[Literal[""basic"", ""stealth""]] = None
+
+class WaitAction(pydantic.BaseModel):
+    """"""Wait action to perform during scraping.""""""
+    type: Literal[""wait""]
+    milliseconds: int
+    selector: Optional[str] = None
+
+class ScreenshotAction(pydantic.BaseModel):
+    """"""Screenshot action to perform during scraping.""""""
+    type: Literal[""screenshot""]
+    fullPage: Optional[bool] = None
+
+class ClickAction(pydantic.BaseModel):
+    """"""Click action to perform during scraping.""""""
+    type: Literal[""click""]
+    selector: str
+
+class WriteAction(pydantic.BaseModel):
+    """"""Write action to perform during scraping.""""""
+    type: Literal[""write""]
+    text: str
+
+class PressAction(pydantic.BaseModel):
+    """"""Press action to perform during scraping.""""""
+    type: Literal[""press""]
+    key: str
+
+class ScrollAction(pydantic.BaseModel):
+    """"""Scroll action to perform during scraping.""""""
+    type: Literal[""scroll""]
+    direction: Literal[""up"", ""down""]
+    selector: Optional[str] = None
+
+class ScrapeAction(pydantic.BaseModel):
+    """"""Scrape action to perform during scraping.""""""
+    type: Literal[""scrape""]
+
+class ExecuteJavascriptAction(pydantic.BaseModel):
+    """"""Execute javascript action to perform during scraping.""""""
+    type: Literal[""executeJavascript""]
+    script: str
+
+class ExtractAgent(pydantic.BaseModel):
+    """"""Configuration for the agent in extract operations.""""""
+    model: Literal[""FIRE-1""] = ""FIRE-1""
+
+class ExtractConfig(pydantic.BaseModel):
+    """"""Configuration for extraction.""""""
+    prompt: Optional[str] = None
+    schema: Optional[Any] = None
+    systemPrompt: Optional[str] = None
+    agent: Optional[ExtractAgent] = None
+
+class ScrapeParams(CommonOptions):
+    """"""Parameters for scraping operations.""""""
+    extract: Optional[ExtractConfig] = None
+    jsonOptions: Optional[ExtractConfig] = None
+    actions: Optional[List[Union[WaitAction, ScreenshotAction, ClickAction, WriteAction, PressAction, ScrollAction, ScrapeAction, ExecuteJavascriptAction]]] = None
+    agent: Optional[AgentOptions] = None
+
+class ScrapeResponse(FirecrawlDocument[T], Generic[T]):
+    """"""Response from scraping operations.""""""
+    success: bool = True
+    warning: Optional[str] = None
+    error: Optional[str] = None
+
+class BatchScrapeResponse(pydantic.BaseModel):
+    """"""Response from batch scrape operations.""""""
+    id: Optional[str] = None
+    url: Optional[str] = None
+    success: bool = True
+    error: Optional[str] = None
+    invalidURLs: Optional[List[str]] = None
+
+class BatchScrapeStatusResponse(pydantic.BaseModel):
+    """"""Response from batch scrape status checks.""""""
+    success: bool = True
+    status: Literal[""scraping"", ""completed"", ""failed"", ""cancelled""]
+    completed: int
+    total: int
+    creditsUsed: int
+    expiresAt: datetime
+    next: Optional[str] = None
+    data: List[FirecrawlDocument]
+
+class CrawlParams(pydantic.BaseModel):
+    """"""Parameters for crawling operations.""""""
+    includePaths: Optional[List[str]] = None
+    excludePaths: Optional[List[str]] = None
+    maxDepth: Optional[int] = None
+    maxDiscoveryDepth: Optional[int] = None
+    limit: Optional[int] = None
+    allowBackwardLinks: Optional[bool] = None
+    allowExternalLinks: Optional[bool] = None
+    ignoreSitemap: Optional[bool] = None
+    scrapeOptions: Optional[CommonOptions] = None
+    webhook: Optional[Union[str, WebhookConfig]] = None
+    deduplicateSimilarURLs: Optional[bool] = None
+    ignoreQueryParameters: Optional[bool] = None
+    regexOnFullURL: Optional[bool] = None
+
+class CrawlResponse(pydantic.BaseModel):
+    """"""Response from crawling operations.""""""
+    id: Optional[str] = None
+    url: Optional[str] = None
+    success: bool = True
+    error: Optional[str] = None
+
+class CrawlStatusResponse(pydantic.BaseModel):
+    """"""Response from crawl status checks.""""""
+    success: bool = True
+    status: Literal[""scraping"", ""completed"", ""failed"", ""cancelled""]
+    completed: int
+    total: int
+    creditsUsed: int
+    expiresAt: datetime
+    next: Optional[str] = None
+    data: List[FirecrawlDocument]
+
+class CrawlErrorsResponse(pydantic.BaseModel):
+    """"""Response from crawl/batch scrape error monitoring.""""""
+    errors: List[Dict[str, str]]  # {id: str, timestamp: str, url: str, error: str}
+    robotsBlocked: List[str]
+
+class MapParams(pydantic.BaseModel):
+    """"""Parameters for mapping operations.""""""
+    search: Optional[str] = None
+    ignoreSitemap: Optional[bool] = None
+    includeSubdomains: Optional[bool] = None
+    sitemapOnly: Optional[bool] = None
+    limit: Optional[int] = None
+    timeout: Optional[int] = None
+
+class MapResponse(pydantic.BaseModel):
+    """"""Response from mapping operations.""""""
+    success: bool = True
+    links: Optional[List[str]] = None
+    error: Optional[str] = None
+
+class ExtractParams(pydantic.BaseModel):
+    """"""Parameters for extracting information from URLs.""""""
+    prompt: Optional[str] = None
+    schema: Optional[Any] = None
+    systemPrompt: Optional[str] = None
+    allowExternalLinks: Optional[bool] = None
+    enableWebSearch: Optional[bool] = None
+    includeSubdomains: Optional[bool] = None
+    origin: Optional[str] = None
+    showSources: Optional[bool] = None
+    scrapeOptions: Optional[CommonOptions] = None
+
+class ExtractResponse(pydantic.BaseModel, Generic[T]):
+    """"""Response from extract operations.""""""
+    success: bool = True
+    data: Optional[T] = None
+    error: Optional[str] = None
+    warning: Optional[str] = None
+    sources: Optional[List[str]] = None
+
 class SearchParams(pydantic.BaseModel):
+    """"""Parameters for search operations.""""""
     query: str
     limit: Optional[int] = 5
     tbs: Optional[str] = None
@@ -34,13 +310,30 @@ class SearchParams(pydantic.BaseModel):
     scrapeOptions: Optional[Dict[str, Any]] = None
 
 class GenerateLLMsTextParams(pydantic.BaseModel):
-    """"""
-    Parameters for the LLMs.txt generation operation.
-    """"""
+    """"""Parameters for the LLMs.txt generation operation.""""""
     maxUrls: Optional[int] = 10
     showFullText: Optional[bool] = False
     __experimental_stream: Optional[bool] = None
 
+class GenerateLLMsTextResponse(pydantic.BaseModel):
+    """"""Response from LLMs.txt generation initiation.""""""
+    success: bool = True
+    id: Optional[str] = None
+    error: Optional[str] = None
+
+class GenerateLLMsTextStatusResponseData(pydantic.BaseModel):
+    """"""Data in the LLMs.txt generation status response.""""""
+    llmstxt: str
+    llmsfulltxt: Optional[str] = None
+
+class GenerateLLMsTextStatusResponse(pydantic.BaseModel):
+    """"""Response from LLMs.txt generation status checks.""""""
+    success: bool = True
+    status: Literal[""processing"", ""completed"", ""failed""]
+    data: Optional[GenerateLLMsTextStatusResponseData] = None
+    error: Optional[str] = None
+    expiresAt: Optional[str] = None
+
 class DeepResearchParams(pydantic.BaseModel):
     """"""
     Parameters for the deep research operation.
@@ -138,200 +431,310 @@ def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None)
             
         logger.debug(f""Initialized FirecrawlApp with API URL: {self.api_url}"")
 
-    def scrape_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
-        """"""
-        Scrape the specified URL using the Firecrawl API.
+    def scrape_url(
+            self,
+            url: str,
+            formats: Optional[List[Literal[""markdown"", ""html"", ""rawHtml"", ""content"", ""links"", ""screenshot"", ""screenshot@fullPage"", ""extract"", ""json""]]] = None,
+            include_tags: Optional[List[str]] = None,
+            exclude_tags: Optional[List[str]] = None,
+            only_main_content: Optional[bool] = None,
+            wait_for: Optional[int] = None,
+            timeout: Optional[int] = None,
+            location: Optional[LocationConfig] = None,
+            mobile: Optional[bool] = None,
+            skip_tls_verification: Optional[bool] = None,
+            remove_base64_images: Optional[bool] = None,
+            block_ads: Optional[bool] = None,
+            proxy: Optional[Literal[""basic"", ""stealth""]] = None,
+            extract: Optional[ExtractConfig] = None,
+            json_options: Optional[ExtractConfig] = None,
+            actions: Optional[List[Union[WaitAction, ScreenshotAction, ClickAction, WriteAction, PressAction, ScrollAction, ScrapeAction, ExecuteJavascriptAction]]] = None,
+            agent: Optional[AgentOptions] = None) -> ScrapeResponse[Any]:
+        """"""
+        Scrape and extract content from a URL.
 
         Args:
-            url (str): The URL to scrape.
-            params (Optional[Dict[str, Any]]): Additional parameters for the scrape request.
+            url (str): Target URL to scrape
+            formats (Optional[List[Literal[""markdown"", ""html"", ""rawHtml"", ""content"", ""links"", ""screenshot"", ""screenshot@fullPage"", ""extract"", ""json""]]]): Content types to retrieve
+            include_tags (Optional[List[str]]): HTML tags to include
+            exclude_tags (Optional[List[str]]): HTML tags to exclude
+            only_main_content (Optional[bool]): Extract main content only
+            wait_for (Optional[int]): Wait time in milliseconds
+            timeout (Optional[int]): Request timeout in milliseconds
+            location (Optional[LocationConfig]): Geographic location settings
+            mobile (Optional[bool]): Use mobile user agent
+            skip_tls_verification (Optional[bool]): Skip TLS certificate verification
+            remove_base64_images (Optional[bool]): Remove base64 encoded images
+            block_ads (Optional[bool]): Block advertisements
+            proxy (Optional[Literal[""basic"", ""stealth""]]): Proxy type to use
+            extract (Optional[ExtractConfig]): Content extraction settings
+            json_options (Optional[ExtractConfig]): JSON extraction settings
+            actions (Optional[List[Union[WaitAction, ScreenshotAction, ClickAction, WriteAction, PressAction, ScrollAction, ScrapeAction, ExecuteJavascriptAction]]]): Actions to perform
+            agent (Optional[AgentOptions]): Agent configuration
 
         Returns:
-            Any: The scraped data if the request is successful.
-
+            ScrapeResponse[Any]: Object containing scraped content and status information
+            
         Raises:
-            Exception: If the scrape request fails.
+            Exception: If the scrape request fails or returns an error
         """"""
-
         headers = self._prepare_headers()
 
         # Prepare the base scrape parameters with the URL
-        scrape_params = {'url': url}
+        scrape_params = {
+            'url': url,
+            'formats': formats,
+            'includeTags': include_tags,
+            'excludeTags': exclude_tags,
+            'onlyMainContent': only_main_content,
+            'waitFor': wait_for,
+            'timeout': timeout,
+            'mobile': mobile,
+            'skipTlsVerification': skip_tls_verification,
+            'removeBase64Images': remove_base64_images,
+            'blockAds': block_ads,
+            'proxy': proxy,
+            'origin': f""python-sdk@{version}""
+        }
 
-        # If there are additional params, process them
-        if params:
-            # Handle extract (for v1)
-            extract = params.get('extract', {})
-            if extract:
-                if 'schema' in extract and hasattr(extract['schema'], 'schema'):
-                    extract['schema'] = extract['schema'].schema()
+        if location:
+            scrape_params['location'] = location.dict(exclude_none=True)
+
+        # Handle extract config if provided
+        if extract:
+            if hasattr(extract, 'dict'):
+                extract_dict = extract.dict(exclude_none=True)
+                if 'schema' in extract_dict and hasattr(extract_dict['schema'], 'schema'):
+                    extract_dict['schema'] = extract_dict['schema'].schema()
+                scrape_params['extract'] = extract_dict
+            else:
                 scrape_params['extract'] = extract
 
-            # Include any other params directly at the top level of scrape_params
-            for key, value in params.items():
-                if key not in ['extract']:
-                    scrape_params[key] = value
-
-            json = params.get(""jsonOptions"", {})
-            if json:
-                if 'schema' in json and hasattr(json['schema'], 'schema'):
-                    json['schema'] = json['schema'].schema()
-                scrape_params['jsonOptions'] = json
-
-            change_tracking = params.get(""changeTrackingOptions"", {})
-            if change_tracking:
-                scrape_params['changeTrackingOptions'] = change_tracking
-
-            # Include any other params directly at the top level of scrape_params
-            for key, value in params.items():
-                if key not in ['jsonOptions', 'changeTrackingOptions', 'agent']:
-                    scrape_params[key] = value
-                    
-            agent = params.get('agent')
-            if agent:
+        if json_options:
+            if hasattr(json_options, 'dict'):
+                json_dict = json_options.dict(exclude_none=True)
+                if 'schema' in json_dict and hasattr(json_dict['schema'], 'schema'):
+                    json_dict['schema'] = json_dict['schema'].schema()
+                scrape_params['jsonOptions'] = json_dict
+            else:
+                scrape_params['jsonOptions'] = json_options
+
+        if actions:
+            scrape_params['actions'] = [action.dict(exclude_none=True) for action in actions]
+
+        if agent:
+            if hasattr(agent, 'dict'):
+                scrape_params['agent'] = agent.dict(exclude_none=True)
+            else:
                 scrape_params['agent'] = agent
 
+        scrape_params = {k: v for k, v in scrape_params.items() if v is not None}
 
         endpoint = f'/v1/scrape'
         # Make the POST request with the prepared headers and JSON data
-        response = requests.post(
+        response = self._post_request(
             f'{self.api_url}{endpoint}',
-            headers=headers,
-            json=scrape_params,
-            timeout=(scrape_params[""timeout""] + 5000 if ""timeout"" in scrape_params else None),
+            scrape_params,
+            headers,
+            timeout=(timeout + 5000 if timeout is not None else None),
         )
+        
         if response.status_code == 200:
             try:
-                response = response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
-            if response['success'] and 'data' in response:
-                return response['data']
-            elif ""error"" in response:
-                raise Exception(f'Failed to scrape URL. Error: {response[""error""]}')
-            else:
-                raise Exception(f'Failed to scrape URL. Error: {response}')
+                response_data = response.json()
+                if response_data.get('success') and 'data' in response_data:
+                    return ScrapeResponse(**response_data['data'])
+                elif ""error"" in response_data:
+                    raise Exception(f'Failed to scrape URL. Error: {response_data[""error""]}')
+                else:
+                    raise Exception(f'Failed to scrape URL. Error: {response_data}')
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, 'scrape URL')
 
-    def search(self, query: str, params: Optional[Union[Dict[str, Any], SearchParams]] = None) -> Dict[str, Any]:
-        """"""
-        Search for content using the Firecrawl API.
+    def search(
+            self,
+            query: str,
+            limit: Optional[int] = None,
+            tbs: Optional[str] = None,
+            filter: Optional[str] = None,
+            lang: Optional[str] = None,
+            country: Optional[str] = None,
+            location: Optional[str] = None,
+            origin: Optional[str] = None,
+            timeout: Optional[int] = None,
+            scrape_options: Optional[CommonOptions] = None) -> SearchResponse:
+        """"""
+        Perform a search using the Firecrawl API.
 
         Args:
-            query (str): The search query string.
-            params (Optional[Union[Dict[str, Any], SearchParams]]): Additional search parameters.
+            query (str): The search query string
+            limit (Optional[int]): Maximum number of search results to return (default: 5)
+            tbs (Optional[str]): Time-based search filter
+            filter (Optional[str]): Additional search filter
+            lang (Optional[str]): Language code for search results (default: 'en')
+            country (Optional[str]): Country code for search context (default: 'us')
+            location (Optional[str]): Geographic location for search context
+            origin (Optional[str]): Origin identifier for the search request
+            timeout (Optional[int]): Request timeout in milliseconds (default: 60000)
+            scrape_options (Optional[CommonOptions]): Additional scraping configuration options
 
         Returns:
-            Dict[str, Any]: The search response containing success status and search results.
+            SearchResponse: Object containing search results and status information
+            
+        Raises:
+            Exception: If the search request fails or returns an error
         """"""
-        if params is None:
-            params = {}
-
-        if isinstance(params, dict):
-            search_params = SearchParams(query=query, **params)
+        headers = self._prepare_headers()
+        
+        search_params = {
+            'query': query,
+            'limit': limit if limit is not None else 5,
+            'tbs': tbs,
+            'filter': filter,
+            'lang': lang if lang is not None else 'en',
+            'country': country if country is not None else 'us',
+            'location': location,
+            'origin': origin if origin is not None else ""api"",
+            'timeout': timeout if timeout is not None else 60000,
+            'origin': f""python-sdk@{version}""
+        }
+        
+        if scrape_options:
+            search_params['scrapeOptions'] = scrape_options.dict(exclude_none=True)
+        
+        search_params = {k: v for k, v in search_params.items() if v is not None}
+        
+        response = self._post_request(f'{self.api_url}/v1/search', search_params, headers)
+        if response.status_code == 200:
+            try:
+                return self.SearchResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
-            search_params = params
-            search_params.query = query
-
-        response = requests.post(
-            f""{self.api_url}/v1/search"",
-            headers={""Authorization"": f""Bearer {self.api_key}""},
-            json=search_params.dict(exclude_none=True)
-        )
-
-        if response.status_code != 200:
-            raise Exception(f""Request failed with status code {response.status_code}"")
-
-        try:
-            return response.json()
-        except:
-            raise Exception(f'Failed to parse Firecrawl response as JSON.')
+            self._handle_error(response, ""search"")
 
-    def crawl_url(self, url: str,
-                  params: Optional[Dict[str, Any]] = None,
-                  poll_interval: Optional[int] = 2,
-                  idempotency_key: Optional[str] = None) -> Any:
+    def crawl_url(
+            self,
+            url: str,
+            params: Optional[CrawlParams] = None,
+            poll_interval: int = 2,
+            idempotency_key: Optional[str] = None) -> CrawlStatusResponse:
         """"""
-        Initiate a crawl job for the specified URL using the Firecrawl API.
+        Crawl a website starting from a URL and monitor until completion.
 
         Args:
-            url (str): The URL to crawl.
-            params (Optional[Dict[str, Any]]): Additional parameters for the crawl request.
-            poll_interval (Optional[int]): Time in seconds between status checks when waiting for job completion. Defaults to 2 seconds.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            url (str): Target URL to start crawling from
+            params (Optional[CrawlParams]): See CrawlParams model for configuration:
+              URL Discovery:
+              * includePaths - Patterns of URLs to include
+              * excludePaths - Patterns of URLs to exclude
+              * maxDepth - Maximum crawl depth
+              * maxDiscoveryDepth - Maximum depth for finding new URLs
+              * limit - Maximum pages to crawl
+
+              Link Following:
+              * allowBackwardLinks - Follow parent directory links
+              * allowExternalLinks - Follow external domain links  
+              * ignoreSitemap - Skip sitemap.xml processing
+
+              Advanced:
+              * scrapeOptions - Page scraping configuration
+              * webhook - Notification webhook settings
+              * deduplicateSimilarURLs - Remove similar URLs
+              * ignoreQueryParameters - Ignore URL parameters
+              * regexOnFullURL - Apply regex to full URLs
+            poll_interval (int): Seconds between status checks (default: 2)
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            Dict[str, Any]: A dictionary containing the crawl results. The structure includes:
-                - 'success' (bool): Indicates if the crawl was successful.
-                - 'status' (str): The final status of the crawl job (e.g., 'completed').
-                - 'completed' (int): Number of scraped pages that completed.
-                - 'total' (int): Total number of scraped pages.
-                - 'creditsUsed' (int): Estimated number of API credits used for this crawl.
-                - 'expiresAt' (str): ISO 8601 formatted date-time string indicating when the crawl data expires.
-                - 'data' (List[Dict]): List of all the scraped pages.
+            CrawlStatusResponse: Object containing crawl status and crawled data
 
         Raises:
-            Exception: If the crawl job initiation or monitoring fails.
+            Exception: If the crawl job fails or an error occurs during status checks
         """"""
         endpoint = f'/v1/crawl'
         headers = self._prepare_headers(idempotency_key)
-        json_data = {'url': url}
+        json_data = {'url': url, 'origin': f""python-sdk@{version}""}
         if params:
-            json_data.update(params)
+            json_data.update(params.dict(exclude_none=True))
         response = self._post_request(f'{self.api_url}{endpoint}', json_data, headers)
         if response.status_code == 200:
             try:
                 id = response.json().get('id')
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                if not id:
+                    raise Exception('No job ID returned from crawl request')
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             return self._monitor_job_status(id, headers, poll_interval)
-
         else:
             self._handle_error(response, 'start crawl job')
 
 
-    def async_crawl_url(self, url: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
+    def async_crawl_url(
+            self,
+            url: str, 
+            params: Optional[CrawlParams] = None, 
+            idempotency_key: Optional[str] = None) -> CrawlResponse:
         """"""
-        Initiate a crawl job asynchronously.
+        Initiate a crawl job asynchronously without waiting for completion.
 
         Args:
-            url (str): The URL to crawl.
-            params (Optional[Dict[str, Any]]): Additional parameters for the crawl request.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            url (str): Target URL to start crawling from
+            params (Optional[CrawlParams]): See CrawlParams model for configuration:
+              URL Discovery:
+              * includePaths - Patterns of URLs to include
+              * excludePaths - Patterns of URLs to exclude
+              * maxDepth - Maximum crawl depth
+              * maxDiscoveryDepth - Maximum depth for finding new URLs
+              * limit - Maximum pages to crawl
+              
+              Link Following:
+              * allowBackwardLinks - Follow parent directory links
+              * allowExternalLinks - Follow external domain links  
+              * ignoreSitemap - Skip sitemap.xml processing
+              
+              Advanced:
+              * scrapeOptions - Page scraping configuration
+              * webhook - Notification webhook settings
+              * deduplicateSimilarURLs - Remove similar URLs
+              * ignoreQueryParameters - Ignore URL parameters
+              * regexOnFullURL - Apply regex to full URLs
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            Dict[str, Any]: A dictionary containing the crawl initiation response. The structure includes:
-                - 'success' (bool): Indicates if the crawl initiation was successful.
-                - 'id' (str): The unique identifier for the crawl job.
-                - 'url' (str): The URL to check the status of the crawl job.
+            CrawlResponse: Object containing crawl job initiation status and ID
+
+        Raises:
+            Exception: If the crawl job initiation fails
         """"""
         endpoint = f'/v1/crawl'
         headers = self._prepare_headers(idempotency_key)
-        json_data = {'url': url}
+        json_data = {'url': url, 'origin': f""python-sdk@{version}""}
         if params:
-            json_data.update(params)
+            json_data.update(params.dict(exclude_none=True))
         response = self._post_request(f'{self.api_url}{endpoint}', json_data, headers)
         if response.status_code == 200:
             try:
-                return response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                return CrawlResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, 'start crawl job')
 
-    def check_crawl_status(self, id: str) -> Any:
+    def check_crawl_status(self, id: str) -> CrawlStatusResponse:
         """"""
-        Check the status of a crawl job using the Firecrawl API.
+        Check the status of a crawl job.
 
         Args:
-            id (str): The ID of the crawl job.
+            id (str): Unique identifier of the crawl job
 
         Returns:
-            Any: The status of the crawl job.
+            CrawlStatusResponse: Object containing crawl status and crawled data
 
         Raises:
-            Exception: If the status check request fails.
+            Exception: If the status check request fails or returns an error
         """"""
         endpoint = f'/v1/crawl/{id}'
 
@@ -383,89 +786,112 @@ def check_crawl_status(self, id: str) -> Any:
             if 'next' in status_data:
                 response['next'] = status_data['next']
 
-            return {
+            result = {
                 'success': False if 'error' in status_data else True,
                 **response
             }
+            return CrawlStatusResponse(**result)
         else:
             self._handle_error(response, 'check crawl status')
     
-    def check_crawl_errors(self, id: str) -> Dict[str, Any]:
+    def check_crawl_errors(self, id: str) -> CrawlErrorsResponse:
         """"""
-        Returns information about crawl errors.
+        Get information about errors encountered during a crawl job.
 
         Args:
-            id (str): The ID of the crawl job.
+            id (str): Unique identifier of the crawl job
 
         Returns:
-            Dict[str, Any]: Information about crawl errors.
+            CrawlErrorsResponse: Object containing error details for the crawl job
+
+        Raises:
+            Exception: If the request fails or returns an error
         """"""
         headers = self._prepare_headers()
         response = self._get_request(f'{self.api_url}/v1/crawl/{id}/errors', headers)
         if response.status_code == 200:
             try:
-                return response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                return CrawlErrorsResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, ""check crawl errors"")
     
-    def cancel_crawl(self, id: str) -> Dict[str, Any]:
+    def cancel_crawl(self, id: str) -> CrawlResponse:
         """"""
-        Cancel an asynchronous crawl job using the Firecrawl API.
+        Cancel an in-progress crawl job.
 
         Args:
-            id (str): The ID of the crawl job to cancel.
+            id (str): Unique identifier of the crawl job to cancel
 
         Returns:
-            Dict[str, Any]: The response from the cancel crawl request.
+            CrawlResponse: Object containing cancellation status
+
+        Raises:
+            Exception: If the cancellation request fails or returns an error
         """"""
         headers = self._prepare_headers()
         response = self._delete_request(f'{self.api_url}/v1/crawl/{id}', headers)
         if response.status_code == 200:
             try:
-                return response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                return CrawlResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, ""cancel crawl job"")
 
-    def crawl_url_and_watch(self, url: str, params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> 'CrawlWatcher':
+    def crawl_url_and_watch(
+            self, 
+            url: str, 
+            params: Optional[CrawlParams] = None, 
+            idempotency_key: Optional[str] = None) -> 'CrawlWatcher':
         """"""
-        Initiate a crawl job and return a CrawlWatcher to monitor the job via WebSocket.
+        Initiate a crawl job and return a watcher for real-time monitoring.
 
         Args:
-            url (str): The URL to crawl.
-            params (Optional[Dict[str, Any]]): Additional parameters for the crawl request.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            url (str): Target URL to start crawling from
+            params (Optional[CrawlParams]): Configuration parameters for the crawl
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            CrawlWatcher: An instance of CrawlWatcher to monitor the crawl job.
+            CrawlWatcher: WebSocket-based monitor for the crawl job
+
+        Raises:
+            Exception: If the crawl job fails to start
         """"""
         crawl_response = self.async_crawl_url(url, params, idempotency_key)
-        if crawl_response['success'] and 'id' in crawl_response:
-            return CrawlWatcher(crawl_response['id'], self)
+        if crawl_response.success and hasattr(crawl_response, 'id'):
+            return CrawlWatcher(crawl_response.id, self)
         else:
             raise Exception(""Crawl job failed to start"")
 
-    def map_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
+    def map_url(self, url: str, params: Optional[MapParams] = None) -> MapResponse:
         """"""
-        Perform a map search using the Firecrawl API.
+        Map a website's structure to discover all available URLs.
 
         Args:
-            url (str): The URL to perform the map search on.
-            params (Optional[Dict[str, Any]]): Additional parameters for the map search.
+            url (str): Target URL to map
+            params (Optional[MapParams]): Configuration parameters including:
+              * includePaths - Patterns of URLs to include
+              * excludePaths - Patterns of URLs to exclude
+              * maxDepth - Maximum crawl depth
+              * ignoreSitemap - Skip sitemap.xml processing
+              * ignoreRobots - Ignore robots.txt restrictions
+              * ignoreQueryParameters - Ignore URL parameters
 
         Returns:
-            List[str]: A list of URLs discovered during the map search.
+            MapResponse: Object containing discovered URLs and status information
+
+        Raises:
+            Exception: If the map request fails or returns an error
         """"""
         endpoint = f'/v1/map'
         headers = self._prepare_headers()
 
         # Prepare the base scrape parameters with the URL
-        json_data = {'url': url}
+        json_data = {'url': url, 'origin': f""python-sdk@{version}""}
         if params:
-            json_data.update(params)
+            json_data.update(params.dict(exclude_none=True))
 
         # Make the POST request with the prepared headers and JSON data
         response = requests.post(
@@ -475,120 +901,144 @@ def map_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
         )
         if response.status_code == 200:
             try:
-                response = response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
-            if response['success'] and 'links' in response:
-                return response
-            elif 'error' in response:
-                raise Exception(f'Failed to map URL. Error: {response[""error""]}')
+                response_data = response.json()
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
+            if response_data['success'] and 'links' in response_data:
+                return MapResponse(**response_data)
+            elif 'error' in response_data:
+                raise Exception(f'Failed to map URL. Error: {response_data[""error""]}')
             else:
-                raise Exception(f'Failed to map URL. Error: {response}')
+                raise Exception(f'Failed to map URL. Error: {response_data}')
         else:
             self._handle_error(response, 'map')
 
-    def batch_scrape_urls(self, urls: List[str],
-                  params: Optional[Dict[str, Any]] = None,
-                  poll_interval: Optional[int] = 2,
-                  idempotency_key: Optional[str] = None) -> Any:
+    def batch_scrape_urls(
+            self, 
+            urls: List[str],
+            params: Optional[ScrapeParams] = None,
+            poll_interval: int = 2,
+            idempotency_key: Optional[str] = None) -> BatchScrapeStatusResponse:
         """"""
-        Initiate a batch scrape job for the specified URLs using the Firecrawl API.
+        Scrape multiple URLs in a batch operation and wait for completion.
 
         Args:
-            urls (List[str]): The URLs to scrape.
-            params (Optional[Dict[str, Any]]): Additional parameters for the scraper.
-            poll_interval (Optional[int]): Time in seconds between status checks when waiting for job completion. Defaults to 2 seconds.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            urls (List[str]): List of URLs to scrape
+            params (Optional[ScrapeParams]): Configuration parameters including:
+              * wait - Wait actions to perform before scraping
+              * screenshot - Screenshot configuration
+              * click - Click actions to perform
+              * write - Text input actions
+              * press - Keyboard press actions
+              * scroll - Scroll actions
+              * scrape - Scrape configuration
+              * executeJavascript - JavaScript to execute
+            poll_interval (int): Seconds between status checks (default: 2)
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            Dict[str, Any]: A dictionary containing the scrape results. The structure includes:
-                - 'success' (bool): Indicates if the batch scrape was successful.
-                - 'status' (str): The final status of the batch scrape job (e.g., 'completed').
-                - 'completed' (int): Number of scraped pages that completed.
-                - 'total' (int): Total number of scraped pages.
-                - 'creditsUsed' (int): Estimated number of API credits used for this batch scrape.
-                - 'expiresAt' (str): ISO 8601 formatted date-time string indicating when the batch scrape data expires.
-                - 'data' (List[Dict]): List of all the scraped pages.
+            BatchScrapeStatusResponse: Object containing batch scrape results
 
         Raises:
-            Exception: If the batch scrape job initiation or monitoring fails.
+            Exception: If the batch scrape job fails or an error occurs during status checks
         """"""
         endpoint = f'/v1/batch/scrape'
         headers = self._prepare_headers(idempotency_key)
-        json_data = {'urls': urls}
+        json_data = {'urls': urls, 'origin': f""python-sdk@{version}""}
         if params:
-            json_data.update(params)
+            json_data.update(params.dict(exclude_none=True))
         response = self._post_request(f'{self.api_url}{endpoint}', json_data, headers)
         if response.status_code == 200:
             try:
                 id = response.json().get('id')
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                if not id:
+                    raise Exception('No job ID returned from batch scrape request')
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             return self._monitor_job_status(id, headers, poll_interval)
 
         else:
             self._handle_error(response, 'start batch scrape job')
 
 
-    def async_batch_scrape_urls(self, urls: List[str], params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
+    def async_batch_scrape_urls(
+            self, 
+            urls: List[str], 
+            params: Optional[ScrapeParams] = None, 
+            idempotency_key: Optional[str] = None) -> BatchScrapeResponse:
         """"""
-        Initiate a crawl job asynchronously.
+        Initiate a batch scrape job asynchronously without waiting for completion.
 
         Args:
-            urls (List[str]): The URLs to scrape.
-            params (Optional[Dict[str, Any]]): Additional parameters for the scraper.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            urls (List[str]): List of URLs to scrape
+            params (Optional[ScrapeParams]): Configuration parameters including:
+              * wait - Wait actions to perform before scraping
+              * screenshot - Screenshot configuration
+              * click - Click actions to perform
+              * write - Text input actions
+              * press - Keyboard press actions
+              * scroll - Scroll actions
+              * scrape - Scrape configuration
+              * executeJavascript - JavaScript to execute
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            Dict[str, Any]: A dictionary containing the batch scrape initiation response. The structure includes:
-                - 'success' (bool): Indicates if the batch scrape initiation was successful.
-                - 'id' (str): The unique identifier for the batch scrape job.
-                - 'url' (str): The URL to check the status of the batch scrape job.
+            BatchScrapeResponse: Object containing batch scrape job initiation status and ID
+
+        Raises:
+            Exception: If the batch scrape job initiation fails
         """"""
         endpoint = f'/v1/batch/scrape'
         headers = self._prepare_headers(idempotency_key)
-        json_data = {'urls': urls}
+        json_data = {'urls': urls, 'origin': f""python-sdk@{version}""}
         if params:
-            json_data.update(params)
+            json_data.update(params.dict(exclude_none=True))
         response = self._post_request(f'{self.api_url}{endpoint}', json_data, headers)
         if response.status_code == 200:
             try:
-                return response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                return BatchScrapeResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, 'start batch scrape job')
     
-    def batch_scrape_urls_and_watch(self, urls: List[str], params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> 'CrawlWatcher':
+    def batch_scrape_urls_and_watch(
+            self, 
+            urls: List[str], 
+            params: Optional[ScrapeParams] = None, 
+            idempotency_key: Optional[str] = None) -> 'CrawlWatcher':
         """"""
-        Initiate a batch scrape job and return a CrawlWatcher to monitor the job via WebSocket.
+        Initiate a batch scrape job and return a watcher for real-time monitoring.
 
         Args:
-            urls (List[str]): The URLs to scrape.
-            params (Optional[Dict[str, Any]]): Additional parameters for the scraper.
-            idempotency_key (Optional[str]): A unique uuid key to ensure idempotency of requests.
+            urls (List[str]): List of URLs to scrape
+            params (Optional[ScrapeParams]): Configuration parameters for the scrape
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            CrawlWatcher: An instance of CrawlWatcher to monitor the batch scrape job.
+            CrawlWatcher: WebSocket-based monitor for the batch scrape job
+
+        Raises:
+            Exception: If the batch scrape job fails to start
         """"""
         crawl_response = self.async_batch_scrape_urls(urls, params, idempotency_key)
-        if crawl_response['success'] and 'id' in crawl_response:
-            return CrawlWatcher(crawl_response['id'], self)
+        if crawl_response.success and hasattr(crawl_response, 'id'):
+            return CrawlWatcher(crawl_response.id, self)
         else:
             raise Exception(""Batch scrape job failed to start"")
     
-    def check_batch_scrape_status(self, id: str) -> Any:
+    def check_batch_scrape_status(self, id: str) -> BatchScrapeStatusResponse:
         """"""
-        Check the status of a batch scrape job using the Firecrawl API.
+        Check the status of a batch scrape job.
 
         Args:
-            id (str): The ID of the batch scrape job.
+            id (str): Unique identifier of the batch scrape job
 
         Returns:
-            Any: The status of the batch scrape job.
+            BatchScrapeStatusResponse: Object containing batch scrape status and results
 
         Raises:
-            Exception: If the status check request fails.
+            Exception: If the status check request fails or returns an error
         """"""
         endpoint = f'/v1/batch/scrape/{id}'
 
@@ -597,8 +1047,8 @@ def check_batch_scrape_status(self, id: str) -> Any:
         if response.status_code == 200:
             try:
                 status_data = response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             if status_data['status'] == 'completed':
                 if 'data' in status_data:
                     data = status_data['data']
@@ -616,16 +1066,17 @@ def check_batch_scrape_status(self, id: str) -> Any:
                                 break
                             try:
                                 next_data = status_response.json()
-                            except:
-                                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                            except Exception as e:
+                                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
                             data.extend(next_data.get('data', []))
                             status_data = next_data
                         except Exception as e:
                             logger.error(f""Error during pagination request: {e}"")
                             break
                     status_data['data'] = data
 
-            response = {
+            response_dict = {
+                'success': False if 'error' in status_data else True,
                 'status': status_data.get('status'),
                 'total': status_data.get('total'),
                 'completed': status_data.get('completed'),
@@ -635,48 +1086,60 @@ def check_batch_scrape_status(self, id: str) -> Any:
             }
 
             if 'error' in status_data:
-                response['error'] = status_data['error']
+                response_dict['error'] = status_data['error']
 
             if 'next' in status_data:
-                response['next'] = status_data['next']
+                response_dict['next'] = status_data['next']
 
-            return {
-                'success': False if 'error' in status_data else True,
-                **response
-            }
+            return BatchScrapeStatusResponse(**response_dict)
         else:
             self._handle_error(response, 'check batch scrape status')
 
-    def check_batch_scrape_errors(self, id: str) -> Dict[str, Any]:
+    def check_batch_scrape_errors(self, id: str) -> CrawlErrorsResponse:
         """"""
-        Returns information about batch scrape errors.
+        Get error information for a batch scrape job.
 
         Args:
-            id (str): The ID of the crawl job.
+            id (str): Unique identifier of the batch scrape job
 
         Returns:
-            Dict[str, Any]: Information about crawl errors.
+            CrawlErrorsResponse: Object containing error details for the batch scrape
+
+        Raises:
+            Exception: If the error check request fails or returns an error
         """"""
         headers = self._prepare_headers()
         response = self._get_request(f'{self.api_url}/v1/batch/scrape/{id}/errors', headers)
         if response.status_code == 200:
             try:
-                return response.json()
-            except:
-                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                return CrawlErrorsResponse(**response.json())
+            except Exception as e:
+                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
         else:
             self._handle_error(response, ""check batch scrape errors"")
 
-    def extract(self, urls: Optional[List[str]] = None, params: Optional[ExtractParams] = None) -> Any:
+    def extract(
+            self, 
+            urls: Optional[List[str]] = None, 
+            params: Optional[ExtractParams] = None) -> ExtractResponse[Any]:
         """"""
-        Extracts information from a URL using the Firecrawl API.
+        Extract structured data from URLs using LLMs.
 
         Args:
-            urls (Optional[List[str]]): The URLs to extract information from.
-            params (Optional[ExtractParams]): Additional parameters for the extract request.
+            urls (Optional[List[str]]): URLs to extract data from
+            params (Optional[ExtractParams]): Configuration parameters including:
+              * prompt - Extraction prompt for the LLM
+              * schema - JSON schema for structured extraction
+              * agent - Agent configuration for extraction
+              * scrapeOptions - Page scraping configuration
+              * extractionOptions - Additional extraction options
 
         Returns:
-            Union[ExtractResponse, ErrorResponse]: The response from the extract operation.
+            ExtractResponse[Any]: Object containing extraction results
+
+        Raises:
+            ValueError: If required parameters are missing
+            Exception: If the extraction request fails or returns an error
         """"""
         headers = self._prepare_headers()
 
@@ -741,68 +1204,78 @@ def extract(self, urls: Optional[List[str]] = None, params: Optional[ExtractPara
                         if status_response.status_code == 200:
                             try:
                                 status_data = status_response.json()
-                            except:
-                                raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                            except Exception as e:
+                                raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
                             if status_data['status'] == 'completed':
                                 if status_data['success']:
-                                    return status_data
+                                    return self.ExtractResponse(**status_data)
                                 else:
-                                    raise Exception(f'Failed to extract. Error: {status_data[""error""]}')
+                                    raise Exception(f'Failed to extract. Error: {status_data.get(""error"", ""Unknown error"")}')
                             elif status_data['status'] in ['failed', 'cancelled']:
-                                raise Exception(f'Extract job {status_data[""status""]}. Error: {status_data[""error""]}')
+                                raise Exception(f'Extract job {status_data[""status""]}. Error: {status_data.get(""error"", ""Unknown error"")}')
                         else:
                             self._handle_error(status_response, ""extract-status"")
 
                         time.sleep(2)  # Polling interval
                 else:
-                    raise Exception(f'Failed to extract. Error: {data[""error""]}')
+                    raise Exception(f'Failed to extract. Error: {data.get(""error"", ""Unknown error"")}')
             else:
                 self._handle_error(response, ""extract"")
         except Exception as e:
             raise ValueError(str(e), 500)
 
-        return {'success': False, 'error': ""Internal server error.""}
+        return self.ExtractResponse(success=False, error=""Internal server error."")
     
-    def get_extract_status(self, job_id: str) -> Dict[str, Any]:
+    def get_extract_status(self, job_id: str) -> ExtractResponse[Any]:
         """"""
-        Retrieve the status of an extract job.
+        Check the status of an extraction job.
 
         Args:
-            job_id (str): The ID of the extract job.
+            job_id (str): Unique identifier of the extraction job
 
         Returns:
-            Dict[str, Any]: The status of the extract job.
+            ExtractResponse[Any]: Object containing extraction status and results
 
         Raises:
-            ValueError: If there is an error retrieving the status.
+            ValueError: If there is an error retrieving the status
+            Exception: If the status check request fails or returns an error
         """"""
         headers = self._prepare_headers()
         try:
             response = self._get_request(f'{self.api_url}/v1/extract/{job_id}', headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                    return self.ExtractResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             else:
                 self._handle_error(response, ""get extract status"")
         except Exception as e:
             raise ValueError(str(e), 500)
 
-    def async_extract(self, urls: List[str], params: Optional[Dict[str, Any]] = None, idempotency_key: Optional[str] = None) -> Dict[str, Any]:
+    def async_extract(
+            self, 
+            urls: List[str], 
+            params: Optional[ExtractParams] = None, 
+            idempotency_key: Optional[str] = None) -> ExtractResponse[Any]:
         """"""
-        Initiate an asynchronous extract job.
+        Initiate an asynchronous extraction job without waiting for completion.
 
         Args:
-            urls (List[str]): The URLs to extract data from.
-            params (Optional[Dict[str, Any]]): Additional parameters for the extract request.
-            idempotency_key (Optional[str]): A unique key to ensure idempotency of requests.
+            urls (List[str]): URLs to extract data from
+            params (Optional[ExtractParams]): Configuration parameters including:
+              * prompt - Extraction prompt for the LLM
+              * schema - JSON schema for structured extraction
+              * agent - Agent configuration for extraction
+              * scrapeOptions - Page scraping configuration
+              * extractionOptions - Additional extraction options
+            idempotency_key (Optional[str]): Unique key to prevent duplicate requests
 
         Returns:
-            Dict[str, Any]: The response from the extract operation.
+            ExtractResponse[Any]: Object containing extraction job initiation status and ID
 
         Raises:
-            ValueError: If there is an error initiating the extract job.
+            ValueError: If there is an error initiating the extract job
         """"""
         headers = self._prepare_headers(idempotency_key)
         
@@ -825,32 +1298,36 @@ def async_extract(self, urls: List[str], params: Optional[Dict[str, Any]] = None
             response = self._post_request(f'{self.api_url}/v1/extract', request_data, headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception(f'Failed to parse Firecrawl response as JSON.')
+                    return self.ExtractResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             else:
                 self._handle_error(response, ""async extract"")
         except Exception as e:
             raise ValueError(str(e), 500)
 
-    def generate_llms_text(self, url: str, params: Optional[Union[Dict[str, Any], GenerateLLMsTextParams]] = None) -> Dict[str, Any]:
+    def generate_llms_text(self, url: str, params: Optional[GenerateLLMsTextParams] = None) -> GenerateLLMsTextStatusResponse:
         """"""
         Generate LLMs.txt for a given URL and poll until completion.
 
         Args:
-            url (str): The URL to generate LLMs.txt from.
-            params (Optional[Union[Dict[str, Any], GenerateLLMsTextParams]]): Parameters for the LLMs.txt generation.
+            url (str): The URL to generate LLMs.txt from
+            params (Optional[GenerateLLMsTextParams]): Configuration parameters including:
+              * prompt - Custom prompt for the LLM
+              * model - LLM model to use
+              * temperature - Sampling temperature for generation
+              * maxTokens - Maximum tokens to generate
 
         Returns:
-            Dict[str, Any]: A dictionary containing the generation results. The structure includes:
-                - 'success' (bool): Indicates if the generation was successful.
-                - 'status' (str): The final status of the generation job.
-                - 'data' (Dict): The generated LLMs.txt data.
-                - 'error' (Optional[str]): Error message if the generation failed.
-                - 'expiresAt' (str): ISO 8601 formatted date-time string indicating when the data expires.
+            GenerateLLMsTextStatusResponse: Object containing generation results including:
+              * success - Whether the generation was successful
+              * status - Final status of the generation job
+              * data - The generated LLMs.txt data
+              * error - Error message if generation failed
+              * expiresAt - Expiration timestamp for the data
 
         Raises:
-            Exception: If the generation job fails or an error occurs during status checks.
+            Exception: If the generation job fails or an error occurs during status checks
         """"""
         if params is None:
             params = {}
@@ -861,36 +1338,38 @@ def generate_llms_text(self, url: str, params: Optional[Union[Dict[str, Any], Ge
             generation_params = params
 
         response = self.async_generate_llms_text(url, generation_params)
-        if not response.get('success') or 'id' not in response:
-            return response
+        if not response.success or not hasattr(response, 'id'):
+            return GenerateLLMsTextStatusResponse(**response.dict())
 
-        job_id = response['id']
+        job_id = response.id
         while True:
             status = self.check_generate_llms_text_status(job_id)
             
-            if status['status'] == 'completed':
+            if status.status == 'completed':
                 return status
-            elif status['status'] == 'failed':
-                raise Exception(f'LLMs.txt generation failed. Error: {status.get(""error"")}')
-            elif status['status'] != 'processing':
+            elif status.status == 'failed':
+                raise Exception(f'LLMs.txt generation failed. Error: {status.error if hasattr(status, ""error"") else ""Unknown error""}')
+            elif status.status != 'processing':
                 break
 
             time.sleep(2)  # Polling interval
 
-        return {'success': False, 'error': 'LLMs.txt generation job terminated unexpectedly'}
+        return GenerateLLMsTextStatusResponse(success=False, error='LLMs.txt generation job terminated unexpectedly')
 
-    def async_generate_llms_text(self, url: str, params: Optional[Union[Dict[str, Any], GenerateLLMsTextParams]] = None) -> Dict[str, Any]:
+    def async_generate_llms_text(self, url: str, params: Optional[GenerateLLMsTextParams] = None) -> GenerateLLMsTextResponse:
         """"""
-        Initiate an asynchronous LLMs.txt generation operation.
+        Initiate an asynchronous LLMs.txt generation job without waiting for completion.
 
         Args:
-            url (str): The URL to generate LLMs.txt from.
-            params (Optional[Union[Dict[str, Any], GenerateLLMsTextParams]]): Parameters for the LLMs.txt generation.
+            url (str): URL to generate LLMs.txt from
+            params (Optional[GenerateLLMsTextParams]): Configuration parameters including:
+              * prompt - Custom prompt for the LLM
+              * model - LLM model to use
+              * temperature - Sampling temperature for generation
+              * maxTokens - Maximum tokens to generate
 
         Returns:
-            Dict[str, Any]: A dictionary containing the generation initiation response. The structure includes:
-                - 'success' (bool): Indicates if the generation initiation was successful.
-                - 'id' (str): The unique identifier for the generation job.
+            GenerateLLMsTextResponse: Object containing generation job initiation status and ID
 
         Raises:
             Exception: If the generation job initiation fails.
@@ -910,45 +1389,50 @@ def async_generate_llms_text(self, url: str, params: Optional[Union[Dict[str, An
             response = self._post_request(f'{self.api_url}/v1/llmstxt', json_data, headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception('Failed to parse Firecrawl response as JSON.')
+                    return GenerateLLMsTextResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             else:
                 self._handle_error(response, 'start LLMs.txt generation')
         except Exception as e:
             raise ValueError(str(e))
 
-        return {'success': False, 'error': 'Internal server error'}
+        return GenerateLLMsTextResponse(success=False, error='Internal server error')
 
-    def check_generate_llms_text_status(self, id: str) -> Dict[str, Any]:
+    def check_generate_llms_text_status(self, id: str) -> GenerateLLMsTextStatusResponse:
         """"""
-        Check the status of a LLMs.txt generation operation.
+        Check the status of a LLMs.txt generation job.
 
         Args:
-            id (str): The ID of the LLMs.txt generation operation.
+            id (str): ID of the LLMs.txt generation job to check
 
         Returns:
-            Dict[str, Any]: The current status and results of the generation operation.
+            GenerateLLMsTextStatusResponse: Object containing generation job status including:
+              * success - Whether the status check was successful
+              * status - Current status of the generation job
+              * data - Generated LLMs.txt data if job is completed
+              * error - Error message if job failed
+              * expiresAt - Expiration timestamp for the data
 
         Raises:
-            Exception: If the status check fails.
+            Exception: If the status check request fails or returns an error
         """"""
         headers = self._prepare_headers()
         try:
             response = self._get_request(f'{self.api_url}/v1/llmstxt/{id}', headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception('Failed to parse Firecrawl response as JSON.')
+                    return GenerateLLMsTextStatusResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             elif response.status_code == 404:
                 raise Exception('LLMs.txt generation job not found')
             else:
                 self._handle_error(response, 'check LLMs.txt generation status')
         except Exception as e:
             raise ValueError(str(e))
 
-        return {'success': False, 'error': 'Internal server error'}
+        return GenerateLLMsTextStatusResponse(success=False, error='Internal server error')
 
     def _prepare_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
         """"""
@@ -1136,22 +1620,36 @@ def _handle_error(self, response: requests.Response, action: str) -> None:
         # Raise an HTTPError with the custom message and attach the response
         raise requests.exceptions.HTTPError(message, response=response)
 
-    def deep_research(self, query: str, params: Optional[Union[Dict[str, Any], DeepResearchParams]] = None, 
-                     on_activity: Optional[Callable[[Dict[str, Any]], None]] = None,
-                     on_source: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
+    def deep_research(
+            self, 
+            query: str, 
+            params: Optional[DeepResearchParams] = None, 
+            on_activity: Optional[Callable[[Dict[str, Any]], None]] = None,
+            on_source: Optional[Callable[[Dict[str, Any]], None]] = None) -> DeepResearchStatusResponse:
         """"""
         Initiates a deep research operation on a given query and polls until completion.
 
         Args:
-            query (str): The query to research.
-            params (Optional[Union[Dict[str, Any], DeepResearchParams]]): Parameters for the deep research operation.
-            on_activity (Optional[Callable[[Dict[str, Any]], None]]): Optional callback to receive activity updates in real-time.
+            query (str): The query to research
+            params (Optional[DeepResearchParams]): Configuration parameters including:
+              * maxSources - Maximum number of sources to use
+              * maxDepth - Maximum depth for research
+              * searchParams - Parameters for search operations
+              * scrapeOptions - Configuration for page scraping
+              * extractionOptions - Options for content extraction
+            on_activity (Optional[Callable[[Dict[str, Any]], None]]): Callback for activity updates
+            on_source (Optional[Callable[[Dict[str, Any]], None]]): Callback for source updates
 
         Returns:
-            Dict[str, Any]: The final research results.
+            DeepResearchStatusResponse: Object containing research results including:
+              * success - Whether the research was successful
+              * status - Final status of the research job
+              * activities - List of research activities performed
+              * sources - List of sources used in the research
+              * results - Final research results and analysis
 
         Raises:
-            Exception: If the research operation fails.
+            Exception: If the research operation fails
         """"""
         if params is None:
             params = {}
@@ -1162,51 +1660,56 @@ def deep_research(self, query: str, params: Optional[Union[Dict[str, Any], DeepR
             research_params = params
 
         response = self.async_deep_research(query, research_params)
-        if not response.get('success') or 'id' not in response:
-            return response
+        if not response.success or not hasattr(response, 'id'):
+            return DeepResearchStatusResponse(**response.dict())
 
-        job_id = response['id']
+        job_id = response.id
         last_activity_count = 0
         last_source_count = 0
 
         while True:
             status = self.check_deep_research_status(job_id)
             
-            if on_activity and 'activities' in status:
-                new_activities = status['activities'][last_activity_count:]
+            if on_activity and hasattr(status, 'activities') and status.activities:
+                new_activities = status.activities[last_activity_count:]
                 for activity in new_activities:
                     on_activity(activity)
-                last_activity_count = len(status['activities'])
+                last_activity_count = len(status.activities)
             
-            if on_source and 'sources' in status:
-                new_sources = status['sources'][last_source_count:]
+            if on_source and hasattr(status, 'sources') and status.sources:
+                new_sources = status.sources[last_source_count:]
                 for source in new_sources:
                     on_source(source)
-                last_source_count = len(status['sources'])
+                last_source_count = len(status.sources)
             
-            if status['status'] == 'completed':
+            if status.status == 'completed':
                 return status
-            elif status['status'] == 'failed':
-                raise Exception(f'Deep research failed. Error: {status.get(""error"")}')
-            elif status['status'] != 'processing':
+            elif status.status == 'failed':
+                raise Exception(f'Deep research failed. Error: {status.error if hasattr(status, ""error"") else ""Unknown error""}')
+            elif status.status != 'processing':
                 break
 
             time.sleep(2)  # Polling interval
 
-        return {'success': False, 'error': 'Deep research job terminated unexpectedly'}
-    def async_deep_research(self, query: str, params: Optional[Union[Dict[str, Any], DeepResearchParams]] = None) -> Dict[str, Any]:
+        return DeepResearchStatusResponse(success=False, error='Deep research job terminated unexpectedly')
+    def async_deep_research(self, query: str, params: Optional[DeepResearchParams] = None) -> DeepResearchResponse:
         """"""
-        Initiates an asynchronous deep research operation.
+        Initiates an asynchronous deep research job without waiting for completion.
 
         Args:
-            query (str): The query to research.
-            params (Optional[Union[Dict[str, Any], DeepResearchParams]]): Parameters for the deep research operation.
+            query (str): The query to research
+            params (Optional[DeepResearchParams]): Configuration parameters including:
+              * maxSources - Maximum number of sources to use
+              * maxDepth - Maximum depth for research
+              * searchParams - Parameters for search operations
+              * scrapeOptions - Configuration for page scraping
+              * extractionOptions - Options for content extraction
 
         Returns:
-            Dict[str, Any]: The response from the deep research initiation.
+            DeepResearchResponse: Object containing research job initiation status and ID
 
         Raises:
-            Exception: If the research initiation fails.
+            Exception: If the research initiation fails
         """"""
         if params is None:
             params = {}
@@ -1230,45 +1733,50 @@ def async_deep_research(self, query: str, params: Optional[Union[Dict[str, Any],
             response = self._post_request(f'{self.api_url}/v1/deep-research', json_data, headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception('Failed to parse Firecrawl response as JSON.')
+                    return DeepResearchResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             else:
                 self._handle_error(response, 'start deep research')
         except Exception as e:
             raise ValueError(str(e))
 
-        return {'success': False, 'error': 'Internal server error'}
+        return DeepResearchResponse(success=False, error='Internal server error')
 
-    def check_deep_research_status(self, id: str) -> Dict[str, Any]:
+    def check_deep_research_status(self, id: str) -> DeepResearchStatusResponse:
         """"""
-        Check the status of a deep research operation.
+        Check the status of a deep research job.
 
         Args:
-            id (str): The ID of the deep research operation.
+            id (str): ID of the deep research job to check
 
         Returns:
-            Dict[str, Any]: The current status and results of the research operation.
+            DeepResearchStatusResponse: Object containing research job status including:
+              * success - Whether the status check was successful
+              * status - Current status of the research job
+              * activities - List of research activities performed
+              * sources - List of sources used in the research
+              * results - Final research results and analysis
 
         Raises:
-            Exception: If the status check fails.
+            Exception: If the status check request fails or returns an error
         """"""
         headers = self._prepare_headers()
         try:
             response = self._get_request(f'{self.api_url}/v1/deep-research/{id}', headers)
             if response.status_code == 200:
                 try:
-                    return response.json()
-                except:
-                    raise Exception('Failed to parse Firecrawl response as JSON.')
+                    return DeepResearchStatusResponse(**response.json())
+                except Exception as e:
+                    raise Exception(f'Failed to parse Firecrawl response as JSON: {str(e)}')
             elif response.status_code == 404:
                 raise Exception('Deep research job not found')
             else:
                 self._handle_error(response, 'check deep research status')
         except Exception as e:
             raise ValueError(str(e))
 
-        return {'success': False, 'error': 'Internal server error'}
+        return DeepResearchStatusResponse(success=False, error='Internal server error')
 
 class CrawlWatcher:
     def __init__(self, id: str, app: FirecrawlApp):