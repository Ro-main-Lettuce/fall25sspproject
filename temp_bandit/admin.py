@@ -131,7 +131,7 @@ class OrganisationAdmin(admin.ModelAdmin[Organisation]):
     def get_queryset(
         self, request: HttpRequest
     ) -> QuerySet[Organisation]:  # pragma: no cover
-        return (
+        queryset: QuerySet[Organisation] = (
             Organisation.objects.select_related(""subscription"")
             .annotate(
                 num_users=Count(
@@ -145,6 +145,7 @@ def get_queryset(
             )
             .all()
         )
+        return queryset
 
     def num_users(self, instance: OrganisationWithAnnotations) -> int:
         return instance.num_users