from logger import Logger
from config import Configuration
import yaml
from SSH_handler import SSH_Handler

class workflow_handler:
    def __init__(self) -> None:
        self.logger = Logger()
        self.config = Configuration()
        self.ssh_handler = SSH_Handler()

        with open ("workflow.yaml", "r") as f:
            self.workflow = yaml.safe_load(f)

            for key, value in self.workflow.items():
                print(str(key) + str(value))
    
    def run_workflow(self) -> None:
        """A function to run a workflow"""
        print(self.workflow["name"])

        for key, _ in self.workflow.items():
            if key == "run":
                for command in self.workflow["run"]:
                    self.ssh_handler.send_ssh_command(command)

            elif key == "upload-files":
                for file in self.workflow["upload-files"]:
                    self.ssh_handler.upload_file_to_remote(file, file)

            elif key == "download-files":
                for file in self.workflow["download-files"]:
                    self.ssh_handler.download_file_from_remote(file, file)

    def create_workflow(self) -> None:
        """
        A function to create workflows
        """
        pass

if __name__ == "__main__":
    handler = workflow_handler()