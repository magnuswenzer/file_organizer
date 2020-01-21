import tkinter as tk
from tkinter import ttk

import gui.widgets as tkw


class FrameAddTags(tk.Frame): 

	def __init__(self, 
				 parent, 
				 controller=None, 
				 prop_frame={}, 
				 **kwargs):  
		self.controller = controller
		self.prop_frame = {} 
		self.prop_frame.update(prop_frame)	
		
		self.grid_frame = {'row': 0,
						   'column': 0,
						   'sticky': 'nsew',
						   'padx': 5,
						   'pady': 5}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame) 
		
		self._set_frame()

		self.update_frame()
	
	def _set_frame(self): 

		layout = dict(padx=5, 
				  	  pady=5, 
				  	  sticky='nsew') 

		self.frame_tag_type = tk.LabelFrame(self, text='Tag-typer') 
		self.frame_tag_type.grid(row=0, column=0, **layout) 

		self.frame_tag_name = tk.LabelFrame(self, text='Tag-namn') 
		self.frame_tag_name.grid(row=0, column=1, **layout)

		tkw.grid_configure(self, nr_columns=2)

		self._set_frame_tag_type()
		self._set_frame_tag_name()

	def _set_frame_tag_type(self): 
		frame = self.frame_tag_type

		layout = dict(padx=5, 
				  	  pady=5, 
				  	  sticky='nsew') 

		self.widget_tag_types = tkw.ListboxWidget(frame, 
												 prop_frame={}, 
												 prop_listbox={},
												 items=[], 
												 only_unique_items=True, 
												 include_delete_button='',
												 callback_delete_button=None,  # returns the removed item
												 title='', 
												 row=0, 
												 column=0, 
												 columnspan=2, 
												 **layout) 

		self.entry_add_tag_type = tk.Entry(frame)
		self.entry_add_tag_type.grid(row=1, column=0, **layout)

		self.button_add_tag_type = tk.Button(frame, text='Lägg till tag', command=self._add_tag_type)
		self.button_add_tag_type.grid(row=2, column=0, **layout)

		self.button_remove_tag_type = tk.Button(frame, text='Ta bort tag', command=self._remove_tag_type)
		self.button_remove_tag_type.grid(row=2, column=1, **layout)

		tkw.grid_configure(frame, nr_rows=3, nr_columns=2, r0=20, r2=20)

	def _set_frame_tag_name(self): 
		frame = self.frame_tag_name

		layout = dict(padx=5, 
				  	  pady=5, 
				  	  sticky='nsew') 

		self.widget_tag_names = tkw.ListboxWidget(frame, 
												  prop_frame={}, 
												  prop_listbox={},
												  items=[], 
												  only_unique_items=True, 
												  include_delete_button='',
												  callback_delete_button=None,  # returns the removed item
												  title='', 
												  row=0, 
												  column=0, 
												  columnspan=2, 
												  **layout) 

		self.entry_add_tag_name = tk.Entry(frame)
		self.entry_add_tag_name.grid(row=1, column=0, **layout)

		self.button_add_tag_name = tk.Button(frame, text='Lägg till tag', command=self._add_tag_name)
		self.button_add_tag_name.grid(row=2, column=0, **layout)

		self.button_remove_tag_name = tk.Button(frame, text='Ta bort tag', command=self._remove_tag_name)
		self.button_remove_tag_name.grid(row=2, column=1, **layout)

		tkw.grid_configure(frame, nr_rows=3, nr_columns=2, r0=20, r2=20) 

	def _add_tag_type(self): 
		pass 

	def _add_tag_name(self): 
		pass

	def _remove_tag_type(self): 
		pass 

	def _remove_tag_name(self):
		pass

	def update_frame(self): 
		self._update_widgets() 

	def _update_widgets(self): 
		self._update_widgets_tag_type()
		self._update_widgets_tag_name() 

	def _update_widgets_tag_type(self):
		tag_type_list = sorted(self.controller.get_tag_type_list())
		self.widget_tag_types.update_items(tag_type_list)

	def _update_widgets_tag_name(self): 
		item_list = []
		for tag_type in sorted(self.controller.get_tag_type_list()): 
			for tag_name in sorted(self.controller.get_tag_name_list(tag_type)): 
				item_list.append(f'{tag_type.ljust(30)}: {tag_name}')
		self.widget_tag_names.update_items(item_list)


