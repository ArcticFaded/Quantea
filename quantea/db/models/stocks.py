from pymodm import fields, MongoModel
import random
import string

# Widgets belong to a concrete state and can contain labels
class Stock(MongoModel):
    key = fields.CharField(blank=False, primary_key=True)
    ticker = fields.CharField(blank=False)
    close = fields.FloatField(blank=True)
    volume = fields.BigIntegerField(blank=True)
    date = fields.DateTimeField(blank=False)