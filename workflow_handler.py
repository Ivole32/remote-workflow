import os
import yaml
from logger import Logger
from config import Configuration
from SSH_handler import SSH_Handler

class workflow_handler:
    def __init__(self) -> None:
        self.logger = Logger()
        self.config = Configuration()
        self.ssh_handler = SSH_Handler()

        self.workflow_folder = self.config.get_config_value(value="workflow-folder", topic="config", return_type=str)[1]
        self.workflows = []

        self.__load_worklows()

        print(str(self.workflows))
    
    def __load_worklows(self) -> None:
        """A function to load workflows from the workflow folder and storem them in a usefull format"""
        self.files = [f for f in os.listdir(self.workflow_folder) if os.path.isfile(os.path.join(self.workflow_folder, f))]

        for file in self.files:
            if file.endswith(".yaml"):
                with open(os.path.join(self.workflow_folder, file), "r") as f:
                    workflow = yaml.safe_load(f)
                    workflow = [
                        [
                            workflow["name"],
                            file
                        ],
                        workflow
                    ]
                self.workflows.append(workflow)

    def run_workflow(self, workflow_specs: list | str) -> None:
        """
        A function to run a workflow
        
        Arguments:
            workflow_specs: str or list
                If str, it can be the name of the workflow or the filename of the workflow.
                If list, it should be a list with two elements: [name, filepath] (recommended).
        """

        if isinstance(workflow_specs, str):
            for workflow in self.workflows:
                if workflow[0][0] == workflow_specs or workflow[0][1] == workflow_specs:
                    self.workflow = workflow[1]
                    break

        elif isinstance(workflow_specs, list):
            for workflow in self.workflows:
                if workflow[0] == workflow_specs:
                    self.workflow = workflow[1]
                    break

        for key, _ in self.workflow.items():
            if key == "run":
                for command in self.workflow["run"]:
                    self.ssh_handler.send_ssh_command(command)

            elif key == "upload-files":
                for file in self.workflow["upload-files"]:
                    self.ssh_handler.upload_file_to_remote(file, file)

            elif key == "download-files":
                for file in self.workflow["download-files"]:
                    self.ssh_handler.download_file_from_remote(file, ".")

    def create_workflow(self) -> None:
        """
        A function to create workflows
        """
        pass

if __name__ == "__main__":
    handler = workflow_handler()
    handler.run_workflow(["update", "update.yaml"])