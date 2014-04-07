#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import kivy
from kivy.config import Config
Config.set("input", "mouse", "mouse, disable_multitouch")
import table
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from table import MyTable



class MainScreen(BoxLayout):
    """docstring for MainScreen"""
    def __init__(self):
        super(MainScreen, self).__init__()
        my_table = MyTable()
        self.add_widget(my_table)
        my_table.cols = 4
        for i in range(32):
            my_table.add_line('asd','qwe'+str(i),'zxc'+str(i),'123'+str(i))
        my_table.label_panel.visible = True
        print 'VISIBLE', my_table.label_panel.visible
        my_table.label_panel.height_widget = 50
        print 'HEIGHT PANEL', my_table.label_panel.height_widget
        element = my_table.get_item(12,2)
        my_table.choose_row(1)
        print my_table.get_row_count()



class TestApp(App):
    """ App class """
    def build(self):
        return MainScreen()

    def on_pause(self):
        return True



if __name__ in ('__main__', '__android__'):
    TestApp().run()