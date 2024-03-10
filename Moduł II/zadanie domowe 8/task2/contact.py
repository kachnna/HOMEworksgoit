from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)
