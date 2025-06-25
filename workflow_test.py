import yaml
from SSH_handler import SSH_Handler

ssh_handler = SSH_Handler()

with open ("workflow.yaml", "r") as f:
    workflow = yaml.safe_load(f)

print(workflow["name"])

upload_files = workflow["upload-files"]
for file in upload_files:
    ssh_handler.upload_file_to_remote(file, file)

run = workflow["run"]

for command in run:
    ssh_handler.send_ssh_command(command)

download_files = workflow["download-files"]

for file in download_files:
    ssh_handler.download_file_from_remote(file, ".")