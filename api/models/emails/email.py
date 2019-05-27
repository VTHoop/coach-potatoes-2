import uuid

from common.database import Database
import models.emails.constants as EmailConstants


class Email(object):
    def __init__(self, email, _id=None):
        self.email = email
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "email": self.email,
            "_id": self._id
        }

    @classmethod
    def get_all_emails(cls):
        return [cls(**elem) for elem in Database.find(EmailConstants.COLLECTION, {})]
