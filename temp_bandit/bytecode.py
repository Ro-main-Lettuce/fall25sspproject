@@ -126,6 +126,15 @@ def size(self):
         """"""
         return len(self.__buff)
 
+    def can_read(self, size):
+        """"""
+        Check if we can read `size` bytes from current position
+        
+        :param int size: number of bytes to check
+        :rtype: bool
+        """"""
+        return self.__idx + size <= len(self.__buff)
+
     def length_buff(self):
         """"""
         Alias for :meth:`size`