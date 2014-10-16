import zmq

import pyrun

from base import Base


class Subscriber(Base):
    """
    A Subscriber listens for requests over zeromq, and converts them into pyrun commands.
    """
    def __init__(self, *args, **kwargs):
        super(Subscriber, self).__init__(*args, **kwargs)

        self.socket_type = zmq.SUB
        self.socket_opt = zmq.SUBSCRIBE

        self._connect()

    def run(self, verbose=False):
        while True:
            raw_data = self.socket.recv()

            task = self._extract_msg(raw_data)

            pyrun.run(**task)

    def hello_world(self, limit=20):
        c = 0
        while True:
            raw_data = self.socket.recv()

            task = self._extract_msg(raw_data)

            print(task)

            c += 1

            if c >= limit:
                break


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], ":", ["limit=", "ip=", "port=", "hello"])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_hello = False
    run_limit = 0

    for o, a in opts:
        if o in ["--hello"]:
            run_hello = True

        if o in ["--limit"]:
            run_limit = int(a)

        if o in ["--ip"]:
            run_ip = a

        if o in ["--port"]:
            run_port = a

    if run_hello:
        # Force a limit
        if run_limit == 0:
            run_limit = 20

        print("Running Hello World as Subscriber...")

        sub = Subscriber(ip=run_ip, port=run_port)
        sub.hello_world(limit=run_limit)

        print("Done.")



