import kivy
kivy.require('1.10.0')

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

from stats import *
from history import *
from actions import *
from add_qbased import *
from add_tbased import *
from add_instants import *


class StatsScreen(Screen):

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.add_widget(Factory.StatsScreenLayout())


class WaterTrackerRoot(BoxLayout):

    _screen_manager = ObjectProperty(None)

    def onBackBtn(self):
        self._screen_manager.current = 'start_screen'
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
