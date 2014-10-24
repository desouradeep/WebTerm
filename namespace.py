import json
import logging
from uuid import uuid4
from client_thread import ClientThread

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin, RoomsMixin


class WebTermNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    client_threads = {}
    logging.basicConfig(filename='webterm.log', level=logging.INFO)

    def generate_uuid(self):
        logging.info("Generating UUID")
        return str(uuid4())

    def add_new_client(self, UUID):
        new_client_thread = ClientThread(UUID)

        logging.info("Attempting to add new client...")
        self.client_threads[UUID] = new_client_thread
        logging.info("New client added.")

        new_client_thread.start()
        logging.info("Client thread started")

    def recv_connect(self):
        '''
        Called when connection is establised with a client.
        Generates a uuid, assigns it to the client. This uuid is to be used to
        keep track of the thread assigned to the client.
        '''
        logging.info("New client connection requested")
        new_uuid = self.generate_uuid()

        # create a dedicated thread for the client, and add it to the
        # client threads list
        self.add_new_client(new_uuid)

        payload = {
            "uuid": new_uuid
        }

        self.emit('establish-connection', json.dumps(payload))
        logging.info("UUID sent to client")

    def on_user_message(self, payload):
        '''
        Called when a client sends a message to the realtime server
        '''
        # these will record errors and results if any and will be placed
        # in the payload json which is sent back to the client
        error = ''
        result = ''

        logging.info("New command recieved from a client.")
        payload = json.loads(payload)

        client_thread_uuid = payload.get("uuid", None)
        if client_thread_uuid is None:
            logging.info("Looks like the client is fake?!!")
            error = "No client UUID found, cannot proceed with a valid UUID"
        else:
            try:
                client_thread = self.client_threads[client_thread_uuid]

                # valid client found
                command = payload.get('command', '')
                result = client_thread.execute_command(command)

            except KeyError:
                logging.info("Client thread doesn't exist")
                error = 'No matching client key found.'

            payload = {
                'error': error,
                'result': result,
            }

        self.emit('command', json.dumps(payload))
