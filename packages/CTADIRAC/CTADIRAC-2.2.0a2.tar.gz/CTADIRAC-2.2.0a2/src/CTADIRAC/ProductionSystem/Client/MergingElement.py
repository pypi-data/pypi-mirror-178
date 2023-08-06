"""
   Wrapper around the job class to build a workflow element (production step + job)
"""

__RCSID__ = "$Id$"

# generic imports
from copy import deepcopy
import json

# DIRAC imports
import DIRAC
from CTADIRAC.Interfaces.API.Prod5CtaPipeMergeJob import Prod5CtaPipeMergeJob
from CTADIRAC.ProductionSystem.Client.WorkflowElement import WorkflowElement


class MergingElement(WorkflowElement):
    """Composite class for workflow element (production step + job)"""

    #############################################################################

    def __init__(self, parent_prod_step):
        """Constructor"""
        WorkflowElement.__init__(self, parent_prod_step)
        self.job = Prod5CtaPipeMergeJob(cpuTime=259200.0)
        self.job.setOutputSandbox(["*Log.txt"])
        self.job.input_limit = None
        self.job.merged = 0
        self.prod_step.Type = "DataReprocessing"
        self.prod_step.Name = "Merge"
        self.mandatory_keys = {"MCCampaign", "configuration_id", "version"}
        self.constrained_keys = {"catalogs", "group_size", "nsb"}
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
        merged = self.get_merging_level()
        metadata["merged"] = merged
        self.job.set_output_metadata(metadata)

    def get_merging_level(self):
        """Get the merging level from parent step or from the user query"""
        if self.prod_step.ParentStep:
            merged = self.prod_step.ParentStep.Outputquery["merged"]
        else:
            merged = self.job.merged
        return merged

    def build_element_config(self):
        """Set job and production step attributes specific to the configuration"""
        self.prod_step.GroupSize = self.job.group_size
        self.job.set_executable_sequence(debug=False)
        self.prod_step.Body = self.job.workflow.toXML()

    #############################################################################
