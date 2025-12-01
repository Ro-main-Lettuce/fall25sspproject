@@ -175,3 +175,78 @@ def test_format_string(client, model: str, mode: instructor.Mode, is_list: bool)
     assert isinstance(resp, User)
     assert resp.name == ""Jason""
     assert resp.age == 25
+
+
+@pytest.mark.parametrize(""model"", models)
+@pytest.mark.parametrize(""mode"", modes)
+def test_system_message_templating(client, model, mode):
+    client = instructor.from_genai(client, mode=mode)
+    response = client.chat.completions.create(
+        model=model,
+        messages=[
+            {
+                ""role"": ""system"",
+                ""content"": ""{{name}} is {{age}} years old"",
+            },
+            {
+                ""role"": ""user"",
+                ""content"": ""Make sure that the response is a list of users"",
+            },
+        ],
+        response_model=Users,
+        context={""name"": ""Jason"", ""age"": 25},
+    )
+    assert isinstance(response, Users)
+    assert len(response.users) > 0
+    assert response.users[0].name == ""Jason""
+    assert response.users[0].age == 25
+
+
+@pytest.mark.parametrize(""model"", models)
+@pytest.mark.parametrize(""mode"", modes)
+def test_system_kwarg_templating(client, model, mode):
+    client = instructor.from_genai(client, mode=mode)
+    response = client.chat.completions.create(
+        model=model,
+        system=""{{name}} is {{age}} years old"",
+        messages=[
+            {
+                ""role"": ""user"",
+                ""content"": ""Make sure that the response is a list of users"",
+            },
+        ],
+        response_model=Users,
+        context={""name"": ""Jason"", ""age"": 25},
+    )
+    assert isinstance(response, Users)
+    assert len(response.users) > 0
+    assert response.users[0].name == ""Jason""
+    assert response.users[0].age == 25
+
+
+@pytest.mark.parametrize(""model"", models)
+@pytest.mark.parametrize(""mode"", modes)
+def test_system_message_list_templating(client, model, mode):
+    client = instructor.from_genai(client, mode=mode)
+    response = client.chat.completions.create(
+        model=model,
+        messages=[
+            {
+                ""role"": ""system"",
+                ""content"": [
+                    ""{{name}} is"",
+                    "" {{age}} years old"",
+                ],
+            },
+            {
+                ""role"": ""user"",
+                ""content"": ""Make sure that the response is a list of users"",
+            },
+        ],
+        response_model=Users,
+        context={""name"": ""Jason"", ""age"": 25},
+    )
+    assert isinstance(response, Users)
+    assert len(response.users) > 0
+    assert response.users[0].name == ""Jason""
+    assert response.users[0].age == 25