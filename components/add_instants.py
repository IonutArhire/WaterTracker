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


from storage import storage


class AddInstantsScreen(Screen):

    def __init__(self, **kwargs):
        super(AddInstantsScreen, self).__init__(**kwargs)
        self.screen_layout = Factory.AddInstantsLayout()
        self.add_widget(self.screen_layout)

    def initialize(self, category, action):
        self.category = category
        self.action = action

        self.screen_layout._tl_text = self.action

    def add(self):
        new_id = str(uuid4())
        amount = self.screen_layout._user_input.text
        cur_date = str(datetime.now())

        storage.json_store.put(new_id,
                               category=self.category,
                               action=self.action,
                               total_amount=amount,
                               date=cur_date)

        # Update the live store with the newly inserted record
        storage.store.append(storage.json_store.get(new_id))

        app = App.get_running_app()
        app.root._screen_manager.current = 'start_screen'
