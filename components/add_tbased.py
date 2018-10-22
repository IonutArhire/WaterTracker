# So that we can import from
# other directories (like ..)
import sys
sys.path.append('..')

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty


from datetime import datetime
from uuid import uuid4


from storage import store


class AddTBasedScreen(Screen):

    sw_active = False
    time = NumericProperty(-1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_layout = Factory.AddTBasedLayout1()
        self.add_widget(self.screen_layout)

    def initialize(self, category, action):
        self.category = category
        self.action = action

        self.screen_layout._tl_text = self.action

    def on_click_stopwatch(self):
        if not self.sw_active:
            self.sw_active = True
            self.start_stopwatch()
        else:
            self.sw_active = False
            self.stop_stopwatch()

    def tick(self, *_):
        self.time += 1

    def update_stopwatch(self, _, time):
        self.screen_layout._stopwatch_text = str(time) + 's'

    def start_stopwatch(self):
        self.timer_proc = Clock.schedule_interval(self.tick, 1)
        self.bind(time=self.update_stopwatch)
        self.time = 0

    def stop_stopwatch(self):
        Clock.unschedule(self.timer_proc)
        self.unbind(time=self.update_stopwatch)

        self.remove_widget(self.screen_layout)
        self.screen_layout = Factory.AddTBasedLayout2()
        self.add_widget(self.screen_layout)

        self.screen_layout._tl_text = self.action
        self.screen_layout._stopwatch_result = f'Time passed: {str(self.time)}s'

    def add(self):
        new_id = str(uuid4())
        amount_per_second = self.screen_layout._user_input.text
        cur_date = str(datetime.now())

        store.put(new_id,
                  category=self.category,
                  action=self.action,
                  total_amount=int(amount_per_second) * self.time,
                  seconds_passed=self.time,
                  amount_per_second=amount_per_second,
                  date=cur_date)

        # Update the history screen with the newly inserted record
        app = App.get_running_app()
        app.root._screen_manager._history_screen.update(new_id)

        app.root._screen_manager.current = 'start_screen'
