@@ -113,10 +113,11 @@ def check_button_dto(button_dto: ButtonDto):
 def html_2_markdown(content):
     def video_repl(match):
         url = match.group(""url"")
+        title = match.group(""title"")
         bvid_match = re.search(r""BV\w+"", url)
         if bvid_match:
             bvid = bvid_match.group(0)
-            return f'<iframe src=""https://player.bilibili.com/player.html?isOutside=true&bvid={bvid}&p=1&high_quality=1"" scrolling=""no"" border=""0"" frameborder=""no"" framespacing=""0"" allowfullscreen=""true""></iframe>'  # noqa: E501 E261
+            return f'<iframe src=""https://player.bilibili.com/player.html?isOutside=true&bvid={bvid}&p=1&high_quality=1"" title=""{title}"" scrolling=""no"" border=""0"" frameborder=""no"" framespacing=""0"" allowfullscreen=""true""></iframe>'  # noqa: E501 E261
         return url
 
     def profile_repl(match):
@@ -154,7 +155,8 @@ def markdown_2_html(content):
 
     def iframe_repl(match):
         bvid = match.group(""bvid"")
-        return f'<span data-tag=""video"" data-url=""https://www.bilibili.com/video/{bvid}/"" data-title=""视频占位"">视频占位</span>'
+        title = match.group(""title"")
+        return f'<span data-tag=""video"" data-url=""https://www.bilibili.com/video/{bvid}/"" data-title=""{title}"">{title}</span>'
 
     def profile_repl(match):
         var = match.group(""var"")
@@ -167,7 +169,7 @@ def image_repl(match):
         return f'<span data-tag=""image"" data-url=""{url}"" data-title=""{title}"" data-scale=""{scale}"">{title}</span>'
 
     content = re.sub(
-        r'(?s)<iframe[^>]*src=""[^""]*bvid=(?P<bvid>BV\w+)[^""]*""[^>]*></iframe>',
+        r'(?s)<iframe[^>]*src=""[^""]*bvid=(?P<bvid>BV\w+)[^""]*""[^>]*title=""(?P<title>[^""]*)""[^>]*></iframe>',
         iframe_repl,
         content,
     )