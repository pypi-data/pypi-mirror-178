"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
from copy import deepcopy
import json

# DIRAC imports
import DIRAC
from CTADIRAC.Interfaces.API.Prod5CtaPipeModelingJob import Prod5CtaPipeModelingJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class CtapipeModelingElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = Prod5CtaPipeModelingJob(cpuTime=259200.0)
        self.job.setOutputSandbox(["*Log.txt"])
        self.job.input_limit = None
        self.prod_step.Type = "DataReprocessing"
        self.prod_step.Name = "Modeling_ctapipe"
        self.mandatory_keys = {"MCCampaign", "configuration_id", "version"}
        self.constrained_keys = {"catalogs", "nsb", "group_size"}
        self.file_meta_fields = {"nsb", "split"}

    def set_constrained_job_attribute(self, key, value):
        """Set job attribute with constraints"""
        if key == "catalogs":
            # remove whitespaces between catalogs if there are some and separate between commas
            setattr(self.job, key, json.dumps(value.replace(", ", ",").split(sep=",")))
        elif key == "group_size":
            setattr(self.job, key, value)
            self.prod_step.GroupSize = self.job.group_size
        elif key == "nsb":
            try:
                self.job.output_file_metadata[key] = value['=']
            except BaseException:
                self.job.output_file_metadata[key] = value

    def build_job_output_data(self, workflow_step):
        """Build job output meta data"""
        metadata = deepcopy(self.prod_step.Inputquery)
        for key, value in workflow_step["job_config"].items():
            metadata[key] = value
        self.job.set_output_metadata(metadata)

    #############################################################################
