Kivy Table widget v1
====================

###This is a Table widget for the [Kivy]() library.

Short example:
``` Python
...
from table import Table
...
self.my_table = Table()
self.my_table.cols = 2
self.my_table.add_button_row('123','456')
self.my_table.add_row([Button, {'text':'button2',
                                'color_widget': [0,0,0.5,1],
                                'color_click': [0,1,0,1]
                                }], 
                      [TextInput, {'text':'textinput2',
                                   'color_click': [1,0,.5,1]
                                  }])
self.my_table.choose_row(3)
self.my_table.del_row(5)
self.my_table.grid.bkcolor = [1, 0, 0, 1]
self.my_table.grid.cells[1][1].text = 'edited textinput text'
self.my_table.grid.cells[3][0].height = 100
self.my_table.label_panel.labels[0].text = 'New name'
...
```

For more information look at example file 
[example.py](https://github.com/Seg-mel/.../blob/master/example.py) 
and [API Reference](https://github.com/Seg-mel/.../wiki/API-Reference). 
The Table widget is licensed under the terms of the MIT. Please refer to the 
[LICENSE](https://github.com/Seg-mel/.../blob/master/LICENSE) file. 
Authors of the project are listed in the 
[AUTHORS](https://github.com/Seg-mel/.../blob/master/AUTHORS) file.