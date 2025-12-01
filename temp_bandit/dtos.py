@@ -139,22 +139,22 @@ def __json__(self):
 class AICourseDTO:
     course_id: str
     course_name: str
-    teach_avator: str
+    teach_avatar: str
     course_price: Decimal
     lessons: list[AILessonAttendDTO]
 
     def __init__(
         self,
         course_id: str,
         course_name: str,
-        teach_avator: str,
+        teach_avatar: str,
         course_price: Decimal,
         lessons: List[AILessonAttendDTO],
         updated: bool = False,
     ) -> None:
         self.course_id = course_id
         self.course_name = course_name
-        self.teach_avator = teach_avator
+        self.teach_avatar = teach_avatar
         self.lessons = lessons
         self.course_price = course_price
         self.updated = updated
@@ -163,7 +163,7 @@ def __json__(self):
         return {
             ""course_id"": self.course_id,
             ""course_name"": self.course_name,
-            ""teach_avator"": self.teach_avator,
+            ""teach_avatar"": self.teach_avatar,
             ""lessons"": self.lessons,
             ""updated"": self.updated,
             ""course_price"": self.course_price,
@@ -245,22 +245,22 @@ class StudyRecordDTO:
     records: List[StudyRecordItemDTO]
     ui: ScriptDTO
     ask_mode: bool
-    teach_avator: str
+    teach_avatar: str
     ask_ui: ScriptDTO
 
-    def __init__(self, records, ui=None, ask_mode=True, teach_avator=None):
+    def __init__(self, records, ui=None, ask_mode=True, teach_avatar=None):
         self.records = records
         self.ui = ui
         self.ask_mode = ask_mode
-        self.teach_avator = teach_avator
+        self.teach_avatar = teach_avatar
         self.ask_ui = None
 
     def __json__(self):
         return {
             ""records"": self.records,
             ""ui"": self.ui,
             ""ask_mode"": self.ask_mode,
-            ""teach_avator"": self.teach_avator,
+            ""teach_avatar"": self.teach_avatar,
             ""ask_ui"": self.ask_ui,
         }
 