@@ -5,23 +5,25 @@
 
 class CrewTrainingHandler(PickleHandler):
     def save_trained_data(self, agent_id: str, trained_data: dict) -> None:
-        """"""
-        Save the trained data for a specific agent.
+        """"""Save the trained data for a specific agent.
 
-        Parameters:
+        Parameters
+        ----------
         - agent_id (str): The ID of the agent.
         - trained_data (dict): The trained data to be saved.
+
         """"""
         data = self.load()
         data[agent_id] = trained_data
         self.save(data)
 
     def append(self, train_iteration: int, agent_id: str, new_data) -> None:
-        """"""
-        Append new data to the existing pickle file.
+        """"""Append new data to the existing pickle file.
 
-        Parameters:
+        Parameters
+        ----------
         - new_data (object): The new data to be appended.
+
         """"""
         data = self.load()
 