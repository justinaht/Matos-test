from flask_marshmallow import Schema
from marshmallow.fields import Nested, Dict, List, Str, Int


class ExceptionSchema(Schema):
    class Meta:
        fields = ['message', 'status']

    message = Str()
    status = Int()
