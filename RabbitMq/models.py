from mongoengine import Document, StringField
from mongoengine.fields import BooleanField


class Users(Document):
    fullname = StringField(required=True)
    email = StringField(max_length=100)
    phone = StringField(max_length=20)
    delivery_status = BooleanField(default=False)
    preferred_mode = StringField()
