@@ -20,10 +20,13 @@
 import binascii
 import logging
 
+from typing import Optional
+
 from pyaxmlparser.axmlparser import AXMLParser
 from pyaxmlparser.utils import format_value
 import pyaxmlparser.constants as const
 from lxml import etree
+from pyaxmlparser.exceptions import ValidationError
 
 log = logging.getLogger(""pyaxmlparser.axmlprinter"")
 
@@ -39,75 +42,82 @@ class AXMLPrinter:
     __charrange = None
     __replacement = None
 
-    def __init__(self, raw_buff):
+    def __init__(self, raw_buff: Optional[bytes]):
         self.axml = AXMLParser(raw_buff)
 
         self.root = None
         self.packerwarning = False
         cur = []
 
-        while self.axml.is_valid():
-            _type = next(self.axml)
+        if not self.axml.is_valid():
+            return
 
-            if _type == const.START_TAG:
-                name = self._fix_name(self.axml.name)
-                uri = self._print_namespace(self.axml.namespace)
-                tag = ""{}{}"".format(uri, name)
+        try:
+            while self.axml.is_valid():
+                _type = next(self.axml)
 
-                comment = self.axml.comment
-                if comment:
-                    if self.root is None:
-                        log.warning(""Can not attach comment with content '{}' without root!"".format(comment))
-                    else:
-                        cur[-1].append(etree.Comment(comment))
+                if _type == const.START_TAG:
+                    name = self._fix_name(self.axml.name)
+                    uri = self._print_namespace(self.axml.namespace)
+                    tag = ""{}{}"".format(uri, name)
+
+                    comment = self.axml.comment
+                    if comment:
+                        if self.root is None:
+                            log.warning(""Can not attach comment with content '{}' without root!"".format(comment))
+                        else:
+                            cur[-1].append(etree.Comment(comment))
 
-                log.debug(""START_TAG: {} (line={})"".format(tag, self.axml.m_lineNumber))
-                elem = etree.Element(tag, nsmap=self.axml.nsmap)
+                    log.debug(""START_TAG: {} (line={})"".format(tag, self.axml.m_lineNumber))
+                    elem = etree.Element(tag, nsmap=self.axml.nsmap)
 
-                for i in range(self.axml.getAttributeCount()):
-                    uri = self._print_namespace(self.axml.getAttributeNamespace(i))
-                    name = self._fix_name(self.axml.getAttributeName(i))
-                    value = self._fix_value(self._get_attribute_value(i))
+                    for i in range(self.axml.getAttributeCount()):
+                        uri = self._print_namespace(self.axml.getAttributeNamespace(i))
+                        name = self._fix_name(self.axml.getAttributeName(i))
+                        value = self._fix_value(self._get_attribute_value(i))
 
-                    log.debug(""found an attribute: {}{}='{}'"".format(uri, name, value.encode(""utf-8"")))
-                    if ""{}{}"".format(uri, name) in elem.attrib:
-                        log.warning(""Duplicate attribute '{}{}'! Will overwrite!"".format(uri, name))
-                    elem.set(""{}{}"".format(uri, name), value)
+                        log.debug(""found an attribute: {}{}='{}'"".format(uri, name, value.encode(""utf-8"")))
+                        if ""{}{}"".format(uri, name) in elem.attrib:
+                            log.warning(""Duplicate attribute '{}{}'! Will overwrite!"".format(uri, name))
+                        elem.set(""{}{}"".format(uri, name), value)
 
-                if self.root is None:
-                    self.root = elem
-                else:
+                    if self.root is None:
+                        self.root = elem
+                    else:
+                        if not cur:
+                            # looks like we lost the root?
+                            log.error(""No more elements available to attach to! Is the XML malformed?"")
+                            break
+                        cur[-1].append(elem)
+                    cur.append(elem)
+
+                if _type == const.END_TAG:
                     if not cur:
