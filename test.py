import paramiko
from logger import Logger

logger = Logger()

def test_ssh_key_connection(host, user, private_key_path):
    try:
        key = paramiko.RSAKey.from_private_key_file(private_key_path)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Trying to connect to {user}@{host} using key: {private_key_path}")
        
        ssh.connect(hostname=host, username=user, pkey=key, timeout=5)
        
        stdin, stdout, stderr = ssh.exec_command("echo connected")
        output = stdout.read().decode().strip()
        
        if output == "connected":
            logger.ok("SSH key authentication successful.")
        else:
            logger.warn("SSH connected, but command failed.")

        ssh.close()
    except Exception as e:
        logger.error(f"SSH key authentication failed:\n{e}")

if __name__ == "__main__":
    test_ssh_key_connection(
        host="192.168.112.102",
        user="ivo",
        private_key_path=r".\.ssh\id_rsa"
    )