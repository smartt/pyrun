import zmq

from base import Base

class Pusher(Base):
    """
    A Pusher sends pyrun requests over zeromq to Pullers.
    """
    def __init__(self, *args, **kwargs):
        super(Pusher, self).__init__(*args, **kwargs)

        self.socket_type = zmq.PUSH
        self.async = True
        self._connect()

    def hello_world(self):
        """
        A simple test that will send a series of messages to all listeners.
        """
        for i in range(1, 21):
            msg = "<{}> Oh hai".format(i)

            print("  sending: {}".format(msg))

            self.send_json({'msg': msg})


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
        opts, args = getopt.getopt(sys.argv[1:], ":", ["ip=", "port=", "limit=", "hello", "pusher", "puller"])
    except getopt.GetoptError, err:
        print(str(err))
        sys.exit(2)

    run_hello = False
    run_ip = None
    run_port = None
    run_puller = False
    run_pusher = False

    for o, a in opts:
        if o in ["--hello"]:
            run_hello = True

        if o in ["--pusher"]:
            run_pusher = True

        if o in ["--puller"]:
            run_puller = True

        if o in ["--ip"]:
            run_ip = a

        if o in ["--port"]:
            run_port = a

        if o in ["--limit"]:
            run_limit = int(a)

    if run_pusher:
        if run_hello:
            print("Running Hello World as Pusher...")

            pub = Pusher(ip=run_ip, port=run_port)
            pub.hello_world()

            print("Done.")

    elif run_puller:
        if run_hello:
            print("Running Hello World as Puller...")

            sub = Puller(ip=run_ip, port=run_port)
            sub.hello_world(limit=run_limit)

            print("Done.")

        else:
            sub = Puller(ip=run_ip, port=run_port)
            sub.run()



