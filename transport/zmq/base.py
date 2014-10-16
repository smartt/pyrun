import json
import time
import zmq


class Base(object):
    def __init__(self, ip='127.0.0.1', port='5678', topic='', verbose=False, *args, **kwargs):
        if ip is None:
            self.ip = '127.0.0.1'
        else:
            self.ip = ip

        if port is None:
            self.port = '5678'
        else:
            self.port = port

        self.topic = topic
        self.context = None
        self.socket = None
        self.socket_type = None
        self.socket_opt = None
        self.verbose = verbose

    def _socket_should_bind(self, t):
        return t in (zmq.PUB, zmq.PUSH)

    def _connect(self):
        self.context = zmq.Context()

        # Setup listener
        self.socket = self.context.socket(self.socket_type)
        should_bind = self._socket_should_bind(self.socket_type)

        if should_bind:
            self.socket.bind("tcp://{ip}:{port}".format(ip=self.ip, port=self.port))
        else:
            self.socket.connect("tcp://{ip}:{port}".format(ip=self.ip, port=self.port))

        if self.socket_opt:
            self.socket.setsockopt(self.socket_opt, self.topic)

        if should_bind:
            time.sleep(1)  # Give it a sec to setup

    def _get_default_struct(self):
        return {
            "id": None,
            "model": None,
            "package": None,
            "action": None,
            "args": None,
            "function": None,
            "method": None,
            "orm": None,
        }

    def _extract_msg(self, data):
        msg = data[len(self.topic)+1:]

        if self.verbose:
            print("msg: ", msg)

        json_data = json.loads(msg)

        if self.verbose:
            print("json: ", json_data)

        return self._as_task(json_data)

    def _as_task(self, data):
        d = self._get_default_struct()

        # Merge
        for k, v in data.items():
            d[k] = v

        return d
        
    def _pack_msg(self, data):
        return "{topic} {msg}".format(
            topic=self.topic,
            msg=json.dumps(data)
        )

    def send(self, msg):
        self.socket.send(msg)

    def send_json(self, msg):
        self.socket.send(json.dumps(msg))

    def recv_json(self):
        data = self.socket.recv()

        return json.loads(data)

