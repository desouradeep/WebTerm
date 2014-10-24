import threading
import sh


def log(data):
    print "LOG: %s" % (data)


class ClientThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        log("Starting")

    def execute_command(self, cmd):
        cmd = tuple(cmd.split())
        try:
            if cmd[0] == 'ls':
                cmd += ('--color=auto', )
            run_function = getattr(sh, cmd[0])
            output = run_function(*cmd[1:])
            log("OUT: %s" % output)
        except sh.CommandNotFound, e:
            log("ERR: %s" % e)
