import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout



class WaterTrackerRoot(BoxLayout):
    pass


class WaterTrackerApp(App):
    def build(self):
        return WaterTrackerRoot()

    def on_pause(self):
        '''Not sure what this does
        '''
        return True

if __name__ in ('__main__', '__android__'):
    WaterTrackerApp().run()