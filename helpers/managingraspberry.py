
# import librairies
import paramiko
from scp import SCPClient


class Raspberry():
    """This class manages the Raspberry

    Args :

    """

    def __init__(self, server, port, user, password):
        # Initialising ssh datas
        self.server = server
        self.port = port
        self.user = user
        self.password = password

        # Initializing connection
        self.client = paramiko.SSHClient()  # Create object of SSHClient and connecting to SSH
        self.client.load_system_host_keys()  # Adding new host key to the local HostKeys object (in case of missing)
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # AutoAddPolicy for missing host key to be set before connection setup.
        self.client.connect(self.server, self.port, self.user, self.password)  # ssh connection
        self.scp = SCPClient(self.client.get_transport())  # scp connection
        self.sftp = self.client.open_sftp()
        pass

    def run_script_python(self, full_path):
        # Run the script
        stdin, stdout, stderr = self.client.exec_command("nohup python " + full_path)
        # Check if everything is running well
        print(stdout.read().decode('utf-8'))
        # Exit while letting the scipt running
        pass

    def execute_command(self, command, time_out=None):
        stdin, stdout, stderr = self.client.exec_command(command, timeout=time_out)  # Execute command on SSH terminal using exec_command
        return stdout

    def upload_file(self, remote_folder, file_name, local_folder):
        # Upload a file from local computer to the Raspberry
        self.scp.put(local_folder + file_name, remote_folder)  # scp file upload
        pass

    def download_file(self, remote_folder, file_name, local_folder, new_file_name):
        # Download a file from Raspberry to local computer
        self.scp.get(remote_folder + file_name, recursive=True, local_path=local_folder + new_file_name)  # scp file download
        pass

    def upload_folder(self, remote_folder, local_folder):
        # Upload a folder from local computer to the Raspberry
        self.scp.put(local_folder, recursive=True, remote_path=remote_folder)
        pass

    def download_folder(self, remote_folder, local_folder):
        # Download a folder from Raspberry to local computer
        self.scp.get(remote_folder, recursive=True, local_path=local_folder)  # scp folder download
        pass

    def close_connection(self):
        # Exit ssh while letting the scipt running
        self.client.close()
        pass
