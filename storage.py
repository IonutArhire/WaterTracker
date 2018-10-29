from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.storage.jsonstore import JsonStore


class Storage(EventDispatcher):

    store = ListProperty()
    json_store = JsonStore('storage.json')

    instants = [
        'Drink',
        'Flush',
        'Washing Clothes',
        'Other'
    ]

    quantity_based = [
        'Washing Dishes',
        'Washing Clothes (manually)',
        'Watering Plants'
    ]

    time_based = [
        'Showering'
    ]

    def __init__(self):
        for key in self.json_store.keys():
            entity = self.json_store.get(key)
            self.store.append(entity)


storage = Storage()
