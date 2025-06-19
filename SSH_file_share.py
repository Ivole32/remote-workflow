from logger import Logger
import os

logger = Logger()

def generate_SSH_Key(ssh_dir=r".\.ssh") -> None:
    logger.info("Generating SSH key pair...")
    if not os.path.exists(ssh_dir):
        logger.info("'.ssh' directory not found. Creating it now...")
        os.makedirs(ssh_dir)
    logger.info("Creating SSH key pair...")
    os.system(rf'ssh-keygen -t rsa -b 4096 -f {ssh_dir}\id_rsa -P "" -N ""')
    logger.ok("SSH key pair created successfully.")

if __name__ == "__main__":
    generate_SSH_Key()