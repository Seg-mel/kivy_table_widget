#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Table module
# Copyright (C) 2014 Musikhin Andrey <melomansegfault@gmail.com>

import kivy
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from os.path import join, dirname, abspath



Builder.load_file(join(dirname(abspath(__file__)),'./table.kv'))



class Table(BoxLayout):
    """My table widget"""

    def __init__(self):
        super(Table, self).__init__()
        self._cols = 0
        self._chosen_row = 0
        # Getting the LabelPanel object for working with it
        self._label_panel = self.children[1]
        # Getting the GridTable object for working with it
        self._grid = self.children[0].children[0].children[0]
        # Getting the NumberPanel object for working with it
        self._number_panel = self.children[0].children[0].children[1]
        # Getting the ScrollViewTable object for working with it
        self._scroll_view = self.children[0]

    @property
    def scroll_view(self):
        return self._scroll_view

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

    @property
    def row_count(self):
        """ Get row count in our table """
        grid_item_count = len(self.grid.children)
        count = grid_item_count/self._cols
        remainder = grid_item_count%self._cols
        if remainder > 0:
            count += 1
        return count

    def add_button_row(self, *args):
        """ 
        Add new row to table with Button widgets.
        Example: add_button_row('123', 'asd', '()_+')
        """
        if len(args) == self._cols:
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
                                               text=str(self.row_count)))
        else:
            print 'ERROR: Please, add %s strings in method\'s arguments' %\
                                                              str(self._cols)

    def add_row(self, *args):
        """
        Add new row to table with custom widgets.
        Example: add_row([Button, text='text'], [TextInput])
        """
        if len(args) == self._cols:
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
                                               text=str(self.row_count)))
            # Default the choosing
            if len(self.grid.cells) == 1:
                self.choose_row(0)
        else:
            print 'ERROR: Please, add %s strings in method\'s arguments' %\
                                                              str(self._cols)

    def del_row(self, number):
        """ Delete a row by number """
        if len(self.grid.cells) > number:
            for cell in self.grid.cells[number]:
                self.grid.remove_widget(cell)
            del self.grid.cells[number]
            self.number_panel.remove_widget(self.number_panel.children[0])
            # If was deleted the chosen row
            if self._chosen_row == number:
                self.choose_row(number)
        else:
            print 'ERROR: Nothing to delete...'

    def choose_row(self, row_num=0):
        """ 
        Choose a row in our table.
        Example: choose_row(1)
        """
        if len(self.grid.cells) > row_num:
            for col_num in range(self._cols):
                old_grid_element = self.grid.cells[self._chosen_row][col_num]
                current_cell = self.grid.cells[row_num][col_num]
                old_grid_element._background_color(
                                                 old_grid_element.color_widget)
                current_cell._background_color(current_cell.color_click)
            self._chosen_row = row_num
        elif len(self.grid.cells) == 0:
            print 'ERROR: Nothing to choose...'
        else:
            for col_num in range(self._cols):
                old_grid_element = self.grid.cells[self._chosen_row][col_num]
                current_cell = self.grid.cells[-1][col_num]
                old_grid_element._background_color(
                                                 old_grid_element.color_widget)
                current_cell._background_color(current_cell.color_click)
            self._chosen_row = row_num



