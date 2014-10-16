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


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], ":", ["ip=", "port=", "hello"])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_hello = False

    for o, a in opts:
        if o in ["--hello"]:
            run_hello = True

        if o in ["--ip"]:
            run_ip = a

        if o in ["--port"]:
            run_port = a

    if run_hello:
        print("Running Hello World as Publisher...")

        pub = Publisher(ip=run_ip, port=run_port)
        pub.hello_world()

        print("Done.")



