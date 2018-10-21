from kivy.app import App
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class ActionBtn(Button):

    _category = StringProperty()
    _action = StringProperty()

    def set_btn_size(self, obj, size):
        self.width = size[0] * .2 + self.texture_size[0]
        self.height = size[1] * .2


class ActionsSection(BoxLayout):
    _tl_text = StringProperty()
    _tl_font_size = NumericProperty(0)
    _actions_stack = ObjectProperty(None)

    def set_section_size(self, obj, size):
        self._tl_font_size = min(size[0], size[1]) * .09


class ActionsScreen(Screen):

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
        self.screen_layout = Factory.AddNewScreenLayout()
        self.add_widget(self.screen_layout)

        self.screen_layout._content.add_widget(
            self.create_new_section('Instants', self.instants)
        )
        self.screen_layout._content.add_widget(
            self.create_new_section('Quantity-based', self.quantity_based)
        )
        self.screen_layout._content.add_widget(
            self.create_new_section('Time-based', self.time_based)
        )

    def create_new_section(self, category, actions):
        new_section = Factory.ActionsSection(_tl_text=category)
        self.bind(size=new_section.set_section_size)
        self.populate_actions_stack(new_section, category, actions)

        return new_section

    def populate_actions_stack(self, section, category, actions):
        for action in actions:
            action_btn = self.create_new_action_btn(category, action)
            section._actions_stack.add_widget(action_btn)

    def create_new_action_btn(self, category, action):
        action_btn = Factory.ActionBtn(
            _category=category, _action=action, text=action)
        self.bind(size=action_btn.set_btn_size)
        action_btn.bind(on_release=self.start_adding)

        return action_btn

    def start_adding(self, action_btn):
        app = App.get_running_app()
        screen_manager = app.root._screen_manager

        if action_btn._category == 'Instants':
            screen_manager.current = 'add_instants_screen'
            screen_manager._add_instants_screen.initialize(
                action_btn._category, action_btn._action)

        elif action_btn._category == 'Quantity-based':
            screen_manager.current = 'add_qbased_screen'
            screen_manager._add_qbased_screen.initialize(
                action_btn._category, action_btn._action)

        elif action_btn._category == 'Time-based':
            screen_manager.current = 'add_tbased_screen'
            screen_manager._add_tbased_screen.initialize(
                action_btn._category, action_btn._action)
