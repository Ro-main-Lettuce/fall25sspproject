@@ -1,11 +1,11 @@
 from alembic.config import Config
 from alembic.script import ScriptDirectory
 
-config = Config('migrations/alembic.ini')
+config = Config(""migrations/alembic.ini"")
 script = ScriptDirectory.from_config(config)
 
-print('Current heads:', script.get_heads())
-print('
Migration branches:')
+print(""Current heads:"", script.get_heads())
+print(""
Migration branches:"")
 for head in script.get_heads():
     print(f""
Branch ending with {head}:"")
     revision = head