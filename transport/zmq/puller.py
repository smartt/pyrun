import zmq

from pyrun import runner

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
            data = self.recv_json()

            task = self._as_task(data)

            try:
                runner.run(**task)
            except:
                pass

    def hello_world(self, limit=20):
        c = 0
        while True:
            data = self.recv_json()

            print(data)

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
    run_ip = None
    run_port = None

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

        print("Running Hello World as Puller...")

        sub = Puller(ip=run_ip, port=run_port)
        sub.hello_world(limit=run_limit)

        print("Done.")

    else:
        sub = Puller(ip=run_ip, port=run_port)
        sub.run()




