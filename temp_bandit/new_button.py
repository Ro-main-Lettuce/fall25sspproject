@@ -22,7 +22,7 @@ def get_variant_bg_cn(variant: str) -> str:
         str: The background color class name.
 
     """"""
-    return f""enabled:bg-gradient-to-b from-[--{variant}-9] to-[--{variant}-10] dark:to-[--{variant}-9] hover:to-[--{variant}-9] dark:hover:to-[--{variant}-10] disabled:hover:bg-[--{variant}-9]""
+    return f""enabled:bg-gradient-to-b from-(--{variant}-9) to-(--{variant}-10) dark:to-(--{variant}-9) hover:to-(--{variant}-9) dark:hover:to-(--{variant}-10) disabled:hover:bg-(--{variant}-9)""
 
 
 BUTTON_STYLES: Dict[str, Dict[str, Dict[str, str]]] = {