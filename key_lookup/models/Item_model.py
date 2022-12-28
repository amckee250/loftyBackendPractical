from django.db import models


class ItemModel(models.Model):
    """
    Model used for DB and business logic encapsulation of a key, value
    pair object used in data increment endpoints

    Notes: Naming convention is a bit redundant as to not shadow Python's item, key, value keywords

    Future Development: May be worth looking at using a key-value DB to store this data opposed to SQL
    """

    # Supports up to 9.99~ Billion unique objects
    item_key = models.CharField(unique=True, max_length=10)
    item_value = models.IntegerField(default=1)

    def __str__(self):
        return f'Key: {self.item_key} - Value:{self.item_value[:20]}'



