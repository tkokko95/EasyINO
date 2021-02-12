import subprocess
from sys import argv

if __name__ == '__main__':
    if '-u' not in argv and '--upload' not in argv:
        subprocess.run(['arduino-cli', 'boards' ,'listall'], capture_output=True)
        print(subprocess.CompletedProcess.returncode)
