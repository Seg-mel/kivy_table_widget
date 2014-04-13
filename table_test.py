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



class MainScreen(BoxLayout):
    """docstring for MainScreen"""
    def __init__(self):
        super(MainScreen, self).__init__()
        self.my_table = Table()
        self.add_widget(self.my_table)
        self.my_table.cols = 2
        for i in range(110):
            # self.my_table.add_button_row('123','456'+str(i))
            self.my_table.add_row([Button, {'text':'asd%s'%i}], 
                                         [TextInput, {'text':'qwe%s'%i}])
        # self.my_table.label_panel.visible = False
        self.my_table.label_panel.height_widget = 50
        # self.my_table.number_panel.auto_width = False
        # self.my_table.number_panel.width_widget = 100
        # self.my_table.number_panel.visible = False
        self.my_table.choose_row(0)
        print "ROW COUNT:", self.my_table.row_count
        self.my_table.del_row(3)
        self.my_table.grid.bkcolor = '#ff0000'
        self.my_table.label_panel.bkcolor = '#00ff00'
        self.my_table.number_panel.bkcolor = '#0000ff'
        self.my_table.grid.cells[0][0].text = 'asdasdasdasds'
        self.my_table.grid.cells[1][1].text = 'qqweqweqwe'
        self.my_table.grid.cells[1][1].height = 50
        self.my_table.grid.cells[3][0].height = 100
    #     Clock.schedule_interval(self.clock_callback, 1)

    # def clock_callback(self, dt):
    #     ''' Kivy clock method '''
    #     self.my_table.add_row([Button, {'text':'asd'}], 
    #                                      [TextInput, {'text':'qwe'}])



class TestApp(App):
    """ App class """
    def build(self):
        return MainScreen()

    def on_pause(self):
        return True



if __name__ in ('__main__', '__android__'):
    TestApp().run()