import os, sys
import subprocess
import logging, threading

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''


    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def start_django():
    base_path = os.path.dirname(os.path.realpath(__file__))
    shellcmd = "/".join([base_path, 'manage.py'])
    command = "python {} runserver 0.0.0.0:8000".format(shellcmd)
    subprocess.call([command], shell=True)

def main():
    base_path = os.path.dirname(os.path.realpath(__file__))
    stdout = base_path + "/../../../log/django.log"
    logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
       filename=stdout,
       filemode='a'
    )
    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    start_django()

def test():
    return("This is a test")


if __name__ == '__main__':
    main()
