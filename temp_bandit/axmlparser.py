@@ -17,12 +17,14 @@
 
 import logging
 from struct import unpack
+from typing import Optional, Union, Any
 
 import pyaxmlparser.constants as const
 from pyaxmlparser import bytecode
 from pyaxmlparser.stringblock import StringBlock
 from pyaxmlparser.resources import public
 from .arscutil import ARSCHeader
+from pyaxmlparser.exceptions import ChunkError, NamespaceError, ValidationError
 
 log = logging.getLogger(""pyaxmlparser.axmlparser"")
 
@@ -50,11 +52,16 @@ class AXMLParser(object):
 
     See http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/include/androidfw/ResourceTypes.h#563
     """"""
-    def __init__(self, raw_buff):
+    def __init__(self, raw_buff: Optional[bytes]):
         self._reset()
 
         self._valid = True
         self.axml_tampered = False
+        
+        if raw_buff is None:
+            self._valid = False
+            return
+            
         self.buff = bytecode.BuffHandle(raw_buff)
 
         # Minimum is a single ARSCHeader, which would be a strange edge case...
@@ -72,7 +79,7 @@ def __init__(self, raw_buff):
 
         try:
             axml_header = ARSCHeader(self.buff)
-        except AssertionError as e:
+        except Exception as e:
             log.error(""Error parsing first resource header: %s"", e)
             self._valid = False
             return
@@ -128,7 +135,7 @@ def __init__(self, raw_buff):
         # Now we parse the STRING POOL
         try:
             header = ARSCHeader(self.buff)
-        except AssertionError as e:
+        except Exception as e:
             log.error(""Error parsing resource header of string pool: %s"", e)
             self._valid = False
             return
@@ -151,7 +158,12 @@ def __init__(self, raw_buff):
             self._valid = False
             return
 
-        self.sb = StringBlock(self.buff, header)
+        try:
+            self.sb = StringBlock(self.buff, header)
+        except Exception as e:
+            log.error(""Failed to initialize StringBlock: %s"", e)
+            self._valid = False
+            return
 
         # Stores resource ID mappings, if any
         self.m_resourceIDs = []
@@ -167,7 +179,7 @@ def is_valid(self):
         """"""
         return self._valid
 
-    def _reset(self):
+    def _reset(self) -> None:
         self.m_event = -1
         self.m_lineNumber = -1
         self.m_name = -1
@@ -177,13 +189,13 @@ def _reset(self):
         self.m_classAttribute = -1
         self.m_styleAttribute = -1
 
-    def __next__(self):
+    def __next__(self) -> int:
         self._do_next()
         return self.m_event
 
     next = __next__  # For Python 2 compatibility
 
-    def _do_next(self):
+    def _do_next(self) -> None:
         if self.m_event == const.END_DOCUMENT:
             return
 
@@ -197,7 +209,7 @@ def _do_next(self):
             # Again, we read an ARSCHeader
             try:
                 h = ARSCHeader(self.buff)
-            except AssertionError as e:
+            except Exception as e:
                 log.error(""Error parsing resource header: %s"", e)
                 self._valid = False
                 return
@@ -235,7 +247,7 @@ def _do_next(self):
                     ""At chunk type 0x{:04x}, declared header size={}, ""
                     ""chunk size={}"".format(h.type, h.header_size, h.size)
                 )
-                self.buff.seek(h.end)
+                self.buff.set_idx(h.end)
                 continue
 
             # Line Number of the source file, only used as meta information
@@ -252,132 +264,152 @@ def _do_next(self):
                 )
 
             if h.type == const.RES_XML_START_NAMESPACE_TYPE:
