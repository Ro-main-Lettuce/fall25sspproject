@@ -79,7 +79,7 @@ def hosting_patterns() -> rx.Component:
         rx.image(
             src=""/hosting/light/hosting_patterns.svg"",
             alt=""Reflex Hosting Patterns"",
-            class_name=""dark:hidden desktop-only absolute top-0 z-[-1] w-[1028px] h-[478px] pointer-events-none shrink-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2""
+            class_name=""dark:hidden lg:flex hidden absolute top-0 z-[-1] w-[1028px] h-[478px] pointer-events-none shrink-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2""
             + rx.cond(
                 HostingBannerState.show_banner,
                 "" lg:mt-[24rem] mt-[3.5rem]"",
@@ -89,7 +89,7 @@ def hosting_patterns() -> rx.Component:
         rx.image(
             src=""/hosting/dark/hosting_patterns.svg"",
             alt=""Reflex Hosting Patterns"",
-            class_name=""dark:flex hidden desktop-only absolute top-0 z-[-1] w-[1028px] h-[478px] pointer-events-none shrink-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2""
+            class_name=""hidden dark:flex lg:dark:flex absolute top-0 z-[-1] w-[1028px] h-[478px] pointer-events-none shrink-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2""
             + rx.cond(
                 HostingBannerState.show_banner,
                 "" lg:mt-[24rem] mt-[3.5rem]"",