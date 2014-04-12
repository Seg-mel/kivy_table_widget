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
from table import Table
from table import NewButton
from kivy.clock import Clock
from kivy.core.window import Window
import time



class MainScreen(BoxLayout):
    """docstring for MainScreen"""
    def __init__(self):
        super(MainScreen, self).__init__()
        print Window.size
        self.my_table = Table()
        self.add_widget(self.my_table)
        self.my_table.cols = 2
        for i in range(110):
            # self.my_table.add_row('asd','qwe'+str(i),'zxc'+str(i),'123'+str(i))
            self.my_table.add_custom_row(NewButton(text=('asd%d'%i)), 
                                          NewButton(text=('qwe%d'%i)))
        # self.my_table.label_panel.visible = False
        print 'VISIBLE', self.my_table.label_panel.visible
        self.my_table.label_panel.height_widget = 50
        print 'HEIGHT LABEL PANEL', self.my_table.label_panel.height_widget
        self.my_table.num_panel.width_widget = 34
        print 'WIDTH NUM PANEL', self.my_table.num_panel.width_widget
        # self.my_table.num_panel.visible = False
        self.my_table.choose_row(0)
        print self.my_table.get_row_count()
        self.my_table.del_row(5)
        self.my_table.grid.bkcolor = '#ff0000'
        self.my_table.label_panel.bkcolor = '#00ff00'
        self.my_table.num_panel.bkcolor = '#0000ff'
        # Clock.schedule_interval(self.clock_callback, 1)

    def clock_callback(self, dt):
        ''' Kivy clock method '''
        self.my_table.redraw_widget()
        self.my_table.grid.redraw_widget()



class TestApp(App):
    """ App class """
    def build(self):
        return MainScreen()

    def on_pause(self):
        return True



if __name__ in ('__main__', '__android__'):
    TestApp().run()