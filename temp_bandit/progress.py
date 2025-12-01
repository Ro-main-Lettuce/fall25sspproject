@@ -55,10 +55,6 @@ def update(self, ratio: float) -> None:
         if not self.show_progress:
             return
 
-        # マウスカーソルが四桁の数値になり、0から9999までの値が表示できる領域がある
-        # しかし、進捗率をそのまま0から9999の数値に変換すると、下二桁の数値が頻繁に
-        # ラウンドトリップし進捗状況が分かりにくくなる。そのため、下二桁の表示領域
-        # だけを利用し0から99の数値で進捗率を表示する
         self.context.window_manager.progress_update(math.floor(ratio * 99))
 
 