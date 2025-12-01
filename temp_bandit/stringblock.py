@@ -17,8 +17,10 @@
 
 import logging
 from struct import unpack
+from typing import BinaryIO, Union, Optional
 
 import pyaxmlparser.constants as const
+from pyaxmlparser.exceptions import StringBlockError, ValidationError
 
 
 log = logging.getLogger(""pyaxmlparser.stringblock"")
@@ -62,7 +64,7 @@ def __init__(self, buff, header):
 
         self.m_stringOffsets = []
         self.m_styleOffsets = []
-        self.m_charbuff = """"
+        self.m_charbuff = b""""
         self.m_styles = []
 
         # Next, there is a list of string following.
@@ -116,7 +118,7 @@ def __iter__(self):
         for i in range(self.stringCount):
             yield self.getString(i)
 
-    def getString(self, idx):
+    def getString(self, idx: int) -> str:
         """"""
         Return the string at the index in the string table
 
@@ -131,29 +133,38 @@ def getString(self, idx):
 
         offset = self.m_stringOffsets[idx]
 
-        if self.m_isUTF8:
-            self._cache[idx] = self._decode8(offset)
-        else:
-            self._cache[idx] = self._decode16(offset)
+        try:
+            if self.m_isUTF8:
+                self._cache[idx] = self._decode8(offset)
+            else:
+                self._cache[idx] = self._decode16(offset)
+        except (IndexError, UnicodeDecodeError, AssertionError) as e:
+            log.error(f""Failed to decode string at index {idx}, offset {offset}: {e}"")
+            raise StringBlockError(f""Failed to decode string at index {idx}"") from e
 
         return self._cache[idx]
 
-    def getStyle(self, idx):
+    def getStyle(self, idx: int) -> int:
         """"""
         Return the style associated with the index
 
         :param idx: index of the style
         :return:
         """"""
+        if idx < 0 or idx >= len(self.m_styles):
+            raise StringBlockError(f""Style index {idx} out of range"")
         return self.m_styles[idx]
 
-    def _decode8(self, offset):
+    def _decode8(self, offset: int) -> str:
         """"""
         Decode an UTF-8 String at the given offset
 
         :param offset: offset of the string inside the data
         :return: str
         """"""
+        if offset >= len(self.m_charbuff):
+            raise StringBlockError(f""UTF-8 string offset {offset} beyond buffer size {len(self.m_charbuff)}"")
+
         # UTF-8 Strings contain two lengths, as they might differ:
         # 1) the UTF-16 length
         str_len, skip = self._decode_length(offset, 1)
@@ -163,35 +174,45 @@ def _decode8(self, offset):
         encoded_bytes, skip = self._decode_length(offset, 1)
         offset += skip
 
+        if offset + encoded_bytes >= len(self.m_charbuff):
+            raise StringBlockError(f""UTF-8 string data extends beyond buffer"")
+
         data = self.m_charbuff[offset: offset + encoded_bytes]
 
-        assert self.m_charbuff[offset + encoded_bytes] == 0, \
-            ""UTF-8 String is not null terminated! At offset={}"".format(offset)
+        if offset + encoded_bytes >= len(self.m_charbuff) or self.m_charbuff[offset + encoded_bytes] != 0:
+            raise StringBlockError(f""UTF-8 String is not null terminated at offset {offset}"")
 
         return self._decode_bytes(data, 'utf-8', str_len)
 
-    def _decode16(self, offset):
+    def _decode16(self, offset: int) -> str:
         """"""
         Decode an UTF-16 String at the given offset
 
         :param offset: offset of the string inside the data
         :return: str
         """"""
+        if offset >= len(self.m_charbuff):
+            raise StringBlockError(f""UTF-16 string offset {offset} beyond buffer size {len(self.m_charbuff)}"")
+
         str_len, skip = self._decode_length(offset, 2)
         offset += skip
 
         # The len is the string len in utf-16 units
         encoded_bytes = str_len * 2
 
+        if offset + encoded_bytes + 2 > len(self.m_charbuff):
+            raise StringBlockError(f""UTF-16 string data extends beyond buffer"")
+
         data = self.m_charbuff[offset: offset + encoded_bytes]
 
-        assert self.m_charbuff[offset + encoded_bytes:offset + encoded_bytes + 2] == b""\x00\x00"", \
-            ""UTF-16 String is not null terminated! At offset={}"".format(offset)
+        null_terminator = self.m_charbuff[offset + encoded_bytes:offset + encoded_bytes + 2]
+        if null_terminator != b""\x00\x00"":
+            raise StringBlockError(f""UTF-16 String is not null terminated at offset {offset}"")
 
         return self._decode_bytes(data, 'utf-16', str_len)
 
     @staticmethod
-    def _decode_bytes(data, encoding, str_len):
+    def _decode_bytes(data: bytes, encoding: str, str_len: int) -> str:
         """"""
         Generic decoding with length check.
         The string is decoded from bytes with the given encoding, then the length
@@ -203,12 +224,16 @@ def _decode_bytes(data, encoding, str_len):
         :param str_len: length of the decoded string
         :return: str
         """"""
-        string = data.decode(encoding, 'replace')
+        try:
+            string = data.decode(encoding, 'replace')
+        except UnicodeDecodeError as e:
+            raise StringBlockError(f""Failed to decode {encoding} string: {e}"") from e
+        
         if len(string) != str_len:
-            log.warning(""invalid decoded string length"")
+            log.warning(f""Decoded string length {len(string)} does not match expected length {str_len}"")
         return string
 
-    def _decode_length(self, offset, sizeof_char):
+    def _decode_length(self, offset: int, sizeof_char: int) -> tuple[int, int]:
         """"""
         Generic Length Decoding at offset of string
 
@@ -228,7 +253,13 @@ def _decode_length(self, offset, sizeof_char):
         fmt = ""<2{}"".format('B' if sizeof_char == 1 else 'H')
         highbit = 0x80 << (8 * (sizeof_char - 1))
 
-        length1, length2 = unpack(fmt, self.m_charbuff[offset:(offset + sizeof_2chars)])
+        if offset + sizeof_2chars > len(self.m_charbuff):
+            raise StringBlockError(f""Length decode extends beyond buffer at offset {offset}"")
+
+        try:
+            length1, length2 = unpack(fmt, self.m_charbuff[offset:(offset + sizeof_2chars)])
+        except Exception as e:
+            raise StringBlockError(f""Failed to unpack length at offset {offset}: {e}"") from e
 
         if (length1 & highbit) != 0:
             length = ((length1 & ~highbit) << (8 * sizeof_char)) | length2
@@ -238,9 +269,11 @@ def _decode_length(self, offset, sizeof_char):
             size = sizeof_char
 
         if sizeof_char == 1:
-            assert length <= 0x7FFF, ""length of UTF-8 string is too large! At offset={}"".format(offset)
+            if length > 0x7FFF:
+                raise StringBlockError(f""UTF-8 string length {length} too large at offset {offset}"")
         else:
-            assert length <= 0x7FFFFFFF, ""length of UTF-16 string is too large!  At offset={}"".format(offset)
+            if length > 0x7FFFFFFF:
+                raise StringBlockError(f""UTF-16 string length {length} too large at offset {offset}"")
 
         return length, size
 