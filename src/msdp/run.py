import os, sys, time, subprocess
import logging, threading
from multiprocessing import Process
import mysite.start as ms
import subprocess

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


def webserver_func():
    ms.start_django()

def webserver_stop():
    command = "ps ax|grep 8000 |awk '{print $1}' |xargs kill -9"
    subprocess.call([command], shell=True)

def main():
    current_path = os.path.dirname(os.path.abspath(__file__))
    stdout = current_path + "/../../log/mysite.log"
    logging.basicConfig(
       level=logging.DEBUG,
       format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
       filename=stdout,
       filemode='a'
    )
    if len(sys.argv) == 1:
        print(sys.argv[0] + " {start|stop}")
        sys.exit(0)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl


    fpid = os.fork()
    if fpid!=0:
        sys.exit(0)
    if sys.argv[1] == 'start':
        webserver_func()
    elif sys.argv[1] == 'stop':
        webserver_stop()
        print("stop service")


if __name__ == "__main__": 
    main()
