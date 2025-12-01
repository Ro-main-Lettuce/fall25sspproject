@@ -2747,7 +2747,7 @@ def record_process_components(self, record: MutableMapping[str, Any]) -> Iterabl
         record[""inventory_item_id""] = self._unnest_and_resolve_id(record, ""inventoryItem"", ""inventory_item_id"")
         inventory_item = record.get(""inventoryItem"")
         measurement_weight = record.get(""inventoryItem"", {}).get(""measurement"", {}).get(""weight"")
-        record[""weight""] = measurement_weight.get(""value"") if measurement_weight.get(""value"") else 0.0
+        record[""weight""] = measurement_weight.get(""value"", 0.0) if measurement_weight is not None else 0.0
         record[""weight_unit""] = measurement_weight.get(""unit"") if measurement_weight else None
         record[""tracked""] = inventory_item.get(""tracked"") if inventory_item else None
         record[""requires_shipping""] = inventory_item.get(""requires_shipping"") if inventory_item else None