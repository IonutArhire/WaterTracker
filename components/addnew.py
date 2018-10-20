from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class AddNewBtn(Button):

    category = StringProperty()
    action = StringProperty()

    def set_btn_size(self, obj, size):
        self.width = size[0] * .2 + self.texture_size[0]
        self.height = size[1] * .2


class AddNewSection(BoxLayout):
    _tl_text = StringProperty()
    _tl_font_size = NumericProperty(0)
    _btn_stack = ObjectProperty(None)

    def set_section_size(self, obj, size):
        self._tl_font_size = min(size[0], size[1]) * .09


class AddNewScreen(Screen):

    instants = [
        'Drink',
        'Flush',
        'Washing Clothes',
        'Other'
    ]

    quantity_based = [
        'Washing Dishes',
        'Washing Clothes (manually)',
        'Watering Plants'
    ]

    time_based = [
        'Showering'
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        addnew_screen_layout = Factory.AddNewScreenLayout()
        self.add_widget(addnew_screen_layout)

        addnew_screen_layout._content.add_widget(
            self.create_new_section('Instants', self.instants)
        )
        addnew_screen_layout._content.add_widget(
            self.create_new_section('Quantity-based', self.quantity_based)
        )
        addnew_screen_layout._content.add_widget(
            self.create_new_section('Time-based', self.time_based)
        )

    def create_new_section(self, category, actions):
        new_section = Factory.AddNewSection(_tl_text=category)
        self.bind(size=new_section.set_section_size)
        self.populate_btn_stack(new_section, category, actions)

        return new_section

    def populate_btn_stack(self, section, category, actions):
        for action in actions:
            btn = self.create_new_btn(category, action)
            section._btn_stack.add_widget(btn)

    def create_new_btn(self, category, action):
        btn = Factory.AddNewBtn(category=category, action=action, text=action)
        self.bind(size=btn.set_btn_size)
        btn.bind(on_release=self.start_recording)

        return btn

    def start_recording(self, btn):
        app = App.get_running_app()
        app.root._screen_manager.current = 'record_screen'
        app.root._record_screen.initialize(btn.category, btn.action)
