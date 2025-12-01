@@ -1,3 +1,4 @@
+import pytest
 from unittest.mock import MagicMock, patch
 
 from bs4 import BeautifulSoup
@@ -100,3 +101,53 @@ def test_webdriver_initialization(_mocked_chrome_driver):
     assert tool.driver is not None
     assert isinstance(tool.driver, MagicMock)
     _mocked_chrome_driver.assert_called_once()
+
+
+@patch(""selenium.webdriver.Chrome"")
+def test_webdriver_initialization_error(_mocked_chrome_driver):
+    """"""Test WebDriver initialization error handling.""""""
+    _mocked_chrome_driver.side_effect = Exception(""Driver error"")
+    tool = SeleniumScrapingTool()
+    with pytest.raises(RuntimeError) as exc_info:
+        _ = tool.driver
+    assert ""Failed to initialize WebDriver"" in str(exc_info.value)
+
+
+@patch(""selenium.webdriver.Chrome"")
+def test_cookie_handling(_mocked_chrome_driver):
+    """"""Test cookie setting functionality.""""""
+    mock_driver = MagicMock()
+    _mocked_chrome_driver.return_value = mock_driver
+    cookie = {""name"": ""test"", ""value"": ""value""}
+    
+    tool = SeleniumScrapingTool(cookie=cookie)
+    tool._create_driver(""https://example.com"", cookie, 1)
+    
+    mock_driver.add_cookie.assert_called_once_with(cookie)
+    mock_driver.get.assert_called_with(""https://example.com"")
+
+
+@patch(""selenium.webdriver.Chrome"")
+def test_context_manager(_mocked_chrome_driver):
+    """"""Test context manager functionality.""""""
+    mock_driver = MagicMock()
+    _mocked_chrome_driver.return_value = mock_driver
+    
+    with SeleniumScrapingTool() as tool:
+        tool.driver.get(""https://example.com"")
+    
+    mock_driver.quit.assert_called_once()
+    assert tool._driver is None
+
+
+@patch(""selenium.webdriver.Chrome"")
+def test_page_load_timeout(_mocked_chrome_driver):
+    """"""Test page load timeout handling.""""""
+    mock_driver = MagicMock()
+    _mocked_chrome_driver.return_value = mock_driver
+    mock_driver.get.side_effect = Exception(""Timeout"")
+    
+    tool = SeleniumScrapingTool()
+    with pytest.raises(RuntimeError) as exc_info:
+        tool._create_driver(""https://example.com"", None, 1)
+    assert ""Failed to load page"" in str(exc_info.value)