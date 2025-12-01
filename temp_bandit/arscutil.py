@@ -129,10 +129,10 @@ def __init__(self, buff, parent=None):
             self.id = unpack('<B', buff.read(1))[0]
             self.res0 = unpack('<B', buff.read(1))[0]
             if self.res0 != 0:
-                log.warning(""res0 is not zero!"")
+                log.debug(""res0 is not zero!"")
             self.res1 = unpack('<H', buff.read(2))[0]
             if self.res1 != 0:
-                log.warning(""res1 is not zero!"")
+                log.debug(""res1 is not zero!"")
             self.entryCount = unpack(""<I"", buff.read(4))[0]
 
             self.typespec_entries = []
@@ -529,24 +529,58 @@ def __init__(self, buff, mResId, parent=None):
         self.parent = parent
         
         try:
+            if not buff.can_read(8):
+                log.warning(""Insufficient buffer for ARSCResTableEntry at offset %d"", self.start)
+                self.size = 0
+                self.flags = 0
+                self.index = 0
+                self.item = None
+                self.key = None
+                return
+                
             self.size = unpack('<H', buff.read(2))[0]
             self.flags = unpack('<H', buff.read(2))[0]
             self.index = unpack('<I', buff.read(4))[0]
 
             if self.is_complex():
-                self.item = ARSCComplex(buff, parent)
+                try:
+                    self.item = ARSCComplex(buff, parent)
+                except Exception as complex_e:
+                    log.warning(""Failed to parse ARSCComplex in ARSCResTableEntry: %s"", complex_e)
+                    self.item = None
             else:
                 # If FLAG_COMPLEX is not set, a Res_value structure will follow
-                self.key = ARSCResStringPoolRef(buff, self.parent)
+                try:
+                    self.key = ARSCResStringPoolRef(buff, self.parent)
+                except Exception as ref_e:
+                    log.warning(""Failed to parse ARSCResStringPoolRef in ARSCResTableEntry: %s"", ref_e)
+                    self.key = None
         except Exception as e:
-            log.error(""Failed to parse ARSCResTableEntry at offset %d: %s"", self.start, e)
-            raise ResParserError(f""Buffer validation failed in ARSCResTableEntry at offset {self.start}"") from e
+            log.warning(""Failed to parse ARSCResTableEntry at offset %d, using defaults: %s"", self.start, e)
+            self.size = 0
+            self.flags = 0
+            self.index = 0
+            self.item = None
+            self.key = None
 
     def get_index(self):
         return self.index
 
     def get_value(self):
-        return self.parent.mKeyStrings.getString(self.index)
+        if self.is_complex():
+            return ""(complex)""
+        elif self.key and hasattr(self.key, 'get_data_value'):
+            try:
+                return self.key.get_data_value()
+            except Exception as e:
+                log.debug(""Failed to get data value from key: %s"", e)
+                return ""(name removed)""
+        else:
+            try:
+                return self.parent.mKeyStrings.getString(self.index)
+            except Exception as e:
+                log.debug(""Failed to get string from mKeyStrings: %s"", e)
+                return ""(name removed)""
 
     def get_key_data(self):
         return self.key.get_data_value()
@@ -579,16 +613,33 @@ def __init__(self, buff, parent=None):
         self.parent = parent
 
         try:
+            if not buff.can_read(8):
+                log.warning(""Insufficient buffer for ARSCComplex at offset %d"", self.start)
+                self.id_parent = 0
+                self.count = 0
+                self.items = []
+                return
+                
             self.id_parent = unpack('<I', buff.read(4))[0]
             self.count = unpack('<I', buff.read(4))[0]
 
             self.items = []
             for i in range(0, self.count):
-                self.items.append((unpack('<I', buff.read(4))[0],
-                                   ARSCResStringPoolRef(buff, self.parent)))
+                if not buff.can_read(4):
+                    log.warning(""Insufficient buffer for ARSCComplex item %d at offset %d"", i, buff.get_idx())
+                    break
+                try:
+                    item_id = unpack('<I', buff.read(4))[0]
+                    string_ref = ARSCResStringPoolRef(buff, self.parent)
+                    self.items.append((item_id, string_ref))
+                except Exception as item_e:
+                    log.warning(""Failed to parse ARSCComplex item %d: %s"", i, item_e)
+                    break
         except Exception as e:
-            log.error(""Failed to parse ARSCComplex at offset %d: %s"", self.start, e)
-            raise ResParserError(f""Buffer validation failed in ARSCComplex at offset {self.start}"") from e
+            log.warning(""Failed to parse ARSCComplex at offset %d, using defaults: %s"", self.start, e)
+            self.id_parent = 0
+            self.count = 0
+            self.items = []
 
     def __repr__(self):
         return ""<ARSCComplex idx='0x{:08x}' parent='{}' count='{}'>"".format(self.start, self.id_parent, self.count)
@@ -600,15 +651,26 @@ def __init__(self, buff, parent=None):
         self.parent = parent
 
         try:
+            if not buff.can_read(8):
+                log.warning(""Insufficient buffer for ARSCResStringPoolRef at offset %d"", self.start)
+                self.size = 0
+                self.res0 = 0
+                self.data_type = 0
+                self.data = 0
+                return
+                
             self.size, = unpack(""<H"", buff.read(2))
             self.res0, = unpack(""<B"", buff.read(1))
             if self.res0 != 0:
-                log.warning(""res0 is not zero!"")
+                log.debug(""res0 is not zero!"")
             self.data_type = unpack('<B', buff.read(1))[0]
             self.data = unpack('<I', buff.read(4))[0]
         except Exception as e:
-            log.error(""Failed to parse ARSCResStringPoolRef at offset %d: %s"", self.start, e)
-            raise ResParserError(f""Buffer validation failed in ARSCResStringPoolRef at offset {self.start}"") from e
+            log.warning(""Failed to parse ARSCResStringPoolRef at offset %d, using defaults: %s"", self.start, e)
+            self.size = 0
+            self.res0 = 0
+            self.data_type = 0
+            self.data = 0
 
     def get_data_value(self):
         return self.parent.stringpool_main.getString(self.data)