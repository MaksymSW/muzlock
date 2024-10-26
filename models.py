from datetime import datetime

from mongoengine import Document
from mongoengine.fields import BooleanField, DateTimeField, StringField, IntField
from connect import connect



class TimestampedDocument(Document):

    meta = {'allow_inheritance': True, 'abstract': True}

    created_at = DateTimeField(required=True, default=datetime.now)
    updated_at = DateTimeField(required=True, default=datetime.now)

    def save(
        self,
        force_insert=False,
        validate=True,
        clean=True,
        write_concern=None,
        cascade=None,
        cascade_kwargs=None,
        _refs=None,
        save_condition=None,
        signal_kwargs=None,
        **kwargs,
    ):
        self.updated_at = datetime.now()
        super().save(
            force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs, save_condition,
            signal_kwargs, **kwargs
        )

class Users(TimestampedDocument):
    first_name = StringField()
    last_name = StringField()
    tg_id = IntField()
    is_active = BooleanField(default=True)
    language = StringField()
