import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

		self.bind("<Visibility>", self.update_frame)

		self.update_frame()
	
	def _set_frame(self): 

		layout = dict(padx=5, 
				  	  pady=5, 
				  	  sticky='nsew') 

		self.frame_tag_type = tk.LabelFrame(self, text='Typer')
		self.frame_tag_type.grid(row=0, column=0, **layout) 

		self.frame_tag_name = tk.LabelFrame(self, text='Namn')
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


		self.stringvar_add_tag_type = tk.StringVar()
		self.entry_add_tag_type = tk.Entry(frame, textvariable=self.stringvar_add_tag_type)
		self.entry_add_tag_type.grid(row=1, column=0, **layout)
		self.entry_add_tag_type.bind('<Return>', self._add_tag_type)

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

		self.stringvar_type_for_name = tk.StringVar()
		self.combobox_add_tag_name = ttk.Combobox(frame, textvariable=self.stringvar_type_for_name)
		self.combobox_add_tag_name.grid(row=1, column=0, **layout)
		self.combobox_add_tag_name.config(state='readonly')

		self.stringvar_add_tag_name = tk.StringVar()
		self.entry_add_tag_name = tk.Entry(frame, textvariable=self.stringvar_add_tag_name)
		self.entry_add_tag_name.grid(row=2, column=0, **layout)
		self.entry_add_tag_name.bind('<Return>', self._add_tag_name)

		self.button_add_tag_name = tk.Button(frame, text='Lägg till tag', command=self._add_tag_name)
		self.button_add_tag_name.grid(row=3, column=0, **layout)

		self.button_remove_tag_name = tk.Button(frame, text='Ta bort tag', command=self._remove_tag_name)
		self.button_remove_tag_name.grid(row=3, column=1, **layout)

		tkw.grid_configure(frame, nr_rows=4, nr_columns=2, r0=20, r2=20)

	def _add_tag_type(self, event=None):
		tag_type = self.stringvar_add_tag_type.get().lower()
		if not tag_type:
			messagebox.showinfo(title='Lagg till taggtyp', message='Ange namn pa ny tagg!')
			return
		tag_type_list = self.controller.get_tag_type_list()
		if tag_type in tag_type_list:
			messagebox.showinfo(title='Lagg till taggtyp', message='Taggtypen finns redan')
			self.stringvar_add_tag_type.set('')
			return
		self.controller.add_tag_type(tag_type)
		self._update_widgets()


	def _add_tag_name(self, event=None):
		tag_name = self.stringvar_add_tag_name.get().lower()
		if not tag_name:
			messagebox.showinfo(title='Lagg till taggnamn', message='Ange namn pa ny tagg!')
			return
		tag_name_list = self.controller.get_tag_name_list()
		if tag_name in tag_name_list:
			messagebox.showinfo(title='Lagg till tagnamn', message='Taggtypen finns redan')
			self.stringvar_add_tag_name.set('')
			return
		tag_type = self.stringvar_type_for_name.get()
		self.controller.add_tag_name(tag_name, tag_type)
		self._update_widgets()

	def _remove_tag_type(self): 
		selected_item = self.widget_tag_types.get_selected()
		if not selected_item:
			return
		answer = messagebox.askyesno(title='Ta bort taggtyp', message=f'Ar du saker pa att du vill ta bort tag "{selected_item}"?')
		if not answer:
			return
		self.widget_tag_types.pop_selected()
		self.controller.remove_tag_type(selected_item)
		self._update_widgets()

	def _remove_tag_name(self):
		selected_item = self.widget_tag_names.get_selected()
		if not selected_item:
			return
		tag_name = selected_item.split(':')[-1].strip()
		answer = messagebox.askyesno(title='Ta bort taggnamn',
									 message=f'Ar du saker pa att du vill ta bort tag "{tag_name}"?')
		if not answer:
			return
		self.widget_tag_names.pop_selected()
		self.controller.remove_tag_name(tag_name)
		self._update_widgets()

	def update_frame(self, event=None):
		self._update_widgets() 

	def _update_widgets(self): 
		self._update_widgets_tag_type()
		self._update_widgets_tag_name()
		self._update_combobox_add_tag_name()
		self._clear_entries()

	def _clear_entries(self):
		self.stringvar_add_tag_type.set('')
		self.stringvar_add_tag_name.set('')

	def _update_widgets_tag_type(self):
		tag_type_list = sorted(self.controller.get_tag_type_list())
		self.widget_tag_types.update_items(tag_type_list)

	def _update_widgets_tag_name(self): 
		item_list = []
		for tag_type in sorted(self.controller.get_tag_type_list()): 
			for tag_name in sorted(self.controller.get_tag_name_list(tag_type)): 
				item_list.append(f'{tag_type.ljust(30)}: {tag_name}')
		self.widget_tag_names.update_items(item_list)

	def _update_combobox_add_tag_name(self):
		# Get updated list
		new_list = sorted(self.controller.get_tag_type_list())
		if len(new_list) == 0:
			return

		# Find selected item
		selected_item = self.stringvar_type_for_name.get()
		self.combobox_add_tag_name['values'] = new_list

		if selected_item in new_list:
			self.stringvar_type_for_name.set(selected_item)
		else:
			self.stringvar_type_for_name.set(new_list[0])

