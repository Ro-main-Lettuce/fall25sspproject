@@ -6,14 +6,14 @@
     ""primary"", ""success"", ""destructive"", ""secondary"", ""muted""
 ]
 
-default_class_name = ""font-smbold rounded-xl cursor-pointer inline-flex items-center justify-center px-[0.875rem] py-2 relative transition-bg border-t border-[rgba(255,255,255,0.21)]""
+default_class_name = ""text-sm font-semibold rounded-xl cursor-pointer inline-flex items-center justify-center px-[0.875rem] py-2 relative transition-bg border-t""
 
 after_class_name = ""after:absolute after:inset-[1px] after:border-t after:rounded-[11px] after:border-white after:opacity-[0.22]""
 
 
 def get_variant_class(variant: str) -> str:
     return (
-        f""bg-gradient-to-b from-[--{variant}-9] to-[--{variant}-9] hover:to-[--{variant}-10] text-white""
+        f""bg-gradient-to-b from-(--{variant}-9) to-(--{variant}-9) hover:to-(--{variant}-10) text-white""
         + "" ""
     )
 