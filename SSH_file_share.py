from logger import Logger
import subprocess
import os

logger = Logger()

def generate_SSH_Key(ssh_dir=r".\.ssh") -> None:
    logger.info("Generating SSH key pair...")
    if not os.path.exists(ssh_dir):
        logger.info("'.ssh' directory not found. Creating it now...")
        os.makedirs(ssh_dir)
    logger.info("Creating SSH key pair...")
    os.system(rf'ssh-keygen -t rsa -b 4096 -f {ssh_dir}\id_rsa -N ""')
    logger.ok("SSH key pair created successfully.")

def copy_SSH_key(pub_key_file=r".\.ssh\id_rsa.pub", username="ivo", ip="192.168.112.104") -> None:
    with open(pub_key_file, "r") as f:
        public_key = f.read()

    command = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

    proc = subprocess.Popen(
        ["ssh", f"{username}@{ip}", command],
        stdin=subprocess.PIPE,
        text=True
    )

    proc.communicate(public_key)

def fix_windows_key_permissions(ssh_file=r".\.ssh\id_rsa") -> None:
    """
    A function to fix the perminissions for the id_rsa file
    """
    if os.name != 'nt':
        return

    username = os.getlogin()
    logger.info(f"Fixing windows key perminissions: {ssh_file} (User: {username})")

    subprocess.run(["icacls", ssh_file, "/inheritance:r"], check=True)
    subprocess.run(["icacls", ssh_file, "/grant:r", f"{username}:(R)"], check=True)

def test_SSH_without_password(ssh_file=r".\.ssh\id_rsa", username="ivo", ip="192.168.112.104") -> bool:
    fix_windows_key_permissions()
    try:
        result = subprocess.run(
            ["ssh", "-i", f"{ssh_file}", "-o", "BatchMode=yes", f"{username}@{ip}", "echo ok"],
            timeout=30
        )

        print(f"{result.returncode}\n{result.stdout}")
        if result.returncode == 0 and "ok" in result.stdout:
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        print("SSH connection timed out.")
        return False
    except Exception as e:
        print(f"Error testing SSH connection: {e}")
        return False
    
if __name__ == "__main__":
    generate_SSH_Key()
    while True:
        if test_SSH_without_password():
            print("OK")
            break
        else:
            copy_SSH_key()