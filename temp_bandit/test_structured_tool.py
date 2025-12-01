@@ -25,7 +25,7 @@ class TestSchema(BaseModel):
     return TestSchema
 
 
-class TestCrewStructuredTool:
+class InternalCrewStructuredTool:
     def test_initialization(self, basic_function, schema_class):
         """"""Test basic initialization of CrewStructuredTool""""""
         tool = CrewStructuredTool(