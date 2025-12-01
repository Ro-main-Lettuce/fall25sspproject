@@ -70,7 +70,6 @@ def wrapper(*children, **props) -> rx.Component:
                 ),
                 bottom_section(),
                 footer(),
-                badge(),
                 class_name=""relative flex flex-col justify-start items-center w-full h-full min-h-screen font-instrument-sans overflow-hidden"",
                 **props,
             )