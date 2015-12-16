from mongoengine import *


class GameRanking(Document):
    country = StringField(required=True, unique=True)
    code = StringField(required=True)
    rank = DictField()
