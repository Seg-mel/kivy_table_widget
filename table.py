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



class Table(BoxLayout):
    """My table widget"""

    def __init__(self):
        super(Table, self).__init__()
        self._cols = 0
        self._choosen_row = 0
        # Getting the LabelPanel object for working with it
        self._label_panel = self.children[1]
        # Getting the GridTable object for working with it
        self._grid = self.children[0].children[0].children[0]
        # Getting the NumPanel object for working with it
        self._number_panel = self.children[0].children[0].children[1]
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)

    @property
    def grid(self):
        """ Grid object """
        return self._grid

    @property
    def label_panel(self):
        """ Label panel object """
        return self._label_panel

    @property
    def number_panel(self):
        """ Number panel object """
        return self._number_panel

    @property
    def cols(self):
        """ Get/set number of columns """
        return self._cols
    @cols.setter
    def cols(self, number=0):
        self._cols = number
        self.grid.cols = number
        for num in range(number):
            self.label_panel.add_widget(NewLabel())

    def add_button_row(self, *args):
        """ 
        Add new row to table with Button widgets.
        Example: add_row('123', 'asd', '()_+')
        """
        if len(args)==self._cols:
            row_widget_list = []
            for num, item in enumerate(args):
                Cell = type('Cell', (NewCell, Button), {})
                cell = Cell()
                cell.text = item
                self.grid.add_widget(cell)
                # Create widgets row list
                row_widget_list.append(self.grid.children[0])
            # Adding a widget to two-level array 
            self._grid._cells.append(row_widget_list)
            self.number_panel.add_widget(NewNumberLabel(
                                               text=str(self.get_row_count())))
        else:
            print 'ERROR: Please, add %s strings in method\'s arguments' %\
                                                              str(self._cols)

    def add_row(self, *args):
        """
        Add new row to table with custom widgets.
        Example: add_custom_row([Button, text='text'], [TextInput])
        """
        if len(args)==self._cols:
            row_widget_list = []
            for num, item in enumerate(args):
                Cell = type('Cell', (NewCell, item[0]), {})
                cell = Cell()
                for key in item[1].keys():
                    setattr(cell, key, item[1][key])
                self.grid.add_widget(cell)
                # Create widgets row list
                row_widget_list.append(self.grid.children[0])
            # Adding a widget to two-level array 
            self._grid._cells.append(row_widget_list)
            self.number_panel.add_widget(NewNumberLabel(
                                               text=str(self.get_row_count())))
        else:
            print 'ERROR: Please, add %s strings in method\'s arguments' %\
                                                              str(self._cols)

    def del_row(self, number):
        """ Delete a row by number """
        for cell in self.grid.cells[number]:
            self.grid.remove_widget(cell)
        del self.grid.cells[number]
        self.number_panel.remove_widget(self.number_panel.children[0])

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
        if len(self.grid.children) > 0:
            for col_num in range(self._cols):
                old_grid_element = self.grid.cells[self._choosen_row][col_num]
                old_grid_element.set_background_color(
                                                old_grid_element.DEFAULT_COLOR)
                self.grid.cells[row_num][col_num].set_background_color()
            self._choosen_row = row_num

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        print 'TABLE SIZE %s POS %s' % (str(self.size), str(self.pos))
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex('#333333'))
            Rectangle(pos=self.pos, size=self.size)



class ScrollViewTable(ScrollView):
    """ScrollView for grid table"""
    def __init__(self, **kwargs):
        super(ScrollViewTable, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self._bkcolor = '#444444'

    @property
    def bkcolor(self):
        """ Background color """
        return self._bkcolor
    @bkcolor.setter
    def bkcolor(self, color):
        with self.canvas.before:
            # Not clear, because error
            self._bkcolor = color
            Color(*get_color_from_hex(self._bkcolor))
        self.redraw_widget()

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size)



