@@ -281,11 +281,11 @@ async def test_run_connector_publish_pipeline_when_image_does_not_exist(mocker):
     """"""We check that the pipeline fails early when the connector image does not exist.""""""
     for module, to_mock in STEPS_TO_PATCH:
         mocker.patch.object(module, to_mock, return_value=mocker.AsyncMock())
-    
+
     publish_pipeline.MetadataValidation.return_value.run.return_value = mocker.Mock(
         name=""metadata_validation_result"", status=StepStatus.SUCCESS
     )
-    
+
     publish_pipeline.CheckConnectorImageDoesNotExist.return_value.run.return_value = mocker.Mock(
         name=""check_connector_image_does_not_exist_result"", status=StepStatus.FAILURE
     )
@@ -296,11 +296,11 @@ async def test_run_connector_publish_pipeline_when_image_does_not_exist(mocker):
 
     publish_pipeline.MetadataValidation.return_value.run.assert_called_once()
     publish_pipeline.CheckConnectorImageDoesNotExist.return_value.run.assert_called_once()
-    
+
     for module, to_mock in STEPS_TO_PATCH:
         if to_mock not in [""MetadataValidation"", ""CheckConnectorImageDoesNotExist""]:
             getattr(module, to_mock).return_value.run.assert_not_called()
-    
+
     assert (
         report.steps_results
         == context.report.steps_results
@@ -314,9 +314,9 @@ async def test_run_connector_publish_pipeline_when_image_does_not_exist(mocker):
 @pytest.mark.parametrize(
     ""pypi_enabled, pypi_package_does_not_exist_status, publish_step_status, expect_publish_to_pypi_called, expect_build_connector_called,api_token"",
     [
-        pytest.param(True, StepStatus.SUCCESS, StepStatus.SUCCESS, True, True, ""test"", id=""happy_path""),
-        pytest.param(False, StepStatus.SUCCESS, StepStatus.SUCCESS, False, True, ""test"", id=""pypi_disabled, skip all pypi steps""),
-        pytest.param(True, StepStatus.SKIPPED, StepStatus.SUCCESS, False, True, ""test"", id=""pypi_package_exists, skip publish_to_pypi""),
+        pytest.param(True, StepStatus.SUCCESS, StepStatus.SUCCESS, True, False, ""test"", id=""happy_path""),
+        pytest.param(False, StepStatus.SUCCESS, StepStatus.SUCCESS, False, False, ""test"", id=""pypi_disabled, skip all pypi steps""),
+        pytest.param(True, StepStatus.SKIPPED, StepStatus.SUCCESS, False, False, ""test"", id=""pypi_package_exists, skip publish_to_pypi""),
         pytest.param(True, StepStatus.SUCCESS, StepStatus.FAILURE, True, False, ""test"", id=""publish_step_fails, abort""),
         pytest.param(True, StepStatus.FAILURE, StepStatus.FAILURE, False, False, ""test"", id=""pypi_package_does_not_exist_fails, abort""),
         pytest.param(True, StepStatus.SUCCESS, StepStatus.SUCCESS, False, False, None, id=""no_api_token, abort""),