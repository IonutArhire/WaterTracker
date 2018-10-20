# So that we can import from
# other directories (like ..)
import sys
sys.path.append('..')

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


from datetime import datetime
from uuid import uuid4


from storage import store


class RecordScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.record_screen_layout = Factory.RecordScreenLayout()
        self.add_widget(self.record_screen_layout)

    def initialize(self, category, action):
        self.category = category
        self.action = action

        self.record_screen_layout._tl_text = f'{self.category}: {self.action}'

    def record(self):
        new_id = str(uuid4())
        amount = self.record_screen_layout._user_input.text
        cur_date = str(datetime.now())

        store.put(new_id,
                  category=self.category,
                  action=self.action,
                  amount=amount,
                  date=cur_date)

        # Update the history screen with the newly inserted record
        app = App.get_running_app()
        app.root._history_screen.update(new_id)
