@@ -49,7 +49,7 @@ def name_from_metadata(player_meta: dict, raw: Optional[str] = None) -> str:
 # TODO: we could scrape code -> ELO from the slippi website?
 
 # TODO: put this in a json?
-name_groups = [
+NAME_GROUPS = [
   ('Mang0', 'mang', 'mang0', 'MANG#0'),
   ('Zain', 'zain', 'DontTestMe', 'ZAIN#0', 'DTM#664'),
   ('Cody', 'iBDW', 'cody', 'IBDW#0', 'IBDW#734', 'JBDW#120'),
@@ -86,15 +86,15 @@ def name_from_metadata(player_meta: dict, raw: Optional[str] = None) -> str:
   ('Zamu', 'A#9'),
 ]
 
-name_map = {}
-for first, *rest in name_groups:
+NAME_MAP: dict[str, str] = {}
+for first, *rest in NAME_GROUPS:
   for name in rest:
-    name_map[name] = first
+    NAME_MAP[name] = first
 
 def normalize_name(name):
-  return name_map.get(name, name)
+  return NAME_MAP.get(name, name)
 
-KNOWN_PLAYERS = {group[0] for group in name_groups}
+KNOWN_PLAYERS = {group[0] for group in NAME_GROUPS}
 
 def is_known_player(name):
   return normalize_name(name) in KNOWN_PLAYERS
@@ -126,4 +126,4 @@ def is_banned_name(name: str) -> bool:
   return normalize_name(name) in BANNED_NAMES
 
 for name, _ in PLAYER_MAINS:
-  assert name in name_map.values(), name
+  assert name in KNOWN_PLAYERS, name