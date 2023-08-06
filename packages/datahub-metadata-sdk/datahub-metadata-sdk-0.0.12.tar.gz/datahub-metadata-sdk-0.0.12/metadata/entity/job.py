# -*- coding: utf-8 -*-

from typing import List
from dataclasses import dataclass, field

from metadata.entity.dataset import Dataset
from datahub.api.entities.datajob import DataJob
from metadata.entity.workflow import Workflow


@dataclass
class Job:

    def __init__(self, dataflow: Workflow, id: str, name: str, properties: dict[str, str] = None, inlets: List[Dataset] = None, tags: List[str] = None, owners: List[str] = None, outlets: List[Dataset] = None):
        self.datajob = DataJob(flow_urn=dataflow.jobFlow.urn, id=id, name=name)
        dataset_urn_list = []
        if inlets is not None:
            for dataset in inlets:
                dataset_urn_list.append(dataset.urn)
            self.datajob.inlets = dataset_urn_list
        if outlets is not None:
            dataset_urn_list = []
            for outlet in outlets:
                dataset_urn_list.append(outlet.urn)
            self.datajob.outlets = dataset_urn_list
        if properties is not None:
            self.datajob.properties = properties
        if tags is not None:
            for tag in tags:
                self.datajob.tags.add(tag)
        if owners is not None:
            for owner in owners:
                self.datajob.owners.add(owner)

    def __getattr__(self, key):
        if key == 'jobRun':
            raise ValueError('usage start datajob first')
        return super().__getattr__()

    def set_upstream_job(self, job):
        if isinstance(job, Job):
            self.datajob.upstream_urns.append(job.datajob.urn)
        elif type(job) == list and isinstance(job[0], Job):
            for i in job:
                self.datajob.upstream_urns.append(i.urn)
        elif type(job) == list and type(job[0]) == str:
            for i in job:
                self.datajob.upstream_urns.append(i)
        else:
            raise ValueError('unexpected type %s' % type(job))
