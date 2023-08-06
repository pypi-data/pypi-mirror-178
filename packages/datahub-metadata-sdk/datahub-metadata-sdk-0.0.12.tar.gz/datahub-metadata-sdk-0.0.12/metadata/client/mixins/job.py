# -*- encoding: utf-8 -*-

from metadata.entity.job import Job
from datetime import datetime, timezone
from datahub.api.entities.dataprocess.dataprocess_instance import (
    DataProcessInstance,
    InstanceRunResult,
)
import uuid

class DataJobMixin:
    def create_datajob(self, datajob: Job):
        emitter = self.context.emitter
        datajob.datajob.emit(emitter)


    def start_datajob(self, datajob: Job):
        emitter = self.context.emitter
        datajob.jobRun = DataProcessInstance.from_datajob(
            datajob=datajob.datajob, id=f"{datajob.datajob.id}-{uuid.uuid4()}"
        )
        datajob.jobRun.emit_process_start(
            emitter,
            int(datetime.now(timezone.utc).timestamp() * 1000))


    def end_datajob(self, datajob: Job):
        emitter = self.context.emitter
        datajob.jobRun.emit_process_end(
            emitter,
            int(datetime.now(timezone.utc).timestamp() * 1000),
            result=InstanceRunResult.SUCCESS)
