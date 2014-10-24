import threading
import sh
import logging
from datetime import datetime

# threads which were not used for this zombie_time, will be
# considered as zombies, and will be killed
zombie_time = 2 * 60 * 60  # 2 hours


class ClientThread(threading.Thread):
    def __init__(self, UUID):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.UUID = UUID
        self.set_last_called()

    def set_last_called(self):
        self.last_called = datetime.now()

    def isZombie(self):
        datetime_now = datetime.now()
        inactice_time = datetime_now - self.last_called

        if inactice_time.seconds > zombie_time:
            zombied = True
        else:
            zombied = False
        return zombied

    def run(self):
        logging.info("Starting thread %s" % (self.UUID))

    def execute_command(self, cmd):
        self.set_last_called()
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