-                        # looks like we lost the root?
-                        log.error(""No more elements available to attach to! Is the XML malformed?"")
-                        break
-                    cur[-1].append(elem)
-                cur.append(elem)
-
-            if _type == const.END_TAG:
-                if not cur:
-                    log.warning(""Too many END_TAG! No more elements available to attach to!"")
-
-                name = self.axml.name
-                uri = self._print_namespace(self.axml.namespace)
-                tag = ""{}{}"".format(uri, name)
-                if cur[-1].tag != tag:
-                    log.warning(
-                        ""Closing tag '{}' does not match current stack! ""
-                        ""At line number: {}. Is the XML malformed?"".format(
-                            self.axml.name, self.axml.m_lineNumber
+                        log.warning(""Too many END_TAG! No more elements available to attach to!"")
+
+                    name = self.axml.name
+                    uri = self._print_namespace(self.axml.namespace)
+                    tag = ""{}{}"".format(uri, name)
+                    if cur[-1].tag != tag:
+                        log.warning(
+                            ""Closing tag '{}' does not match current stack! ""
+                            ""At line number: {}. Is the XML malformed?"".format(
+                                self.axml.name, self.axml.m_lineNumber
+                            )
                         )
-                    )
-                cur.pop()
-            if _type == const.TEXT:
-                log.debug(""TEXT for {}"".format(cur[-1]))
-                cur[-1].text = self.axml.text
-            if _type == const.END_DOCUMENT:
-                # Check if all namespace mappings are closed
-                if len(self.axml.namespaces) > 0:
-                    log.warning(
-                        ""Not all namespace mappings were closed! Malformed AXML?"")
-                break
+                    cur.pop()
+                if _type == const.TEXT:
+                    log.debug(""TEXT for {}"".format(cur[-1]))
+                    cur[-1].text = self.axml.text
+                if _type == const.END_DOCUMENT:
+                    # Check if all namespace mappings are closed
+                    if len(self.axml.namespaces) > 0:
+                        log.warning(
+                            ""Not all namespace mappings were closed! Malformed AXML?"")
+                    break
+        except Exception as e:
+            log.error(""Failed to parse AXML: %s"", e)
+            raise ValidationError(""Failed to parse AXML"") from e
 
     def get_buff(self):
         """"""
@@ -117,23 +127,25 @@ def get_buff(self):
         """"""
         return self.get_xml(pretty=False)
 
-    def get_xml(self, pretty=True):
+    def get_xml(self, pretty=True) -> str:
         """"""
         Get the XML as an UTF-8 string
 
-        :returns: bytes encoded as UTF-8
+        :returns: str encoded as UTF-8
         """"""
-        return etree.tostring(self.root, encoding=""utf-8"", pretty_print=pretty)
+        if self.root is None:
+            return """"
+        return etree.tostring(self.root, encoding=""utf-8"", pretty_print=pretty).decode(""utf-8"")
 
-    def get_xml_obj(self):
+    def get_xml_obj(self) -> Optional[etree._Element]:
         """"""
         Get the XML as an ElementTree object
 
         :returns: :class:`lxml.etree.Element`
         """"""
         return self.root
 
-    def is_valid(self):
+    def is_valid(self) -> bool:
         """"""
         Return the state of the AXMLParser.
         If this flag is set to False, the parsing has failed, thus
@@ -154,7 +166,7 @@ def is_packed(self):
         """"""
         return self.packerwarning
 
-    def _get_attribute_value(self, index):
+    def _get_attribute_value(self, index: int) -> str:
         """"""
         Wrapper function for format_value
         to resolve the actual value of an attribute in a tag
@@ -166,7 +178,7 @@ def _get_attribute_value(self, index):
 
         return format_value(_type, _data, lambda _: self.axml.getAttributeValue(index))
 
-    def _fix_name(self, name):
+    def _fix_name(self, name: str) -> str:
         """"""
         Apply some fixes to element named and attribute names.
         Try to get conform to:
@@ -177,6 +189,11 @@ def _fix_name(self, name):
         :param name: Name of the attribute
         :return: a fixed version of the name
         """"""
+        if not name:
+            log.warning(""Empty name provided"")
+            self.packerwarning = True
+            return ""_empty_name""
+            
         if not name[0].isalpha() and name[0] != ""_"":
             log.warning(""Invalid start for name '{}'"".format(name))
             self.packerwarning = True
@@ -203,7 +220,7 @@ def _fix_name(self, name):
 
         return name
 
-    def _fix_value(self, value):
+    def _fix_value(self, value: str) -> str:
         """"""
         Return a cleaned version of a value
         according to the specification:
@@ -214,6 +231,9 @@ def _fix_value(self, value):
         :param value: a value to clean
         :return: the cleaned value
         """"""
+        if value is None:
+            return """"
+            
         if not self.__charrange or not self.__replacement:
             if sys.maxunicode == 0xFFFF:
                 # Fix for python 2.x, surrogate pairs does not match in regex
@@ -243,7 +263,7 @@ def _fix_value(self, value):
             value = self.__replacement.sub('_', value)
         return value
 
-    def _print_namespace(self, uri):
+    def _print_namespace(self, uri: str) -> str:
         if uri != """":
             uri = ""{{{}}}"".format(uri)
         return uri