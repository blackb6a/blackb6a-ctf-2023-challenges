import subprocess
import os, sys
import tempfile
import time

def receive_data():
    # Ask the user to provide the data length
    data_length = int(input("Enter the data length: "))
    
    # Receive the data from stdin
    data = sys.stdin.buffer.read(data_length)

    # Create a temp file with a random name
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    filename = temp_file.name
    # Write the data to the temp file
    temp_file.write(data)

    # Close the temp file
    temp_file.close()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chmod(filename, 0o555)

    pid = subprocess.Popen(["./sandbox", filename], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    pid.kill()
    os.remove(filename)
if __name__ == "__main__":
    receive_data()

