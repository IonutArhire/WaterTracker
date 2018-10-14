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
from kivy.storage.jsonstore import JsonStore

from addnew import *


class RecordScreen(Screen):
    pass


class StatsScreen(Screen):

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.add_widget(Factory.StatsScreenLayout())


class HistoryScreen(Screen):

    store = JsonStore('storage.json')

    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)
        history_screen_layout = Factory.HistoryScreenLayout()
        self.add_widget(history_screen_layout)

        for key in self.store.keys():
            entry = Factory.HistoryEntry()

            entry_text = self.get_entry_text(key)
            entry_content = Factory.HistoryEntryLabel(text=entry_text)

            entry.add_widget(entry_content)
            history_screen_layout.history_list.add_widget(entry)

    def get_entry_text(self, key):
        result = ''
        entity = self.store.get(key)

        for key, val in entity.items():
            result += key + ': ' + str(val) + '\n'

        return result[:-1]


class WaterTrackerRoot(BoxLayout):

    screen_manager = ObjectProperty(None)
    history_screen = ObjectProperty(None)

    def onBackBtn(self):
        self.screen_manager.current = 'start_screen'
        return True


class WaterTrackerApp(App):

    def __init__(self, **kwargs):
        super(WaterTrackerApp, self).__init__(**kwargs)
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
