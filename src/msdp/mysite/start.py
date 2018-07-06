import os, sys
import subprocess

def start_django():
    base_path = os.path.dirname(os.path.realpath(__file__))
    shellcmd = "/".join([base_path, 'manage.py'])
    command = ["/usr/bin/python3", shellcmd, "runserver", "0.0.0.0:8000"]

    # First method to run the command in python
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    # If we want to run command in frontground, uncomment the following 2 lines
    #stdout,stderr = process.communicate()
    #print(stdout)


    # Another method to execute command
    #subprocess.call(command, stdout=outfile)

def main():
    start_django()

if __name__ == '__main__':
    main()