class ScrollViewTable(ScrollView):
    """ScrollView for grid table"""
    def __init__(self, **kwargs):
        super(ScrollViewTable, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self._color = [.2, .2, .2, 1]
        # Start scroll_y pisition
        self.scroll_y = 1

    @property
    def color(self):
        """ Background color """
        return self._color
    @color.setter
    def color(self, color):
        with self.canvas.before:
            # Not clear, because error
            self._color = color
            Color(*self._color)
        self._redraw_widget()

    def up(self, row_num=1):
        """ Scrolling up when the chosen row is out of view """
        if self.size != [100.0, 100.0] and (self.parent.row_count != 0):
            if self.parent._chosen_row - row_num > 0:
                self.parent.choose_row(self.parent._chosen_row - row_num)
            else: self.parent.choose_row(0)
            grid_height = float(self.children[0].height)
            scroll_height = float(grid_height - self.height)
            cur_cell = self.children[0].children[0].\
                       cells[self.parent._chosen_row][0]
            cur_cell_height = float(cur_cell.height)
            cur_row_y = float(cur_cell.y)
            # The convert scroll Y position
            _scroll_y = self.scroll_y * scroll_height + self.height - \
                                                        cur_cell_height
            # Jump to the chosen row
            top_scroll_excess = cur_row_y - cur_cell_height
            down_scroll_excess = cur_row_y + self.height - cur_cell_height
            if _scroll_y > down_scroll_excess or _scroll_y < top_scroll_excess:
                new_scroll_y = 0 + \
                          1*((cur_row_y-self.height/2)/100)/(scroll_height/100)
                if new_scroll_y < 0:
                    self.scroll_y = 0
                else:
                    self.scroll_y = new_scroll_y
            # Scrolling to follows the current row
            if (cur_row_y) > _scroll_y:
                self.scroll_y = self.scroll_y + \
                                    1*(cur_cell_height/100)/(scroll_height/100)
            # Stopping the scrolling when start of grid
            if self.scroll_y > 1:
                self.scroll_y = 1
            self._update_mouse(self.effect_y, self.scroll_y)

    def down(self, row_num=1):
        """ Scrolling down when the chosen row is out of view """
        if self.size != [100.0, 100.0] and (self.parent.row_count != 0):
            if self.parent._chosen_row + row_num < self.parent.row_count - 1:
                self.parent.choose_row(self.parent._chosen_row + row_num)
            else: self.parent.choose_row(self.parent.row_count-1)
            grid_height = float(self.children[0].height)
            scroll_height = float(grid_height - self.height)
            cur_cell = self.children[0].children[0].\
                       cells[self.parent._chosen_row][0]
            cur_cell_height = float(cur_cell.height)
            cur_row_y = float(cur_cell.y)
            # The convert scroll Y position
            _scroll_y = self.scroll_y * scroll_height
            # Jump to the chosen row
            top_scroll_excess = cur_row_y - self.height + cur_cell_height
            down_scroll_excess = cur_row_y + cur_cell_height
            if _scroll_y < top_scroll_excess or _scroll_y > down_scroll_excess:
                new_scroll_y = 0 + \
                          1*((cur_row_y-self.height/2)/100)/(scroll_height/100)
                if new_scroll_y > 1:
                    self.scroll_y = 1
                else:
                    self.scroll_y = new_scroll_y
            # Scrolling to follows the current row
            if cur_row_y < _scroll_y:
                self.scroll_y = self.scroll_y - \
                                    1*(cur_cell_height/100)/(scroll_height/100)
            # Stopping the scrolling when end of grid
            if self.scroll_y < 0:
                self.scroll_y = 0
            self._update_mouse(self.effect_y, self.scroll_y)


    def home(self):
        """ Scrolling to the top of the table """
        if self.parent.row_count != 0:
            self.scroll_y = 1
            self.parent.choose_row(0)
            self._update_mouse(self.effect_y, self.scroll_y)

    def end(self):
        """ Scrolling to the bottom of the table """
        if self.parent.row_count != 0:
            self.scroll_y = 0
            self.parent.choose_row(self.parent.row_count - 1)
            self._update_mouse(self.effect_y, self.scroll_y)

    def pgup(self, row_count=10):
        """ Scrolling up when the chosen row is out of view, but with step """
        if self.parent.row_count != 0:
            self.up(row_count)

    def pgdn(self, row_count=10):
        """ 
        Scrolling down when the chosen row is out of view, but with step 
        """
        if self.parent.row_count != 0:
            self.down(row_count)

    def _update_mouse(self, event, value):
        """ Updating the mouse position """
        if event:
            event.value = (event.max + event.min) * value

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size)
        # Editting the number panel width
        number_panel = self.children[0].children[1]
        if number_panel.auto_width and len(number_panel.children) > 0:
            last_number_label = self.children[0].children[1].children[0]
            number_panel.width_widget = last_number_label.texture_size[0] + 10



class ScrollViewBoxLayout(GridLayout):
    """ScrollView's BoxLayout class"""
    def __init__(self, **kwargs):
        super(ScrollViewBoxLayout, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))



