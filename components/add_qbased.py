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


class AddQBasedScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_layout = Factory.AddQBasedLayout()
        self.add_widget(self.screen_layout)

    def initialize(self, category, action):
        self.category = category
        self.action = action

        self.screen_layout._tl_text = self.action

    def add(self):
        new_id = str(uuid4())
        quantity = self.screen_layout._user_input_quantity.text
        amount_per_item = self.screen_layout._user_input_amount.text
        cur_date = str(datetime.now())

        store.put(new_id,
                  category=self.category,
                  action=self.action,
                  total_amount=int(quantity) * int(amount_per_item),
                  quantity=quantity,
                  amount_per_item=amount_per_item,
                  date=cur_date)

        # Update the history screen with the newly inserted record
        app = App.get_running_app()
        app.root._screen_manager._history_screen.update(new_id)

        app.root._screen_manager.current = 'start_screen'