class LabelPanel(BoxLayout):
    """Panel for column labels"""
    def __init__(self, **kwargs):
        super(LabelPanel, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self._visible = True
        self._height = 30
        self._bkcolor = '#444444'

    @property
    def bkcolor(self):
        """ Background color """
        return self._bkcolor
    @bkcolor.setter
    def bkcolor(self, color):
        self._bkcolor = color
        self.redraw_widget()

    @property
    def visible(self):
        """ Get/set panel visible """
        return self._visible
    @visible.setter
    def visible(self, visible=True):
        if visible:
            self._visible = visible
            self.height = self._height
        else:
            self._visible = visible
            self.height = 0

    @property
    def height_widget(self):
        """ Get/set panel height """
        return self.height
    @height_widget.setter
    def height_widget(self, height=30):
        if self._visible == True:
            self._height = height
            self.height = height

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            if len(self.children) > 0:
                self.children[-1].bkcolor = self._bkcolor
            Color(*get_color_from_hex(self._bkcolor))
            Rectangle(pos=self.pos, size=self.size)



class NumPanel(BoxLayout):
    """Num panel class"""
    def __init__(self, **kwargs):
        super(NumPanel, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self._visible = True
        self._width = 30
        self._bkcolor = '#444444'

    @property
    def bkcolor(self):
        """ Background color """
        return self._bkcolor
    @bkcolor.setter
    def bkcolor(self, color):
        self._bkcolor = color
        self.redraw_widget()

    @property
    def visible(self):
        """ Get/set panel visible """
        return self._visible
    @visible.setter
    def visible(self, visible=True):
        # Get null label object
        null_label = self.parent.parent.parent.label_panel.children[-1]
        if visible:
            self._visible = visible
            self.width = self._width
            null_label.width = self._width
        else:
            self._visible = visible
            self.width = 0
            null_label.width = 0

    @property
    def width_widget(self):
        """ Get/set panel width """
        return self.width
    @width_widget.setter
    def width_widget(self, width=30):
        # Get null label object
        null_label = self.parent.parent.parent.label_panel.children[-1]
        if self._visible == True:
            self._width = width
            self.width = width
            null_label.width = width

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex(self._bkcolor))
            Rectangle(pos=self.pos, size=self.size)



class ScrollViewBoxLayout(GridLayout):
    """ScrollView's BoxLayout class"""
    def __init__(self, **kwargs):
        super(ScrollViewBoxLayout, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        


class GridTable(GridLayout):
    """This is the table itself"""
    def __init__(self, **kwargs):
        super(GridTable, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self.bind(minimum_height=self.setter('height'))
        self._bkcolor = '#444444'
        self._cells = []
        self._current_cell = None

    @property
    def current_cell(self):
        """ Current cell """
        return self._current_cell
    @current_cell.setter
    def current_cell(self, value):
        self._current_cell = value

    @property
    def bkcolor(self):
        """ Background color """
        return self._bkcolor
    @bkcolor.setter
    def bkcolor(self, color):
        self._bkcolor = color
        self.redraw_widget()

    @property
    def cells(self):
        """ Two-level array of cells """
        return self._cells

    def get_row_index(self, item_object):
        """ Get select item index """
        for index, child in enumerate(reversed(self.children)):
            if item_object == child:
                columns = self.parent.parent.parent._cols
                row_index = index/columns
                print str(row_index), 'row is choosen'
                return row_index
                break

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        print 'GRID SIZE %s POS %s' % (str(self.size), str(self.pos))
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex(self._bkcolor))
            Rectangle(pos=self.pos, size=self.size)
            self.parent.parent.bkcolor = self._bkcolor



class NewCell(object):
    """Grid/button element for table"""

    DEFAULT_COLOR = '#123123'
    DEFAULT_CONFIG_COLOR = get_color_from_hex(DEFAULT_COLOR)

    def __init__(self, **kwargs):
        super(NewCell, self).__init__(**kwargs)
        # Binds for click on this cell
        self.bind(on_press = self.on_press_button)
        try:
            self.bind(focus=self.on_press_button)
        except: pass

    def set_background_color(self, hex_color='#005522'):
        """ Set hex background color """
        self.background_color = get_color_from_hex(hex_color)

    def on_press_button(self, *args):
        """ On press method for current object """
        self.parent.current_cell = args[0]
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

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on label label'



class NullLabel(Button):
    """Num Label object class"""

    def __init__(self, **kwargs):
        super(NullLabel, self).__init__(**kwargs)
        self.bind(pos=self.redraw_widget)
        self.bind(size=self.redraw_widget)
        self.bind(on_press = self.on_press_button)
        self._bkcolor = '#444444'

    @property
    def bkcolor(self):
        """ Background color """
        return self._bkcolor
    @bkcolor.setter
    def bkcolor(self, color):
        self._bkcolor = color
        self.redraw_widget()
        
    def set_background_color(self, hex_color='#ffffff'):
        """ Set hex background color """
        self.background_color = get_color_from_hex(hex_color)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        # Disable click
        self.state = 'normal'
        print 'pressed on null label'

    def redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*get_color_from_hex(self._bkcolor))
            Rectangle(pos=self.pos, size=self.size)
        
        

class NewNumberLabel(Button):
    """Num Label object class"""

    def __init__(self, **kwargs):
        super(NewNumberLabel, self).__init__(**kwargs)
        self.bind(on_press = self.on_press_button)

    def on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on number label'