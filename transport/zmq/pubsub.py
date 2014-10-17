import zmq

from base import Base

class Publisher(Base):
    """
    A Publisher sends pyrun requests over zeromq to a Subscriber.
    """
    def __init__(self, *args, **kwargs):
        super(Publisher, self).__init__(*args, **kwargs)

        self.socket_type = zmq.PUB
        self._connect()

    def send(self, msg):
        self.socket.send(self._pack_msg(msg))

    def hello_world(self):
        """
        A simple test that will send a series of messages to all listeners.
        """
        for i in range(1, 21):
            msg = "<{}> Oh hai".format(i)

            print("  sending: {}".format(msg))

            self.send({'msg': msg})


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

            runner.run(**task)

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
        opts, args = getopt.getopt(sys.argv[1:], ":", ["limit=", "ip=", "port=", "hello", "pub", "sub"])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_hello = False
    run_limit = 0
    run_ip = None
    run_port = None
    run_pub = False
    run_sub = False

    for o, a in opts:
        if o in ["--pub"]:
            run_pub = True

        if o in ["--sub"]:
            run_sub = True

        if o in ["--hello"]:
            run_hello = True

        if o in ["--ip"]:
            run_ip = a

        if o in ["--port"]:
            run_port = a

        if o in ["--limit"]:
            run_limit = int(a)

    if run_pub:
        if run_hello:
            print("Running Hello World as Publisher...")

            pub = Publisher(ip=run_ip, port=run_port)
            pub.hello_world()

            print("Done.")

    elif run_sub:
        if run_hello:
            # Force a limit
            if run_limit == 0:
                run_limit = 20

            print("Running Hello World as Subscriber...")

            sub = Subscriber(ip=run_ip, port=run_port)
            sub.hello_world(limit=run_limit)

            print("Done.")




