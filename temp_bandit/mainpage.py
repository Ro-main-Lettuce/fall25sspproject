@@ -69,7 +69,6 @@ def wrapper(*children, **props) -> rx.Component:
                     get_started(),
                     class_name=""flex flex-col w-full justify-center items-center"",
                 ),
-                badge(),
                 footer_index(),
                 class_name=""flex flex-col w-full max-w-[94.5rem] justify-center items-center mx-auto px-4 lg:px-5 relative overflow-hidden"",
                 padding_top=rx.cond(HostingBannerState.show_banner, ""56px"", ""0""),