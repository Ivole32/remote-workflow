import subprocess
import os
import shutil
from logger import Logger
from config import Configuration

logger = Logger()
config = Configuration()

class SSH_Handler():
    """
    The main class to work with SSH
    """
    def __init__(self) -> None:
        self.ssh_dir = config.get_config_value(value="ssh-file", return_type=str)[1]
        self.ssh_key_name = config.get_config_value(value="ssh-key-name", return_type=str)[1]
        self.ssh_port = config.get_config_value(value="ssh-port", return_type=int)[1]
        self.ssh_ip = config.get_config_value(value="ssh-ip", return_type=str)[1]
        self.ssh_user = config.get_config_value(value="ssh-user", return_type=str)[1]
        self.pub_key_file = os.path.join(self.ssh_dir, f"{self.ssh_key_name}.pub")

    def generate_SSH_Key(self, overwrite=False) -> None:
        """
        Generates a new SSH key paire

        Arguments:
            overwrite: bool (If the function should overwrite old SSH key paires)
        """
        if overwrite == True:
            logger.info("Deleting old SSH keys if there are some")
            shutil.rmtree(self.ssh_dir)
            logger.info("Generating new SSH key pair...")
            if not os.path.exists(self.ssh_dir):
                logger.info("'.ssh' directory not found. Creating it now...")
                os.makedirs(self.ssh_dir)
            logger.info("Creating SSH key pair...")
            key_path = os.path.join(self.ssh_dir, self.ssh_key_name)
            os.system(rf'ssh-keygen -t rsa -b 4096 -f "{key_path}" -N ""')
            logger.ok("SSH key pair created successfully.")
        if overwrite == False:
            if not os.path.exists(self.ssh_dir):
                logger.info("'.ssh' directory not found. Creating it now...")
                os.makedirs(self.ssh_dir)
            if not os.path.isfile(self.pub_key_file):
                logger.info("Generating SSH key pair...")
                key_path = os.path.join(self.ssh_dir, self.ssh_key_name)
                os.system(rf'ssh-keygen -t rsa -b 4096 -f "{key_path}" -N ""')
                logger.ok("SSH key pair created successfully.")
            else:
                logger.info("Key files are already there. Use 'overwrite=True' to overwrite them...")

    def copy_SSH_key(self) -> None:
        """
        Copies the SSH key to the remote linux server to gain acces without password
        """
        with open(self.pub_key_file, "r") as f:
            public_key = f.read()

        command = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

        proc = subprocess.Popen(
            ["ssh", f"{self.ssh_user}@{self.ssh_ip}", "-p", str(self.ssh_port), command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = proc.communicate(public_key)
        if proc.returncode != 0:
            logger.error(f"Error copying SSH key: {stderr}")
        else:
            logger.ok("SSH key copied successfully.")

    def fix_windows_key_permissions(self) -> None:
        """
        Fixes the perminissions for the key files so the ssh commadn can work with them
        """
        ssh_file = os.path.join(self.ssh_dir, self.ssh_key_name)

        if os.name != 'nt':
            return

        username = os.getlogin()
        logger.info(f"Fixing windows key permissions: {ssh_file} (User: {username})")

        try:
            subprocess.run(["icacls", ssh_file, "/inheritance:r"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["icacls", ssh_file, "/grant:r", f"{username}:(R)"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.error(f"Windows key perminissions could not be fixed: {e}")

    def send_ssh_command(self, command:list):
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

            logger.info(f"SSH command returncode: {result.returncode}, stdout: {result.stdout.strip()}")
            return result

        except subprocess.TimeoutExpired:
            logger.error("SSH connection timed out.")
            return False
        except Exception as e:
            logger.error(f"Error sending SSH command: {e}")
            return False

    def test_SSH_without_password(self) -> bool:
        """
        A function to test if the SSH connection without password works

        Returns:
            bool: If the connection worked without password
        """
        ssh_file = os.path.join(self.ssh_dir, self.ssh_key_name)
        self.fix_windows_key_permissions()

        command = ["ssh", "-i", ssh_file, "-o", "BatchMode=yes", f"{self.ssh_user}@{self.ssh_ip}", "echo ok"]

        self.result = self.send_ssh_command(command)
        return self.result.returncode == 0 and "ok" in self.result.stdout.strip()
        
if __name__ == "__main__":
    handler = SSH_Handler()
    handler.generate_SSH_Key(overwrite=False)
    while True:
        if handler.test_SSH_without_password():
            logger.ok("SSH connection OK")
            break
        else:
            handler.copy_SSH_key()