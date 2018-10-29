# So that we can import from
# other directories (like ..)
import sys
sys.path.append('..')

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from storage import storage


class HistoryScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_layout = Factory.HistoryScreenLayout()
        self.add_widget(self.screen_layout)

        self.populate_history_list()
        storage.bind(store=self.update)

    def populate_history_list(self):
        for entity in storage.store:
            entry = Factory.HistoryEntry()

            entry_text = self.get_entry_text(entity)
            entry_content = Factory.HistoryEntryLabel(text=entry_text)

            entry.add_widget(entry_content)
            self.screen_layout.history_list.add_widget(entry)

    def get_entry_text(self, entity):
        result = ''

        for key, val in entity.items():
            result += key + ': ' + str(val) + '\n'

        return result[:-1]

    def update(self, _, new_list):
        new_entry = Factory.HistoryEntry()

        entry_text = self.get_entry_text(new_list[-1])
        entry_content = Factory.HistoryEntryLabel(text=entry_text)

        new_entry.add_widget(entry_content)
        self.screen_layout.history_list.add_widget(new_entry)
