from os import getenv
from pymodm import connect

# Expose db classes, for creating new folder requires __init__.py to be present

from .models import Stock

connect('mongodb://localhost:27017/machine_learning_trader')