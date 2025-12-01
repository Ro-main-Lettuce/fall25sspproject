@@ -155,48 +155,56 @@ def _render_price_display(price: str, title: str) -> rx.Component:
         return rx.el.div(
             rx.el.span(parts[0], class_name=""text-4xl font-bold text-slate-12""),
             rx.el.span(f""  {parts[1]}"", class_name=""text-sm text-slate-9 ml-2""),
-            class_name=""flex items-baseline""
+            class_name=""flex items-baseline"",
         )
     else:
         # Handle regular pricing (e.g., ""$25/month"", ""Custom"")
         main_price = price.split(""/"")[0] if ""/"" in price else price
         period = f"" / {price.split('/')[1]}"" if ""/"" in price else """"
-        
+
         return rx.el.div(
             rx.el.span(main_price, class_name=""text-4xl font-bold text-slate-12""),
             rx.el.span(period, class_name=""text-sm text-slate-9""),
-            class_name=""flex items-baseline""
+            class_name=""flex items-baseline"",
         )
 
 
 def _render_messaging_section(title: str) -> rx.Component:
     """"""Render the messaging/features section for each plan.""""""
     messaging_config = {
-        ""Hobby"": {
-            ""main"": """",
-            ""sub"": None
-        },
+        ""Hobby"": {""main"": """", ""sub"": None},
         ""Pro"": {
             ""main"": ""Reflex Build 100 msgs/month"",
-            ""sub"": rx.link(""Upgrade to Team for more messages"", href=""#reflex-build"",
-                          class_name=""text-xs text-slate-9 hover:text-slate-11 underline"")
+            ""sub"": rx.link(
+                ""Upgrade to Team for more messages"",
+                href=""#reflex-build"",
+                class_name=""text-xs text-slate-9 hover:text-slate-11 underline"",
+            ),
         },
         ""Team"": {
             ""main"": ""Reflex Build 250 msgs/month"",
-            ""sub"": rx.link(""More messages available on request"", href=""#reflex-build"",
-                          class_name=""text-xs text-slate-9 hover:text-slate-11 underline"")
+            ""sub"": rx.link(
+                ""More messages available on request"",
+                href=""#reflex-build"",
+                class_name=""text-xs text-slate-9 hover:text-slate-11 underline"",
+            ),
         },
         ""Enterprise"": {
             ""main"": ""Reflex Build 500+ msgs/month"",
-            ""sub"": rx.link(""More messages available on request"", href=""#reflex-build"",
-                          class_name=""text-xs text-slate-9 hover:text-slate-11 underline"")
-        }
+            ""sub"": rx.link(
+                ""More messages available on request"",
+                href=""#reflex-build"",
+                class_name=""text-xs text-slate-9 hover:text-slate-11 underline"",
+            ),
+        },
     }
-    
+
     if title in messaging_config:
         config = messaging_config[title]
         return rx.el.div(
-            rx.el.p(config[""main""], class_name=""text-md font-semibold text-slate-12 mt-4""),
+            rx.el.p(
+                config[""main""], class_name=""text-md font-semibold text-slate-12 mt-4""
+            ),
             config[""sub""] if config[""sub""] else None,
         )
     return rx.el.div()
@@ -208,7 +216,7 @@ def _get_features_header(title: str) -> str:
         ""Hobby"": ""Get started with:"",
         ""Pro"": ""Everything in the Free Plan, plus:"",
         ""Team"": ""Everything in the Pro Plan, plus:"",
-        ""Enterprise"": ""Everything in Team, plus:""
+        ""Enterprise"": ""Everything in Team, plus:"",
     }
     return headers.get(title, ""Features:"")
 
@@ -223,7 +231,9 @@ def _render_feature_list(features: list[tuple[str, str]]) -> rx.Component:
                 rx.tooltip(
                     rx.icon(""info"", class_name=""!text-slate-9"", size=12),
                     content=feature[2],
-                ) if len(feature) == 3 else """",
+                )
+                if len(feature) == 3
+                else """",
                 class_name=""text-sm font-medium text-slate-11 flex items-center gap-3 mb-2"",
             )
             for feature in features
@@ -244,8 +254,9 @@ def card(
     return rx.box(
         # Header
         rx.el.h3(title, class_name=""font-semibold text-slate-12 text-2xl mb-4""),
-        rx.el.p(description, class_name=""text-sm font-medium text-slate-9 mb-6 text-pretty""),
-        
+        rx.el.p(
+            description, class_name=""text-sm font-medium text-slate-9 mb-6 text-pretty""
+        ),
         # CTA Button
         rx.link(
             button(
@@ -258,24 +269,25 @@ def card(
             is_external=True,
             underline=""none"",
         ),
-        
         # Pricing Section
         rx.el.div(
-            rx.el.span(_get_price_label(title), class_name=""text-sm text-slate-9 block mb-1""),
+            rx.el.span(
+                _get_price_label(title), class_name=""text-sm text-slate-9 block mb-1""
+            ),
             _render_price_display(price, title),
             _render_messaging_section(title),
-            class_name=""mb-6""
+            class_name=""mb-6"",
         ),
-        
         # Divider
         rx.el.hr(class_name=""border-slate-3 mb-6""),
-        
         # Features Section
         rx.el.div(
-            rx.el.p(_get_features_header(title), class_name=""text-sm font-medium text-slate-9 mb-4""),
+            rx.el.p(
+                _get_features_header(title),
+                class_name=""text-sm font-medium text-slate-9 mb-4"",
+            ),
             _render_feature_list(features),
         ),
-        
         class_name=""flex flex-col p-6 border border-slate-4 rounded-lg shadow-small bg-slate-2 w-full min-w-0 max-w-md w-[28rem] overflow-hidden h-[42rem]"",
     )
 
@@ -294,16 +306,16 @@ def popular_card(
             ""1 Month Free Trial"",
             class_name=""absolute top-[-0.75rem] left-8 rounded-md bg-[--violet-9] h-[1.5rem] text-sm font-medium text-center px-2 flex items-center justify-center text-[#FCFCFD] z-[10]"",
         ),
-        
         # Card Content with Background Effects
         rx.box(
             glow(),
             grid(),
-            
             # Header
             rx.el.h3(title, class_name=""font-semibold text-slate-12 text-2xl mb-4""),
-            rx.el.p(description, class_name=""text-sm font-medium text-slate-9 mb-6 text-pretty""),
-            
+            rx.el.p(
+                description,
+                class_name=""text-sm font-medium text-slate-9 mb-6 text-pretty"",
+            ),
             # CTA Button
             rx.link(
                 button(
@@ -316,27 +328,25 @@ def popular_card(
                 is_external=True,
                 underline=""none"",
             ),
-            
             # Pricing Section
             rx.el.div(
                 rx.el.span(""From"", class_name=""text-sm text-slate-9 block mb-1""),
                 _render_price_display(price, title),
                 _render_messaging_section(title),
-                class_name=""mb-6""
+                class_name=""mb-6"",
             ),
-            
             # Divider
             rx.el.hr(class_name=""border-slate-3 mb-6""),
-            
             # Features Section
             rx.el.div(
-                rx.el.p(""Everything in the Pro Plan, plus:"", class_name=""text-sm font-medium text-slate-9 mb-4""),
+                rx.el.p(
+                    ""Everything in the Pro Plan, plus:"",
+                    class_name=""text-sm font-medium text-slate-9 mb-4"",
+                ),
                 _render_feature_list(features),
             ),
-            
             class_name=""flex flex-col p-6 border-2 border-[--violet-9] rounded-lg w-full min-w-0 max-w-md w-[28rem] relative z-[1] backdrop-blur-[6px] bg-[rgba(249,_249,_251,_0.48)] dark:bg-[rgba(26,_27,_29,_0.48)] shadow-[0px_2px_5px_0px_rgba(28_32_36_0.03)] overflow-hidden h-[42rem]"",
         ),
-        
         class_name=""relative w-full min-w-0 max-w-md w-[28rem]"",
     )
 
@@ -353,7 +363,15 @@ def plan_cards() -> rx.Component:
                     ""Free users are limited to 20 hours of 1 vCPU, 1 GB RAM  machines per month."",
                 ),
                 (""heart-handshake"", ""Discord/Github Support""),
-                (""building"", rx.link(""Reflex Enterprise"", href=""https://reflex.dev/docs/enterprise/overview/"", class_name=""!text-slate-11""), ""Free-tier users can access Reflex Enterprise features, with a required 'Built with Reflex' badge displayed on their apps.""),
+                (
+                    ""building"",
+                    rx.link(
+                        ""Reflex Enterprise"",
+                        href=""https://reflex.dev/docs/enterprise/overview/"",
+                        class_name=""!text-slate-11"",
+                    ),
+                    ""Free-tier users can access Reflex Enterprise features, with a required 'Built with Reflex' badge displayed on their apps."",
+                ),
                 (""frame"", ""Open Source Framework""),
             ],
             ""Start for Free"",
@@ -365,7 +383,11 @@ def plan_cards() -> rx.Component:
             ""Get a plan tailored to your business needs."",
             [
                 (""credit-card"", ""Cloud Compute $100/mo included""),
-                (""hard-drive"", ""On Premise Deployment"", ""Option to self-host your apps on your own infrastructure.""),
+                (
+                    ""hard-drive"",
+                    ""On Premise Deployment"",
+                    ""Option to self-host your apps on your own infrastructure."",
+                ),
                 (""hand-helping"", ""White Glove Onboarding""),
                 (""user-round-plus"", ""Personalized integration help""),
                 (""key"", ""Bring your own AI API keys""),
@@ -376,5 +398,5 @@ def plan_cards() -> rx.Component:
             ""Contact Us"",
             price=""Custom"",
         ),
-        class_name=""flex flex-row flex-wrap justify-center items-center gap-6 w-full""
+        class_name=""flex flex-row flex-wrap justify-center items-center gap-6 w-full"",
     )