class LabelPanel(BoxLayout):
    """Panel for column labels"""
    def __init__(self, **kwargs):
        super(LabelPanel, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self._visible = True
        self._height = 30
        self._color = [.2, .2, .2, 1]

    @property
    def labels(self):
        """ List of label objects """
        return [child for child in reversed(self.children)]

    @property
    def color(self):
        """ Background color """
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self._redraw_widget()

    @property
    def visible(self):
        """ Get/set panel visibility """
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
        if self._visible:
            self._height = height
            self.height = height

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            if len(self.children) > 0:
                self.children[-1].color = self._color
            Color(*self._color)
            Rectangle(pos=self.pos, size=self.size)



class NumberPanel(BoxLayout):
    """Num panel class"""
    def __init__(self, **kwargs):
        super(NumberPanel, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self._visible = True
        self._width = 30
        self._color = [.2, .2, .2, 1]
        self._auto_width = True

    @property
    def auto_width(self):
        """ Auto width this panel """
        return self._auto_width
    @auto_width.setter
    def auto_width(self, value):
        self._auto_width = value

    @property
    def color(self):
        """ Background color """
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self._redraw_widget()

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
        return self._width
    @width_widget.setter
    def width_widget(self, width):
        null_label = self.parent.parent.parent.label_panel.children[-1]
        if self._visible == True:
            self._width = width
            self.width = width
            null_label.width = width

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*self._color)
            Rectangle(pos=self.pos, size=self.size)



class GridTable(GridLayout):
    """This is the table itself"""
    def __init__(self, **kwargs):
        super(GridTable, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self.bind(minimum_height=self.setter('height'))
        self._color = [.2, .2, .2, 1]
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
    def color(self):
        """ Background color """
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self._redraw_widget()

    @property
    def cells(self):
        """ Two-level array of cells """
        return self._cells

    def _get_row_index(self, item_object):
        """ Get select item index """
        for index, child in enumerate(reversed(self.children)):
            if item_object == child:
                columns = self.parent.parent.parent._cols
                row_index = index/columns
                print str(row_index), 'row is chosen'
                return row_index
                break

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        self.parent.parent.color = self._color
        # Hide the grid view and the number panel if the grid view is empty
        if len(self.children) == 0:
            self.height = .01
            self.parent.children[-1].height = .01



class NewCell(object):
    """Grid/button element for table"""

    def __init__(self, **kwargs):
        super(NewCell, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self.bind(on_press = self._on_press_button)
        try:
            self.bind(focus=self._on_press_button)
        except: pass
        self._color_widget = [1, 1, 1, 1]
        self._color_click = [.3, .3, .3, 1]

    def _background_color(self, value):
        """ Set the background color """
        self.background_color = value

    @property
    def color_widget(self):
        """ Cell color """
        return self._color_widget
    @color_widget.setter
    def color_widget(self, value):
        self._color_widget = value
        self.background_color = value

    @property
    def color_click(self):
        """ Cell click color """
        return self._color_click
    @color_click.setter
    def color_click(self, value):
        self._color_click = value

    def _on_press_button(self, *args):
        """ On press method for current object """
        self.parent.current_cell = args[0]
        self.state = 'normal'
        print 'pressed on grid item'
        self.main_table = self.parent.parent.parent.parent
        self.grid = self.parent
        # self.color = self._color
        self.main_table.choose_row(self.grid._get_row_index(self))

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        # Editting a height of number label in this row
        for num, line in enumerate(self.parent.cells):
            for cell in line:
                if cell == self:
                    self.parent.parent.children[1].children[-(num+1)].height =\
                                                                    self.height
                    break
                break



class NewLabel(Button):
    """Label element for label panel"""
    def __init__(self, **kwargs):
        super(NewLabel, self).__init__(**kwargs)
        self.bind(on_press = self._on_press_button)

    def _on_press_button(self, touch=None):
        """ On press method for current object """
        # Disable a click
        self.state = 'normal'
        print 'pressed on name label'



class NullLabel(Button):
    """Num Label object class"""

    def __init__(self, **kwargs):
        super(NullLabel, self).__init__(**kwargs)
        self.bind(size=self._redraw_widget)
        self.bind(on_press = self._on_press_button)
        self._color = [.2, .2, .2, 1]

    @property
    def color(self):
        """ Background color """
        return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self._redraw_widget()

    def _on_press_button(self, touch=None):
        """ On press method for current object """
        # Disable a click
        self.state = 'normal'
        print 'pressed on null label'

    def _redraw_widget(self, *args):
        """ Method of redraw this widget """
        with self.canvas.before:
            self.canvas.before.clear()
            Color(*self._color)
            Rectangle(pos=self.pos, size=self.size)
        
        

class NewNumberLabel(Button):
    """Num Label object class"""

    def __init__(self, **kwargs):
        super(NewNumberLabel, self).__init__(**kwargs)
        self.bind(on_press = self._on_press_button)

    def _on_press_button(self, touch=None):
        """ On press method for current object """
        self.state = 'normal'
        print 'pressed on number label'