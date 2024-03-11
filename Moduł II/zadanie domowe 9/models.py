from mongoengine import Document, StringField, DateField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField


class Author(Document):
    fullname = StringField()
    born_date = DateField()
    born_location = StringField()
    description = StringField()


class Tag(EmbeddedDocument):
    name = StringField()


class Quote(Document):
    tags = ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField(Author)
    quote = StringField()
    meta = {"allow_inheritance": True}
