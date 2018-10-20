import kivy
kivy.require('1.10.1')

# So that we can import from
# other directories (like ./components)
import sys
sys.path.append('./components')

from kivy.app import App
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from storage import store

from actions import *
from add_qbased import *
from add_instants import *


class StatsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Factory.StatsScreenLayout())


class HistoryScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_layout = Factory.HistoryScreenLayout()
        self.add_widget(self.screen_layout)

        for key in store.keys():
            entry = Factory.HistoryEntry()

            entry_text = self.get_entry_text(key)
            entry_content = Factory.HistoryEntryLabel(text=entry_text)

            entry.add_widget(entry_content)
            self.screen_layout.history_list.add_widget(entry)

    def get_entry_text(self, key):
        result = ''
        entity = store.get(key)

        for key, val in entity.items():
            result += key + ': ' + str(val) + '\n'

        return result[:-1]

    def update(self, new_id):
        new_entry = Factory.HistoryEntry()

        entry_text = self.get_entry_text(new_id)
        entry_content = Factory.HistoryEntryLabel(text=entry_text)

        new_entry.add_widget(entry_content)
        self.screen_layout.history_list.add_widget(new_entry)


class WaterTrackerRoot(BoxLayout):

    _screen_manager = ObjectProperty(None)

    def onBackBtn(self):
        self._screen_manager.current = 'start_screen'
        return True


class WaterTrackerApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.onBackBtn)

    def build(self):
        return WaterTrackerRoot()

    def onBackBtn(self, window, key, *args):
        ''' When the back button is pressed on
            android, the app should redirect
            the user to the main menu.
        '''
        if key == 27:
            return self.root.onBackBtn()


if __name__ in ('__main__', '__android__'):
    WaterTrackerApp().run()