-                prefix, = unpack('<L', self.buff.read(4))
-                uri, = unpack('<L', self.buff.read(4))
-
-                s_prefix = self.sb[prefix]
-                s_uri = self.sb[uri]
-
-                log.debug(
-                    ""Start of Namespace mapping: prefix ""
-                    ""{}: '{}' --> uri {}: '{}'"".format(
-                        prefix, s_prefix, uri, s_uri
+                try:
+                    prefix, = unpack('<L', self.buff.read(4))
+                    uri, = unpack('<L', self.buff.read(4))
+
+                    s_prefix = self.sb[prefix]
+                    s_uri = self.sb[uri]
+
+                    log.debug(
+                        ""Start of Namespace mapping: prefix ""
+                        ""{}: '{}' --> uri {}: '{}'"".format(
+                            prefix, s_prefix, uri, s_uri
+                        )
                     )
-                )
 
-                if s_uri == '':
-                    log.warning(""Namespace prefix '{}' resolves to empty URI. ""
-                                ""This might be a packer."".format(s_prefix))
+                    if s_uri == '':
+                        log.warning(""Namespace prefix '{}' resolves to empty URI. ""
+                                    ""This might be a packer."".format(s_prefix))
 
-                if (prefix, uri) in self.namespaces:
-                    log.info(
-                        ""Namespace mapping ({}, {}) already seen! ""
-                        ""This is usually not a problem but could indicate ""
-                        ""packers or broken AXML compilers."".format(prefix, uri))
-                self.namespaces.append((prefix, uri))
+                    if (prefix, uri) in self.namespaces:
+                        log.info(
+                            ""Namespace mapping ({}, {}) already seen! ""
+                            ""This is usually not a problem but could indicate ""
+                            ""packers or broken AXML compilers."".format(prefix, uri))
+                    self.namespaces.append((prefix, uri))
+                except Exception as e:
+                    log.error(""Failed to process START_NAMESPACE: %s"", e)
+                    raise NamespaceError(""Failed to process namespace"") from e
 
                 # We can continue with the next chunk, as we store the namespace
                 # mappings for each tag
                 continue
 
             if h.type == const.RES_XML_END_NAMESPACE_TYPE:
-                # END_PREFIX contains again prefix and uri field
-                prefix, = unpack('<L', self.buff.read(4))
-                uri, = unpack('<L', self.buff.read(4))
-
-                # We remove the last namespace mapping matching
-                if (prefix, uri) in self.namespaces:
-                    self.namespaces.remove((prefix, uri))
-                else:
-                    log.warning(
-                        ""Reached a NAMESPACE_END without having the namespace stored before? ""
-                        ""Prefix ID: {}, URI ID: {}"".format(prefix, uri)
-                    )
+                try:
+                    # END_PREFIX contains again prefix and uri field
+                    prefix, = unpack('<L', self.buff.read(4))
+                    uri, = unpack('<L', self.buff.read(4))
+
+                    # We remove the last namespace mapping matching
+                    if (prefix, uri) in self.namespaces:
+                        self.namespaces.remove((prefix, uri))
+                    else:
+                        log.warning(
+                            ""Reached a NAMESPACE_END without having the namespace stored before? ""
+                            ""Prefix ID: {}, URI ID: {}"".format(prefix, uri)
+                        )
+                except Exception as e:
+                    log.error(""Failed to process END_NAMESPACE: %s"", e)
+                    raise NamespaceError(""Namespace stack underflow"") from e
 
                 # We can continue with the next chunk, as we store the namespace
                 # mappings for each tag
                 continue
 
             # START_TAG is the start of a new tag.
             if h.type == const.RES_XML_START_ELEMENT_TYPE:
-                # The TAG consists of some fields:
-                # * (chunk_size, line_number, comment_index - we read before)
-                # * namespace_uri
-                # * name
-                # * flags
-                # * attribute_count
-                # * class_attribute
-                # After that, there are two lists of attributes, 20 bytes each
-
-                # Namespace URI (String ID)
-                self.m_namespaceUri, = unpack('<L', self.buff.read(4))
-                # Name of the Tag (String ID)
-                self.m_name, = unpack('<L', self.buff.read(4))
-                # FIXME: Flags
-                _ = self.buff.read(4)  # noqa
-                # Attribute Count
-                attributeCount, = unpack('<L', self.buff.read(4))
-                # Class Attribute
-                self.m_classAttribute, = unpack('<L', self.buff.read(4))
-
-                self.m_idAttribute = (attributeCount >> 16) - 1
-                self.m_attribute_count = attributeCount & 0xFFFF
-                self.m_styleAttribute = (self.m_classAttribute >> 16) - 1
-                self.m_classAttribute = (self.m_classAttribute & 0xFFFF) - 1
-
-                # Now, we parse the attributes.
-                # Each attribute has 5 fields of 4 byte
-                for i in range(0, self.m_attribute_count * const.ATTRIBUTE_LENGHT):
-                    # Each field is linearly parsed into the array
-                    # Each Attribute contains:
-                    # * Namespace URI (String ID)
-                    # * Name (String ID)
-                    # * Value
-                    # * Type
-                    # * Data
-                    self.m_attributes.append(unpack('<L', self.buff.read(4))[0])
-
-                # Then there are class_attributes
-                for i in range(const.ATTRIBUTE_IX_VALUE_TYPE, len(self.m_attributes), const.ATTRIBUTE_LENGHT):
-                    self.m_attributes[i] = self.m_attributes[i] >> 24
-
-                self.m_event = const.START_TAG
-                break
+                try:
+                    # The TAG consists of some fields:
+                    # * (chunk_size, line_number, comment_index - we read before)
+                    # * namespace_uri
+                    # * name
+                    # * flags
+                    # * attribute_count
+                    # * class_attribute
+                    # After that, there are two lists of attributes, 20 bytes each
+
+                    # Namespace URI (String ID)
+                    self.m_namespaceUri, = unpack('<L', self.buff.read(4))
+                    # Name of the Tag (String ID)
+                    self.m_name, = unpack('<L', self.buff.read(4))
+                    # FIXME: Flags
+                    _ = self.buff.read(4)  # noqa
+                    # Attribute Count
+                    attributeCount, = unpack('<L', self.buff.read(4))
+                    # Class Attribute
+                    self.m_classAttribute, = unpack('<L', self.buff.read(4))
+
+                    self.m_idAttribute = (attributeCount >> 16) - 1
+                    self.m_attribute_count = attributeCount & 0xFFFF
+                    self.m_styleAttribute = (self.m_classAttribute >> 16) - 1
+                    self.m_classAttribute = (self.m_classAttribute & 0xFFFF) - 1
+
+                    # Now, we parse the attributes.
+                    # Each attribute has 5 fields of 4 byte
+                    for i in range(0, self.m_attribute_count * const.ATTRIBUTE_LENGHT):
+                        # Each field is linearly parsed into the array
+                        # Each Attribute contains:
+                        # * Namespace URI (String ID)
+                        # * Name (String ID)
+                        # * Value
+                        # * Type
+                        # * Data
+                        self.m_attributes.append(unpack('<L', self.buff.read(4))[0])
+
+                    # Then there are class_attributes
+                    for i in range(const.ATTRIBUTE_IX_VALUE_TYPE, len(self.m_attributes), const.ATTRIBUTE_LENGHT):
+                        self.m_attributes[i] = self.m_attributes[i] >> 24
+
+                    self.m_event = const.START_TAG
+                    break
+                except Exception as e:
+                    log.error(""Failed to process START_TAG: %s"", e)
+                    raise ChunkError(""Failed to process START_TAG"") from e
 
             if h.type == const.RES_XML_END_ELEMENT_TYPE:
-                self.m_namespaceUri, = unpack('<L', self.buff.read(4))
-                self.m_name, = unpack('<L', self.buff.read(4))
+                try:
+                    self.m_namespaceUri, = unpack('<L', self.buff.read(4))
+                    self.m_name, = unpack('<L', self.buff.read(4))
 
-                self.m_event = const.END_TAG
-                break
+                    self.m_event = const.END_TAG
+                    break
+                except Exception as e:
+                    log.error(""Failed to process END_TAG: %s"", e)
+                    raise ChunkError(""Failed to process END_TAG"") from e
 
             if h.type == const.RES_XML_CDATA_TYPE:
-                # The CDATA field is like an attribute.
-                # It contains an index into the String pool
-                # as well as a typed value.
-                # usually, this typed value is set to UNDEFINED
-
-                # ResStringPool_ref data --> uint32_t index
-                self.m_name, = unpack('<L', self.buff.read(4))
-
-                # Res_value typedData:
-                # uint16_t size
-                # uint8_t res0 -> always zero
-                # uint8_t dataType
-                # uint32_t data
-                # For now, we ingore these values
-                size, res0, dataType, data = unpack(""<HBBL"", self.buff.read(8))
-
-                log.debug(
-                    ""found a CDATA Chunk: ""
-                    ""index={: 6d}, size={: 4d}, res0={: 4d}, ""
-                    ""dataType={: 4d}, data={: 4d}"".format(
-                        self.m_name, size, res0, dataType, data
+                try:
+                    # The CDATA field is like an attribute.
+                    # It contains an index into the String pool
+                    # as well as a typed value.
+                    # usually, this typed value is set to UNDEFINED
+
+                    # ResStringPool_ref data --> uint32_t index
+                    self.m_name, = unpack('<L', self.buff.read(4))
+
+                    # Res_value typedData:
+                    # uint16_t size
+                    # uint8_t res0 -> always zero
+                    # uint8_t dataType
+                    # uint32_t data
+                    # For now, we ingore these values
+                    size, res0, dataType, data = unpack(""<HBBL"", self.buff.read(8))
+
+                    log.debug(
+                        ""found a CDATA Chunk: ""
+                        ""index={: 6d}, size={: 4d}, res0={: 4d}, ""
+                        ""dataType={: 4d}, data={: 4d}"".format(
+                            self.m_name, size, res0, dataType, data
+                        )
                     )
-                )
 
-                self.m_event = const.TEXT
-                break
+                    self.m_event = const.TEXT
+                    break
+                except Exception as e:
+                    log.error(""Failed to process CDATA: %s"", e)
+                    raise ChunkError(""Failed to process CDATA"") from e
 
             # Still here? Looks like we read an unknown XML header, try to skip it...
             log.warning(""Unknown XML Chunk: 0x{:04x}, skipping {} bytes."".format(h.type, h.size))
@@ -421,7 +453,7 @@ def namespace(self):
         return self.sb[self.m_namespaceUri]
 
     @property
-    def nsmap(self):
+    def nsmap(self) -> dict[str, str]:
         """"""
         Returns the current namespace mapping as a dictionary
 
@@ -437,12 +469,16 @@ def nsmap(self):
         NSMAP = dict()
         # solve 3) by using a set
         for k, v in set(self.namespaces):
-            s_prefix = self.sb[k]
-            s_uri = self.sb[v]
-            # Solve 2) & 4) by not including
-            if s_uri != """" and s_prefix != """":
-                # solve 1) by using the last one in the list
-                NSMAP[s_prefix] = s_uri.strip()
+            try:
+                s_prefix = self.sb[k]
+                s_uri = self.sb[v]
+                # Solve 2) & 4) by not including
+                if s_uri != """" and s_prefix != """":
+                    # solve 1) by using the last one in the list
+                    NSMAP[s_prefix] = s_uri.strip()
+            except Exception as e:
+                log.warning(""Failed to process namespace mapping: %s"", e)
+                continue
 
         return NSMAP
 
@@ -477,7 +513,7 @@ def getPrefix(self):
         """"""
         return self.namespace
 
-    def _get_attribute_offset(self, index):
+    def _get_attribute_offset(self, index: int) -> int:
         """"""
         Return the start inside the m_attributes array for a given attribute
         """"""
@@ -490,7 +526,7 @@ def _get_attribute_offset(self, index):
 
         return offset
 
-    def getAttributeCount(self):
+    def getAttributeCount(self) -> int:
         """"""
         Return the number of Attributes for a Tag
         or -1 if not in a tag
@@ -500,7 +536,7 @@ def getAttributeCount(self):
 
         return self.m_attribute_count
 
-    def getAttributeUri(self, index):
+    def getAttributeUri(self, index: int) -> int:
         """"""
         Returns the numeric ID for the namespace URI of an attribute
         """"""
@@ -509,7 +545,7 @@ def getAttributeUri(self, index):
 
         return uri
 
-    def getAttributeNamespace(self, index):
+    def getAttributeNamespace(self, index: int) -> str:
         """"""
         Return the Namespace URI (if any) for the attribute
         """"""
@@ -521,7 +557,7 @@ def getAttributeNamespace(self, index):
 
         return self.sb[uri]
 
-    def getAttributeName(self, index):
+    def getAttributeName(self, index: int) -> str:
         """"""
         Returns the String which represents the attribute name
         """"""
@@ -531,17 +567,21 @@ def getAttributeName(self, index):
         res = self.sb[name]
         # If the result is a (null) string, we need to look it up.
         if not res:
-            attr = self.m_resourceIDs[name]
-            if attr in public.SYSTEM_RESOURCES['attributes']['inverse']:
-                res = 'android:' + public.SYSTEM_RESOURCES['attributes']['inverse'][attr]
-            else:
-                # Attach the HEX Number, so for multiple missing attributes we do not run
-                # into problems.
-                res = 'android:UNKNOWN_SYSTEM_ATTRIBUTE_{:08x}'.format(attr)
+            try:
+                attr = self.m_resourceIDs[name]
+                if attr in public.SYSTEM_RESOURCES['attributes']['inverse']:
+                    res = 'android:' + public.SYSTEM_RESOURCES['attributes']['inverse'][attr]
+                else:
+                    # Attach the HEX Number, so for multiple missing attributes we do not run
+                    # into problems.
+                    res = 'android:UNKNOWN_SYSTEM_ATTRIBUTE_{:08x}'.format(attr)
+            except (IndexError, KeyError) as e:
+                log.warning(""Failed to resolve attribute name: %s"", e)
+                res = 'android:UNKNOWN_ATTRIBUTE_{:08x}'.format(name)
 
         return res
 
-    def getAttributeValueType(self, index):
+    def getAttributeValueType(self, index: int) -> int:
         """"""
         Return the type of the attribute at the given index
 
@@ -550,7 +590,7 @@ def getAttributeValueType(self, index):
         offset = self._get_attribute_offset(index)
         return self.m_attributes[offset + const.ATTRIBUTE_IX_VALUE_TYPE]
 
-    def getAttributeValueData(self, index):
+    def getAttributeValueData(self, index: int) -> int:
         """"""
         Return the data of the attribute at the given index
 
@@ -559,7 +599,7 @@ def getAttributeValueData(self, index):
         offset = self._get_attribute_offset(index)
         return self.m_attributes[offset + const.ATTRIBUTE_IX_VALUE_DATA]
 
-    def getAttributeValue(self, index):
+    def getAttributeValue(self, index: int) -> str:
         """"""
         This function is only used to look up strings
         All other work is done by