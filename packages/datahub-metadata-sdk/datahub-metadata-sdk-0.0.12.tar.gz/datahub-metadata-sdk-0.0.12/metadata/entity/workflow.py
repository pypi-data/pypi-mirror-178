# -*- coding: utf-8 -*-

from typing import Optional
from dataclasses import dataclass, field

from datahub.api.entities.datajob import DataFlow


@dataclass
class Workflow:
    def __init__(self, cluster: str, orchestrator: str, id: str) -> None:
        self.jobFlow = DataFlow(
            cluster=cluster, orchestrator=orchestrator, id=id)

    def __getattr__(self, key):
        if key == 'jobFlowRun':
            raise ValueError('usage start dataflow first')
        return super().__getattr__()
