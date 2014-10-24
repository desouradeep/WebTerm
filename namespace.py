from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin, RoomsMixin

import json
from uuid import uuid4
from client_thread import ClientThread


class WebTermNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def __init__(self):
        BaseNamespace.__init__(self)
        RoomsMixin.__init__(self)
        BroadcastMixin.__init__(self)

        # client_threads is used to record the
        # threads dedicated to the clients
        self.client_threads = []

    def generate_uuid(self):
        return str(uuid4())

    def add_new_client(self, UUID):
        new_client_thread = ClientThread(UUID)
        self.client_threads.append(new_client_thread)

    def recv_connect(self):
        '''
        Called when connection is establised with a client.
        Generates a uuid, assigns it to the client. This uuid is to be used to
        keep track of the thread assigned to the client.
        '''
        new_uuid = self.generate_uuid()

        # create a dedicated thread for the client, and add it to the
        # client threads list
        self.add_new_client(new_uuid)

        payload = {
            "uuid": new_uuid
        }

        self.emit('establish-connection', json.dumps(payload))

    def on_user_message(self, payload):
        '''
        Called when a client sends a message to the realtime server
        '''
        payload = json.loads(payload)
        print "Recieved: ", payload['command']

        self.emit('data', json.dumps(response_payload))
