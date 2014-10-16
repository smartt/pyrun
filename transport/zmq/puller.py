import zmq

import pyrun

from base import Base


class Puller(Base):
    """
    A Puller listens for requests over zeromq, and converts them into pyrun commands.
    """
    def __init__(self, *args, **kwargs):
        super(Puller, self).__init__(*args, **kwargs)

        self.socket_type = zmq.PULL

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
        opts, args = getopt.getopt(sys.argv[1:], ":", ["limit=", "hello"])
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

    if run_hello:
        # Force a limit
        if run_limit == 0:
            run_limit = 20

        print("Running Hello World as Puller...")

        sub = Puller()
        sub.hello_world(limit=run_limit)

        print("Done.")



