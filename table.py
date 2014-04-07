#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import kivy
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ListProperty, BooleanProperty



Builder.load_file('./table.kv')

COLOR_BKGRND = '#aaaaaa'



class MyTable(BoxLayout):
    """My table widget"""

    def __init__(self):
        super(MyTable, self).__init__()
        self._cols = 0
        self.choosen_row = 0
        # Getting the LabelPanel object for working with it
        self.label_panel = self.children[1]
        # Getting the GridTable object for working with it
        self.grid = self.children[0].children[0].children[0]
        # Getting the NumPanel object for working with it
        self.num_panel = self.children[0].children[0].children[1]

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, number=0):
        """ Set number of columns """
        self._cols = number
        self.grid.cols = number
        self.label_panel.add_widget(NewNullLabel())
        for num in range(number):
            self.label_panel.add_widget(NewLabel())

    def add_line(self, *args):
        """ 
        Add new line to table.
        Example: add_line('123','asd','()_+')
         """
        if len(args)==self._cols:
            for num, item in enumerate(args):
                self.grid.add_widget(NewButton(text=item))
            self.num_panel.add_widget(NewNumberLabel(
                                               text=str(self.get_row_count())))
        else:
            print 'ERROR: Please, add %s strings in method\'s arguments' %\
                                                              str(self._cols)

    def get_item(self, row_num, col_num):
        """ 
        Get item by coordinates. 
        row_num = 0..n, col_num = 0..n.
        Example: get_item(13,12)
        """
        item_num = row_num*self._cols+col_num
        grid_children = reversed(self.grid.children)
        if (len(self.grid.children)>item_num) and (col_num<self._cols):
            for num, child in enumerate(grid_children):
                if num == item_num:
                    return child
                    break
        else:
            print "EROOR: Coordinates does not exist!"
            return None

    def get_row_count(self):
    	""" Get row count in our table """
    	grid_item_count = len(self.grid.children)
    	row_count = grid_item_count/self._cols
    	remainder = grid_item_count%self._cols
    	if remainder>0:
    		row_count+=1
    	return row_count

    def choose_row(self, row_num=0):
        """ 
        Choose a row in our table.
        Example: choose_row(1)
        """
        for col_num in range(self._cols):
            old_grid_element = self.get_item(self.choosen_row, col_num)
            old_grid_element.set_background_color(
                                                old_grid_element.DEFAULT_COLOR)
            self.get_item(row_num, col_num).set_background_color()
        self.choosen_row = row_num



class ScrollViewTable(ScrollView):
    """ScrollView for grid table"""
    def __init__(self, **kwargs):
        super(ScrollViewTable, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self.set_background_color(COLOR_BKGRND)

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size)

    def set_background_color(self, hex_color='#ffffff'):
        """ Setting scrollview color """
        with self.canvas.before:
            color = get_color_from_hex(hex_color)
            Color(*color)
            Rectangle(size=self.size, pos=self.pos)



class LabelPanel(BoxLayout):
    """Panel for column labels"""
    def __init__(self, **kwargs):
        super(LabelPanel, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self.set_background_color('#444444')
        self._visible = True
        self._height = 30

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible=True):
        """ Set panel visible """
        if visible:
            self._visible = visible
            self.height = self._height
        else:
            self._visible = visible
            self.height = 0

    @property
    def height_widget(self):
        return self.height

    @height_widget.setter
    def height_widget(self, height=30):
        """ Set panel height """
        if self._visible == True:
            self._height = height
            self.height = height

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size)

    def set_background_color(self, hex_color='#ffffff'):
        """ Setting scrollview color """
        with self.canvas.before:
            color = get_color_from_hex(hex_color)
            Color(*color)
            Rectangle(size=self.size, pos=self.pos)



class NumPanel(BoxLayout):
    """Num panel class"""
    def __init__(self, **kwargs):
        super(NumPanel, self).__init__(**kwargs)



class ScrollViewBoxLayout(GridLayout):
    """ScrollView's BoxLayout class"""
    def __init__(self, **kwargs):
        super(ScrollViewBoxLayout, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        


class GridTable(GridLayout):
    """This is the table itself"""
    def __init__(self, **kwargs):
        super(GridTable, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))

    def get_row_index(self, item_object):
        """ Get select item index """
        for index, child in enumerate(reversed(self.children)):
            if item_object == child:
                columns = self.parent.parent.parent._cols
                row_index = index/columns
                print str(row_index), 'row is choosen'
                return row_index
                break



class NewButton(Button):
    """Grid/button element for table"""

    DEFAULT_COLOR = '#123123'
    DEFAULT_CONFIG_COLOR = get_color_from_hex(DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super(NewButton, self).__init__(**kwargs)
        self.bind(on_press = self.on_press_button)

    def set_background_color(self, hex_color='#005522'):
        """ Set hex background color """
        self.background_color = get_color_from_hex(hex_color)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on grid item'
        self.main_table = self.parent.parent.parent.parent
        self.grid = self.parent
        self.set_background_color()
        self.main_table.choose_row(self.grid.get_row_index(self))



class NewLabel(Button):
    """Label element for label panel"""
    def __init__(self, **kwargs):
        super(NewLabel, self).__init__(**kwargs)
        self.bind(on_press = self.on_press_button)
        

    def set_background_color(self, hex_color='#005522'):
        """ Set hex background color """
        self.background_color = get_color_from_hex(hex_color)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on label label'



class NewNullLabel(Button):
    """Num Label object class"""

    DEFAULT_COLOR = '#444444'
    DEFAULT_CONFIG_COLOR = get_color_from_hex(DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super(NewNullLabel, self).__init__(**kwargs)
        self.bind(on_press = self.on_press_button)
        

    def set_background_color(self, hex_color='#005522'):
        """ Set hex background color """
        self.background_color = get_color_from_hex(hex_color)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on null label'
        
        

class NewNumberLabel(Button):
    """Num Label object class"""

    def __init__(self, **kwargs):
        super(NewNumberLabel, self).__init__(**kwargs)
        self.bind(on_press = self.on_press_button)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on number label'