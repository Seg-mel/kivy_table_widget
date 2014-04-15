#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config
Config.set("input", "mouse", "mouse, disable_multitouch")
# import logging
# from kivy.logger import Logger
# Logger.setLevel(logging.ERROR)
import table
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from table import Table
from kivy.clock import Clock
from kivy.animation import Animation



class MainScreen(BoxLayout):
    """docstring for MainScreen"""
    def __init__(self):
        super(MainScreen, self).__init__()
        self.my_table = Table()
        self.add_widget(self.my_table)
        self.my_table.cols = 2
        for i in range(500):
            # self.my_table.add_button_row('123','456'+str(i))
            self.my_table.add_row([Button, {'text':'button%s'%i,
                                            'color_widget': [0,0,0.5,1],
                                            'color_click': [0,1,0,1]}], 
                                  [TextInput, {'text':'textinput%s'%i,
                                               'color_click': [1,0,0,1]}])
        # self.my_table.label_panel.visible = False
        self.my_table.label_panel.height_widget = 50
        # self.my_table.number_panel.auto_width = False
        # self.my_table.number_panel.width_widget = 100
        # self.my_table.number_panel.visible = False
        self.my_table.choose_row(3)
        print "ROW COUNT:", self.my_table.row_count
        self.my_table.del_row(5)
        # self.my_table.grid.bkcolor = [1, 0, 0, 1]
        # self.my_table.label_panel.bkcolor = [0, 1, 0, 1]
        # self.my_table.number_panel.bkcolor = [0, 0, 1, 1]
        # self.my_table.scroll_view.bar_width = 10
        self.my_table.scroll_view.scroll_type = ['bars']
        self.my_table.grid.cells[0][0].text = 'edited button text'
        self.my_table.grid.cells[1][1].text = 'edited textinput text'
        self.my_table.grid.cells[20][1].height = 50
        self.my_table.grid.cells[30][1].height = 100
        self.my_table.grid.cells[5][1].height = 100
        self.my_table.grid.cells[3][0].height = 100
    #     Clock.schedule_interval(self.clock_callback, 0.2)

    # def clock_callback(self, dt):
    #     ''' Kivy clock method '''
    #     pass



class TestApp(App):
    """ App class """
    def build(self):
        return MainScreen()

    def on_pause(self):
        return True



if __name__ in ('__main__', '__android__'):
    TestApp().run()