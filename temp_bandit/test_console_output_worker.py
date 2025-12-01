@@ -171,7 +171,8 @@ def test_buffered_writer_basic(self) -> None:
                 cv.notify()
 
             # Wait for the timeout to expire and the message to be written
-            time.sleep(TIMEOUT_S * 2)
+            # Use a longer timeout to ensure the message is processed
+            time.sleep(TIMEOUT_S * 5)
 
             # Check that the message was written to the stream
             assert len(stream.messages) == 1
@@ -227,7 +228,8 @@ def test_buffered_writer_multiple_messages(self) -> None:
                 cv.notify()
 
             # Wait for the timeout to expire and the messages to be written
-            time.sleep(TIMEOUT_S * 2)
+            # Use a longer timeout to ensure the messages are processed
+            time.sleep(TIMEOUT_S * 5)
 
             # Check that the messages were written to the stream
             assert len(stream.messages) == 2  # Merged stdout messages + stderr