import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout



class WaterTrackerRoot(BoxLayout):
    def onBackBtn(self):
        self.ids.screen_manager.current = 'start_screen'
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