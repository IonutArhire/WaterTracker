from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen


class RecordScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        record_screen_layout = Factory.RecordScreenLayout()
        self.add_widget(record_screen_layout)

    def initialize(self, category, action):
        print('test')
