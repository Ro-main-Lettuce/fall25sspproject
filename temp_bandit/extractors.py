@@ -12,7 +12,10 @@
 from airbyte_cdk.sources.declarative.extractors.dpath_extractor import DpathExtractor
 from airbyte_cdk.sources.declarative.interpolation.interpolated_string import InterpolatedString
 from airbyte_cdk.sources.types import Config
-from source_google_sheets.utils import name_conversion, safe_name_conversion
+from source_google_sheets.utils import (
+    safe_name_conversion,
+    safe_sanitzation_conversion,
+)
 
 
 class RawSchemaParser:
@@ -67,11 +70,25 @@ def parse_raw_schema_values(
         duplicate_fields = set()
         parsed_schema_values = []
         seen_values = set()
+        # Gather all sanitisation flags from config
+        config = getattr(self, ""config"", {})
+        flags = {
+            ""remove_leading_trailing_underscores"": config.get(""remove_leading_trailing_underscores"", False),
+            ""combine_number_word_pairs"": config.get(""combine_number_word_pairs"", False),
+            ""remove_special_characters"": config.get(""remove_special_characters"", False),
+            ""combine_letter_number_pairs"": config.get(""combine_letter_number_pairs"", False),
+            ""allow_leading_numbers"": config.get(""allow_leading_numbers"", False),
+        }
+        use_sanitzation = any(flags.values())
+
         for property_index, raw_schema_property in enumerate(raw_schema_properties):
             raw_schema_property_value = self._extract_data(raw_schema_property, key_pointer)
             if not raw_schema_property_value or raw_schema_property_value.isspace():
                 break
-            if names_conversion:
+            # Use sanitzation if any flag is set, else legacy
+            if names_conversion and use_sanitzation:
+                raw_schema_property_value = safe_sanitzation_conversion(raw_schema_property_value, **flags)
+            elif names_conversion:
                 raw_schema_property_value = safe_name_conversion(raw_schema_property_value)
 
             if raw_schema_property_value in seen_values:
@@ -193,6 +210,7 @@ def extract_records(self, response: requests.Response) -> Iterable[MutableMappin
                     )
 
 
+@dataclass
 class DpathSchemaExtractor(DpathExtractor, RawSchemaParser):
     """"""
     Makes names conversion and parses sheet headers from the provided row.