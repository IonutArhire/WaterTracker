from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class AddNewBtn(Button):

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
        super(AddNewScreen, self).__init__(**kwargs)
        addnew_screen_layout = Factory.AddNewScreenLayout()
        self.add_widget(addnew_screen_layout)

        addnew_screen_layout.content.add_widget(
            self.create_new_section('Instants', self.instants)
        )
        addnew_screen_layout.content.add_widget(
            self.create_new_section('Quantity-based', self.quantity_based)
        )
        addnew_screen_layout.content.add_widget(
            self.create_new_section('Time-based', self.time_based)
        )

    def create_new_section(self, title, actions):
        new_section = Factory.AddNewSection(_tl_text=title)
        self.bind(size=lambda a, b: new_section.set_section_size(a, b))
        self.populate_btn_stack(new_section, actions)

        return new_section

    def populate_btn_stack(self, section, actions):
        for action in actions:
            btn = self.create_new_btn(action)
            section._btn_stack.add_widget(btn)

    def create_new_btn(self, action):
        btn = Factory.AddNewBtn(text=action)
        self.bind(size=lambda a, b: btn.set_btn_size(a, b))

        return btn

    def start_recording(self, text):
        print(text)
