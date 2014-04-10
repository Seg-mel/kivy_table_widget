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
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from table import MyTable
from table import NewButton
import time



class MainScreen(BoxLayout):
    """docstring for MainScreen"""
    def __init__(self):
        super(MainScreen, self).__init__()
        my_table = MyTable()
        self.add_widget(my_table)
        my_table.cols = 4
        for i in range(110):
            my_table.add_line('asd','qwe'+str(i),'zxc'+str(i),'123'+str(i))
            # my_table.add_custom_line(NewButton(text=('asd%d'%i)), NewButton(text=('qwe%d'%i)))
        # my_table.label_panel.visible = False
        print 'VISIBLE', my_table.label_panel.visible
        my_table.label_panel.height_widget = 30
        print 'HEIGHT LABEL PANEL', my_table.label_panel.height_widget
        my_table.num_panel.width_widget = 34
        print 'WIDTH NUM PANEL', my_table.num_panel.width_widget
        # my_table.num_panel.visible = False
        element = my_table.get_item(12,2)
        my_table.choose_row(0)
        print my_table.get_row_count()
        my_table.del_line(5)



class TestApp(App):
    """ App class """
    def build(self):
        return MainScreen()

    def on_pause(self):
        return True



if __name__ in ('__main__', '__android__'):
    TestApp().run()