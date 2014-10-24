import threading
import sh
import logging


class ClientThread(threading.Thread):
    def __init__(self, UUID):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.UUID = UUID

    def run(self):
        logging.info("Starting thread %s" % (self.UUID))

    def execute_command(self, cmd):
        output = ''
        error = ''
        cmd = tuple(cmd.split())

        try:
            if cmd[0] == 'ls':
                cmd += ('--color=auto', )
            run_function = getattr(sh, cmd[0])
            output = str(run_function(*cmd[1:]))
        except Exception, e:
            error = e.message

        return output + "\n" + error
