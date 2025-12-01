@@ -299,48 +299,6 @@ def _test_block_hash(self,
             for node in nodes:
                 node.cleanup()
 
-    def test_block_hash_v1(self):
-        """"""Starts a cluster using protocol version 24 and verifies block hashes.
-
-        The cluster is started with a protocol version in which the first
-        version of the BlockHeaderInnerRest has been used.
-        """"""
-        self._test_block_hash(1, BLOCK_HEADER_V1_PROTOCOL_VERSION)
-
-    def test_block_hash_v2(self):
-        """"""Starts a cluster using protocol version 42 and verifies block hashes.
-
-        The cluster is started with a protocol version in which the second
-        version of the BlockHeaderInnerRest has been used.
-        """"""
-        self._test_block_hash(2, BLOCK_HEADER_V2_PROTOCOL_VERSION)
-
-    def test_block_hash_v3(self):
-        """"""Starts a cluster using protocol version 50 and verifies block hashes.
-
-        The cluster is started with a protocol version in which the third
-        version of the BlockHeaderInnerRest has been used.
-        """"""
-        self._test_block_hash(3, BLOCK_HEADER_V3_PROTOCOL_VERSION)
-
-    def test_block_hash_v4(self):
-        """"""Starts a cluster using protocol version 63 and verifies block hashes.
-
-        The cluster is started with a protocol version in which the fourth
-        version of the BlockHeaderInnerRest has been used.
-        """"""
-        self._test_block_hash(4, BLOCK_HEADER_V4_PROTOCOL_VERSION)
-
-    if binary_protocol_version >= BLOCK_HEADER_V5_PROTOCOL_VERSION:
-
-        def test_block_hash_v5(self):
-            """"""Starts a cluster using protocol version 145 and verifies block hashes.
-
-            The cluster is started with a protocol version in which the fifth
-            version of the BlockHeaderInnerRest has been used.
-            """"""
-            self._test_block_hash(5, BLOCK_HEADER_V5_PROTOCOL_VERSION)
-
     def test_block_hash_latest(self):
         """"""Starts a cluster using latest protocol and verifies block hashes.
 
@@ -349,10 +307,7 @@ def test_block_hash_latest(self):
         BlockHeaderInnerRest message has been introduced and this test needs to
         be updated to support it.
         """"""
-        if binary_protocol_version >= BLOCK_HEADER_V5_PROTOCOL_VERSION:
-            self._test_block_hash(5)
-        else:
-            self._test_block_hash(4)
+        self._test_block_hash(5)
 
 
 if __name__ == '__main__':