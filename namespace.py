from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin, RoomsMixin

import json
from uuid import uuid4

class WebTermNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):

    def recv_connect(self):
        '''
        Called when connection is establised with a client.
        Generates a uuid, assigns it to the client. This uuid is to be used to
        keep track of the thread assigned to the client.
        '''
        new_uuid = str(uuid4())
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
        out, err = system(payload['command'])
        response_payload = {
            'output': out,
            'error': err,
        }

        self.emit('data', json.dumps(response_payload))
