from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
db = SQLAlchemy()
import os
from twilio.rest import Client
## Nos permite leer de un archivo .env
from dotenv import load_dotenv
from os import access, environ
load_dotenv()

class Queue:

    def __init__(self):
        self._queue = []
        # depending on the _mode, the queue has to behave like a FIFO or LIFO
        self._mode = 'FIFO'
        # Your Account SID from twilio.com/console
        self.account_sid = environ.get('account_sid')

        # Your Auth Token from twilio.com/console
        self.auth_token = environ.get('auth_token')

    def enqueue(self, item):
        self._queue.append(item)
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            to="+541151756994",
            from_="+12028738292",
            body=f"Hello, you were added successfully to the queue, there are {len(self._queue) -1} users before you."
        )

    def dequeue(self):
        if self._mode == 'LIFO':
            lastUser = self._queue.pop(0)
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                to=environ.get('to'),
                from_=environ.get('from_'),
                body=f"Hello {lastUser['name']}, it's your turn now."
            )
            return lastUser['name']

        if self._mode == 'LIFO':
            lastUser = self._queue.pop()
            client = Client(self.account_sid, self.auth_token)
            message = client.messages.create(
                to=environ.get('to'),
                from_=environ.get('from_'),
                body=f"Hello {lastUser['name']}, it's your turn now"
            )
            return lastUser['name']

    def get_queue(self):
        users = []
        for user in self._queue:
            users.append(user['name'])
            client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            to=environ.get('to'),
            from_=environ.get('from_'),
            body=f"Updated queue: {users}"
        )

    def size(self):
        return len(self._queue)
