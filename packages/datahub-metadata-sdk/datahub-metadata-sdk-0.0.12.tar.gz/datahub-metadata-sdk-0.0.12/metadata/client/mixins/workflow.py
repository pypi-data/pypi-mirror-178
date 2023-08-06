# -*- encoding: utf-8 -*-

from metadata.entity.workflow import Workflow
from datetime import datetime, timezone
from datahub.metadata.schema_classes import ChangeTypeClass, DatasetProfileClass
from datahub.api.entities.dataprocess.dataprocess_instance import InstanceRunResult, DataProcessInstance
import uuid

class WorkflowMixin:
    def create_dataflow(self, _dataflow: Workflow):
        emitter = self.context.emitter
        _dataflow.jobFlow.emit(emitter)


    def start_dataflow(self, dataflow: Workflow):
        emitter = self.context.emitter
        dataflow.jobFlowRun = DataProcessInstance.from_dataflow(
            dataflow=dataflow.jobFlow, id=f"{dataflow.jobFlow.id}-{uuid.uuid4()}"
        )
        dataflow.jobFlowRun.emit_process_start(
            emitter,
            int(datetime.now(timezone.utc).timestamp() * 1000))
        
    def end_dataflow(self, dataflow: Workflow):
        emitter = self.context.emitter
        dataflow.jobFlowRun.emit_process_end(
            emitter,
            int(datetime.now(timezone.utc).timestamp() * 1000),
            result=InstanceRunResult.SUCCESS)
