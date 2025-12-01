@@ -558,8 +558,6 @@ async def run_connector_publish_pipeline(context: PublishConnectorContext, semap
             if check_connector_image_results.status is StepStatus.FAILURE:
                 return create_connector_report(results, context)
 
-
-
             # For pre-releases, we need to handle them separately
             if check_connector_image_results.status is StepStatus.SUCCESS and context.pre_release:
                 already_published_connector = context.dagger_client.container().from_(context.docker_image)