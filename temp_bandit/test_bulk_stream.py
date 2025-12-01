@@ -38,7 +38,7 @@
 _JOB_START_DATE = datetime.fromisoformat(""2024-05-05T00:00:00+00:00"")
 _JOB_END_DATE = _JOB_START_DATE + timedelta(hours=2, minutes=24)
 
-_URL_GRAPHQL = f""https://{_SHOP_NAME}.myshopify.com/admin/api/2024-04/graphql.json""
+_URL_GRAPHQL = f""https://{_SHOP_NAME}.myshopify.com/admin/api/2025-01/graphql.json""
 _JOB_RESULT_URL = ""https://storage.googleapis.com/shopify-tiers-assets-prod-us-east1/bulk-operation-outputs/l6lersgk4i81iqc3n6iisywwtipb-final?GoogleAccessId=assets-us-prod%40shopify-tiers.iam.gserviceaccount.com&Expires=1715633149&Signature=oMjQelfAzUW%2FdulC3HbuBapbUriUJ%2Bc9%2FKpIIf954VTxBqKChJAdoTmWT9ymh%2FnCiHdM%2BeM%2FADz5siAC%2BXtHBWkJfvs%2F0cYpse0ueiQsw6R8gW5JpeSbizyGWcBBWkv5j8GncAnZOUVYDxRIgfxcPb8BlFxBfC3wsx%2F00v9D6EHbPpkIMTbCOAhheJdw9GmVa%2BOMqHGHlmiADM34RDeBPrvSo65f%2FakpV2LBQTEV%2BhDt0ndaREQ0MrpNwhKnc3vZPzA%2BliOGM0wyiYr9qVwByynHq8c%2FaJPPgI5eGEfQcyepgWZTRW5S0DbmBIFxZJLN6Nq6bJ2bIZWrVriUhNGx2g%3D%3D&response-content-disposition=attachment%3B+filename%3D%22bulk-4476008693949.jsonl%22%3B+filename%2A%3DUTF-8%27%27bulk-4476008693949.jsonl&response-content-type=application%2Fjsonl""
 
 _INCREMENTAL_JOB_START_DATE_ISO = ""2024-05-05T00:00:00+00:00""