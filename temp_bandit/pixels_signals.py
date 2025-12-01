@@ -11,7 +11,7 @@
   script.async = true;
   window.signals = Object.assign(
     [],
-    ['page', 'identify', 'form'].reduce(function (acc, method){
+    ['page', 'identify', 'form', 'track'].reduce(function (acc, method){
       acc[method] = function () {
         signals.push([method, arguments]);
         return signals;