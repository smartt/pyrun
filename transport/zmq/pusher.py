import zmq

from base import Base

class Pusher(Base):
    """
    A Pusher sends pyrun requests over zeromq to Pullers.
    """
    def __init__(self, *args, **kwargs):
        super(Pusher, self).__init__(*args, **kwargs)

        self.socket_type = zmq.PUSH
        self._connect()

    def hello_world(self):
        """
        A simple test that will send a series of messages to all listeners.
        """
        for i in range(1, 21):
            msg = "<{}> Oh hai".format(i)

            print("  sending: {}".format(msg))

            self.send_json({'msg': msg})


# --------------------------------------------------
#               MAIN
# --------------------------------------------------
if __name__ == "__main__":
    import sys
    import getopt

    try:
        opts, args = getopt.getopt(sys.argv[1:], ":", ["hello"])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_hello = False

    for o, a in opts:
        if o in ["--hello"]:
            run_hello = True

    if run_hello:
        print("Running Hello World as Pusher...")

        pub = Pusher()
        pub.hello_world()

        print("Done.")



