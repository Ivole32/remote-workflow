import subprocess
import os
from logger import Logger
from config import Configuration

logger = Logger()
config = Configuration()

class SSH_Handler():
    def __init__(self) -> None:
        self.ssh_dir = config.get_config_value(value="ssh-file", return_type=str)[1]
        self.ssh_key_name = config.get_config_value(value="ssh-key-name", return_type=str)[1]
        self.ssh_port = config.get_config_value(value="ssh-port", return_type=int)[1]
        self.ssh_ip = config.get_config_value(value="ssh-ip", return_type=str)[1]
        self.ssh_user = config.get_config_value(value="ssh-user", return_type=str)[1]
        self.pub_key_file = os.path.join(self.ssh_dir, f"{self.ssh_key_name}.pub")

    def generate_SSH_Key(self) -> None:
        logger.info("Generating SSH key pair...")
        if not os.path.exists(self.ssh_dir):
            logger.info("'.ssh' directory not found. Creating it now...")
            os.makedirs(self.ssh_dir)
        logger.info("Creating SSH key pair...")
        key_path = os.path.join(self.ssh_dir, self.ssh_key_name)
        os.system(rf'ssh-keygen -t rsa -b 4096 -f "{key_path}" -N ""')
        logger.ok("SSH key pair created successfully.")

    def copy_SSH_key(self) -> None:
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
        ssh_file = os.path.join(self.ssh_dir, self.ssh_key_name)

        if os.name != 'nt':
            return

        username = os.getlogin()
        logger.info(f"Fixing windows key permissions: {ssh_file} (User: {username})")

        subprocess.run(["icacls", ssh_file, "/inheritance:r"], check=True)
        subprocess.run(["icacls", ssh_file, "/grant:r", f"{username}:(R)"], check=True)

    def test_SSH_without_password(self) -> bool:
        ssh_file = os.path.join(self.ssh_dir, self.ssh_key_name)
        self.fix_windows_key_permissions()
        try:
            result = subprocess.run(
                ["ssh", "-i", ssh_file, "-o", "BatchMode=yes", f"{self.ssh_user}@{self.ssh_ip}", "echo ok"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )

            logger.info(f"SSH test returncode: {result.returncode}, stdout: {result.stdout.strip()}")
            return result.returncode == 0 and "ok" in result.stdout.strip()

        except subprocess.TimeoutExpired:
            logger.error("SSH connection timed out.")
            return False
        except Exception as e:
            logger.error(f"Error testing SSH connection: {e}")
            return False

if __name__ == "__main__":
    handler = SSH_Handler()
    handler.generate_SSH_Key()
    while True:
        if handler.test_SSH_without_password():
            print("OK")
            break
        else:
            handler.copy_SSH_key()