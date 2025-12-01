@@ -19,37 +19,43 @@ class RunState(Enum):
 
 
 class SceneWatcher(Protocol):
-    """"""シーンの変更を検知し、検知した際に何らかの処理を行うようにするプロトコル.""""""
+    """"""Protocol for detecting scene changes and performing some action when detected.""""""
 
     def run(self, context: Context) -> RunState:
-        """"""シーンの変更の検知と、検知した際に何らかの処理を行う.
+        """"""Detect scene changes and perform some action when detected.
 
-        シーンに検知したい変更が発生していない場合、このメソッドは100マイクロ秒未満で
-        returnする必要がある。時間が足りない場合、現在状態をインスタンス変数などに保存
-        して処理を中断する。
+        If no changes that need to be detected have occurred in the scene, this method
+        must return in less than 100 microseconds. If there is not enough time, save
+        the current state to instance variables and interrupt the process.
 
-        このメソッドはBlenderのフレームを跨いで複数回実行される。通常そのような処理は
-        ジェネレーターやasyncを使うことで効率的に実装できるが、このクラスではそうしない。
+        This method is executed multiple times across Blender frames. Usually such
+        processing can be efficiently implemented using generators or async, but this
+        class does not do so.
 
-        その理由は、Blenderのネイティブなオブジェクトへの参照をフレームをまたいで保持
-        できないが、ジェネレーターやasyncはそれを考慮してのプログラミングが難しいため。
+        The reason is that references to Blender's native objects cannot be held
+        across frames, but programming with generators and async is difficult when
+        considering this limitation.
 
-        :return 処理が完了した場合FINISH。完了しなかった場合はPREEMPT。
+        :return FINISH if processing is complete. PREEMPT if not complete.
         """"""
         raise NotImplementedError
 
     def create_fast_path_performance_test_objects(self, context: Context) -> None:
-        """"""run()が通常100マイクロ秒未満で完了するかのテストのためのオブジェクトを作成する.""""""
+        """"""Create objects for testing whether run() normally completes.
+
+        This tests whether the run() method normally completes in less than 100
+        microseconds.
+        """"""
         raise NotImplementedError
 
     def reset_run_progress(self) -> None:
-        """"""run()の中断状態をリセットする.""""""
+        """"""Reset the interrupted state of run().""""""
         raise NotImplementedError
 
 
 @dataclass
 class SceneWatcherSchedule:
-    """"""SceneWatcherと、その稼働状況を保持する.""""""
+    """"""Holds SceneWatcher and its operation status.""""""
 
     scene_watcher: SceneWatcher
     requires_run_once_more: bool = False
@@ -58,7 +64,11 @@ class SceneWatcherSchedule:
 
 @dataclass
 class SceneWatcherScheduler:
-    """"""UIをブロックしないように注意しながら、登録されたSceneWatcherを順番に定期的に実行する.""""""
+    """"""Periodically executes registered SceneWatchers in order.
+
+    This scheduler is careful not to block the UI while executing the
+    SceneWatcher instances.
+    """"""
 
     INTERVAL: Final[float] = 0.2
     scene_watcher_schedule_index: int = 0
@@ -74,24 +84,24 @@ def trigger(self, scene_watcher_type: type[SceneWatcher]) -> None:
             scene_watcher_type
         )
         if scene_watcher_schedule:
-            # 呼び出し頻度が高いファストパス。
-            # 最小限の処理でreturnできるようにしておく。
+            # High-frequency fast path.
+            # Allow returning with minimal processing.
 
             if scene_watcher_schedule.finished:
-                # タスクが終了済みの場合は再開
+                # If the task is finished, restart it
                 scene_watcher_schedule.finished = False
                 scene_watcher_schedule.scene_watcher.reset_run_progress()
             else:
-                # タスクが実行中の場合は、
-                # 「一度完了した後にもう一度実行」と設定
+                # If the task is running,
+                # set it to ""run once more after completion""
                 scene_watcher_schedule.requires_run_once_more = True
             return
 
-        # 呼び出し頻度が低いスローパス。
-        # 処理が重くなっても大丈夫。
+        # Low-frequency slow path.
+        # Heavy processing is okay.
 
-        # テスト対象から漏れないようにするため、
-        # 未登録のSceneWatcherをインスタンス化しようとしたらエラーにする。
+        # To prevent unregistered SceneWatchers from being missed in testing,
+        # throw an error if trying to instantiate an unregistered SceneWatcher.
         if scene_watcher_type not in self.get_all_scene_watcher_types():
             message = f""{scene_watcher_type} is not registered""
             raise NotImplementedError(message)
@@ -109,9 +119,9 @@ def get_all_scene_watcher_types() -> Sequence[type[SceneWatcher]]:
         return [OutlineUpdater, LookAtPreviewUpdater, MToon1AutoSetup]
 
     def process(self, context: Context) -> bool:
-        """"""SceneWatcherを一つ実行する.
+        """"""Execute one SceneWatcher.
 
-        GC Allocationを抑えるため、インデックス値を用いる
+        Use index values to reduce GC allocation.
         """"""
         if not self.scene_watcher_schedules:
             return False
@@ -120,14 +130,14 @@ def process(self, context: Context) -> bool:
             self.scene_watcher_schedule_index += 1
             self.scene_watcher_schedule_index %= len(self.scene_watcher_schedules)
 
-            # すでに完了しているタスクは飛ばす
+            # Skip tasks that are already completed
             scene_watcher_schedule = self.scene_watcher_schedules[
                 self.scene_watcher_schedule_index
             ]
             if scene_watcher_schedule.finished:
                 continue
 
-            # タスクを実行
+            # Execute the task
             run_state = scene_watcher_schedule.scene_watcher.run(context)
             if run_state == RunState.FINISH:
                 if scene_watcher_schedule.requires_run_once_more:
@@ -136,7 +146,7 @@ def process(self, context: Context) -> bool:
                 else:
                     scene_watcher_schedule.finished = True
 
-            # 一つでもタスクを実行したならreturn
+            # Return if at least one task was executed
             return True
         return False
 