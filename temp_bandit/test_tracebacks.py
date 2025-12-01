@@ -14,12 +14,12 @@
 class TestTracebacks:
     def test_highlight_traceback(self) -> None:
         # Test that _highlight_traceback adds HTML formatting
-        traceback = ""Traceback (most recent call last):
  File \""<stdin>\"", line 1, in <module>
ValueError: invalid value""
+        traceback = 'Traceback (most recent call last):
  File ""<stdin>"", line 1, in <module>
ValueError: invalid value'
 
         highlighted = _highlight_traceback(traceback)
 
         # Should contain HTML formatting
-        assert ""<span class=\""codehilite\"">"" in highlighted
+        assert '<span class=""codehilite"">' in highlighted
         assert ""</span>"" in highlighted
 
         # Should contain the original traceback text
@@ -33,15 +33,15 @@ def test_write_traceback_to_stderr(self) -> None:
         mock_stderr = MagicMock(spec=Stderr)
 
         with patch(""sys.stderr"", mock_stderr):
-            traceback = ""Traceback (most recent call last):
  File \""<stdin>\"", line 1, in <module>
ValueError: invalid value""
+            traceback = 'Traceback (most recent call last):
  File ""<stdin>"", line 1, in <module>
ValueError: invalid value'
             write_traceback(traceback)
 
             # Should call _write_with_mimetype with highlighted traceback
             mock_stderr._write_with_mimetype.assert_called_once()
 
             # First argument should be the highlighted traceback
             args, _ = mock_stderr._write_with_mimetype.call_args
-            assert ""<span class=\""codehilite\"">"" in args[0]
+            assert '<span class=""codehilite"">' in args[0]
             assert ""Traceback"" in args[0]
 
             # Second argument should be the mimetype
@@ -54,7 +54,7 @@ def test_write_traceback_to_regular_stderr(self) -> None:
         mock_stderr.write = MagicMock()
 
         with patch(""sys.stderr"", mock_stderr):
-            traceback = ""Traceback (most recent call last):
  File \""<stdin>\"", line 1, in <module>
ValueError: invalid value""
+            traceback = 'Traceback (most recent call last):
  File ""<stdin>"", line 1, in <module>
ValueError: invalid value'
             write_traceback(traceback)
 
             # Should call write with the original traceback
@@ -64,10 +64,18 @@ def test_is_code_highlighting(self) -> None:
         # Test is_code_highlighting function
 
         # Should return True for strings containing the codehilite class
-        assert is_code_highlighting(""<span class=\""codehilite\"">code</span>"") is True
-        assert is_code_highlighting(""before <span class=\""codehilite\"">code</span> after"") is True
+        assert (
+            is_code_highlighting('<span class=""codehilite"">code</span>')
+            is True
+        )
+        assert (
+            is_code_highlighting(
+                'before <span class=""codehilite"">code</span> after'
+            )
+            is True
+        )
 
         # Should return False for strings not containing the codehilite class
         assert is_code_highlighting(""<span>code</span>"") is False
         assert is_code_highlighting("""") is False
-        assert is_code_highlighting(""class=\""not-codehilite\"""") is False
+        assert is_code_highlighting('class=""not-codehilite""') is False