from kivy.app import App
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

from storage import storage


class StatsLabel(Label):

    def set_lbl_size(self, obj, size):
        self.font_size = min(size[0], size[1]) * .04


class StatsSection(BoxLayout):
    _tl_text = StringProperty()
    _tl_font_size = NumericProperty(0)
    _stats_table = ObjectProperty(None)

    def set_section_size(self, obj, size):
        self._tl_font_size = min(size[0], size[1]) * .09


class StatsScreen(Screen):

    # Here we'll keep the last computed amount
    #   for every action and it's corresponding widget
    cache = {}

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.screen_layout = Factory.StatsScreenLayout()
        self.add_widget(self.screen_layout)

        self.initialize_cache()
        self.populate_cache()

        self.screen_layout._content.add_widget(
            self.create_new_section('Instants', storage.instants)
        )
        self.screen_layout._content.add_widget(
            self.create_new_section('Quantity-based', storage.quantity_based)
        )
        self.screen_layout._content.add_widget(
            self.create_new_section('Time-based', storage.time_based)
        )

        self.set_total_lbl()

        storage.bind(store=self.update)

    def initialize_cache(self):
        def initialize_cache_by_category(actions):
            for action in actions:
                self.cache[action] = {}
                self.cache[action]['total_amount'] = 0

        initialize_cache_by_category(storage.instants)
        initialize_cache_by_category(storage.quantity_based)
        initialize_cache_by_category(storage.time_based)

    def populate_cache(self):
        for entity in storage.store:
            action = entity['action']
            total_amount = int(entity['total_amount'])
            self.cache[action]['total_amount'] += total_amount

    def create_new_section(self, category, actions):
        new_section = Factory.StatsSection(_tl_text=category)
        self.bind(size=new_section.set_section_size)
        self.bind(size=new_section._action_header.set_lbl_size)
        self.bind(size=new_section._amount_header.set_lbl_size)
        self.populate_table(new_section, actions)

        return new_section

    def populate_table(self, section, actions):
        for action in actions:
            action_lbl = self.create_new_stats_label(action)

            amount = self.cache[action]['total_amount']
            amount_lbl = self.create_new_stats_label(str(amount))

            self.cache[action]['amount_lbl'] = amount_lbl
            section._stats_table.add_widget(action_lbl)
            section._stats_table.add_widget(amount_lbl)

    def create_new_stats_label(self, text):
        lbl = Factory.StatsLabel(text=str(text))
        self.bind(size=lbl.set_lbl_size)

        return lbl

    def update(self, _, new_list):
        new_entity = new_list[-1]
        action = new_entity['action']
        total_amount = int(new_entity['total_amount'])

        self.cache[action]['total_amount'] += total_amount
        self.cache[action]['amount_lbl'].text = str(
            self.cache[action]['total_amount'])

        self.set_total_lbl()

    def set_total_lbl(self):
        total = sum(self.cache[action]['total_amount']
                    for action in self.cache)
        self.screen_layout._total_lbl.text = 'Total amount (ml):' + str(total)
