import tkinter as tk 
from tkinter import ttk 

from PIL import ImageTk, Image

import re

class ImageWidget(tk.Frame): 

	def __init__(self, 
				 parent, 
   				 size=30, 
				 prop_frame={}, 
				 **kwargs): 

		self.prop_frame = {}
		self.prop_frame.update(prop_frame)

		self.grid_frame = {'padx': 5, 
						   'pady': 5, 
						   'sticky': 'nsew'}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)  

		self.image_path = None 
		self.original_image = None

		if size > 1:
			size = size / 100
		self.size = size  # In percent 

		self._set_frame()


	def _set_frame(self):
		self.label = tk.Label(self)
		self.label.grid(row=0, column=0) 
		grid_configure(self)

	def show_image(self, image_path):
		self.image_path = image_path 
		self.original_image = Image.open(self.image_path)
		width, height = self.original_image.size 
		self.image = self.original_image.resize((int(width*self.size), int(height*self.size)))
		self.tk_image = ImageTk.PhotoImage(self.image)
		self.label.configure(image=self.tk_image)
		self.label.image = self.tk_image

	def set_size(self, size): 
		if size > 1:
			size = size / 100
		self.size = size 
		self.show_image(self.image_path)



class ImageViewWidget(tk.Frame): 

	def __init__(self, 
				 parent, 
				 prop_frame={}, 
				 **kwargs): 

		self.prop_frame = {}
		self.prop_frame.update(prop_frame)

		self.grid_frame = {'padx': 5, 
						   'pady': 5, 
						   'sticky': 'nsew'}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)  

	def _set_frame(self):
		self.image_widget = widgets.ImageWidget(self.frame_main)


class NotebookWidget(ttk.Notebook):
	 
	def __init__(self, 
				 parent, 
				 tabs=[], 
				 notebook_prop={}, 
				 **kwargs):
		
		self.tab_list = tabs
		self.notebook_prop = {}
		self.notebook_prop.update(notebook_prop)
		
		self.grid_notebook = {'padx': 5, 
							  'pady': 5, 
							  'sticky': 'nsew'}
		self.grid_notebook.update(kwargs)
		
		ttk.Notebook.__init__(self, parent, **self.notebook_prop)
		self.grid(**self.grid_notebook)
		
		self.tab_dict = {}
		self._set_widget()
		
	
	#===========================================================================
	def _set_widget(self):
				
		for tab in self.tab_list:
			name = tab.strip('?')
			name = 'tab_' + name.lower().replace(' ', '_').replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
			notebook_frame = tk.Frame(self)
			setattr(self, name, notebook_frame)
			self.add(notebook_frame, text=tab)
			self.tab_dict[tab] = notebook_frame
			grid_configure(notebook_frame)
		grid_configure(self)		  
	
	#===========================================================================
	def select_tab(self, tab):
		if tab in self.tab_dict:
			self.select(self.tab_dict[tab])
			return True
		else:
			return False

	def get_selcted_tab(self):
		return self.tab(self.select(), "text")

	#===========================================================================
	def get_frame(self, tab):
		return self.tab_dict[tab]


class ListboxWidget(tk.Frame):
	"""
	Originally developed by me at SMHI (https://github.com/sharksmhi/sharkpylib/tree/master/sharkpylib/tklib). 
	Now modified.	  
	"""
	
	def __init__(self, 
				 parent, 
				 prop_frame={}, 
				 prop_listbox={},
				 items=[], 
				 only_unique_items=True, 
				 include_delete_button='',
				 callback_delete_button=None,  # returns the removed item
				 title='',
				 **kwargs):
		
		# Update kwargs dict
		self.prop_frame = {}
		self.prop_frame.update(prop_frame)
		
		self.prop_listbox = {'bg': 'grey'}
		self.prop_listbox.update(prop_listbox)		
		
		self.grid_frame = {'row': 0,
						   'column': 0,
						   'sticky': 'nsew',
						   'padx': 5,
						   'pady': 5}
		self.grid_frame.update(kwargs)
		
		self.title = title
		self.items = items
		self.only_unique_items = only_unique_items 
		self.include_delete_button = include_delete_button
		self.callback_delete_button = callback_delete_button

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame) 
		
		self._set_frame()
	
	def _set_frame(self):
		
		padx = 2
		pady = 2
		frame = tk.Frame(self)
		frame.grid(row=0, column=0, padx=padx, pady=pady, sticky='nsew')
		grid_configure(self) 
		
		r=0
		self.listbox = tk.Listbox(frame, selectmode='single', **self.prop_listbox)
		self.listbox.grid(row=r, column=0, padx=padx, pady=pady, sticky='nsew')
		self.scrollbar = ttk.Scrollbar(frame, 
									   orient='vertical', 
									   command=self.listbox.yview)
		self.scrollbar.grid(row=r, column=1, pady=pady, sticky='nsw')
		self.listbox.configure(yscrollcommand=self.scrollbar.set)
		
		if self.include_delete_button: 
			r+=1
			button_text = 'Delete' 
			if type(self.include_delete_button) == str:
				button_text = self.include_delete_button
			self.button_delete = ttk.Button(frame, text=button_text, command=self._on_delete_item)
			self.button_delete.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')
		
		grid_configure(frame, nr_rows=r+1, nr_columns=2, c0=10) 
		
	def add_item(self, item):
		self.items.append(item) 
		self._update_items()
		
	def remove_item(self, item):
		if item in self.items:
			self.items.remove(item)
		self._update_items()
		
	def _on_delete_item(self, event=None): 
		selection = self.listbox.curselection()
		if selection:
			index_to_pop = int(selection[0])
			item = self.items[index_to_pop]
			self.items.pop(index_to_pop) 
			self._update_items()
			if self.callback_delete_button:
				self.callback_delete_button(item)
		
	def update_items(self, items):
		self.items = items
		self._update_items()
	
	def _update_items(self): 
		# Delete old entries
		self.listbox.delete(0, 'end')
		
		if self.only_unique_items:
			self.items = list(set(self.items))
		# Add new entries
		try:
			self.items = sorted(self.items, key=int)
		except:
			self.items = sorted(self.items)
			
		for item in self.items:  
			self.listbox.insert('end', item)

	def get_items(self):
		return self.items[:]


class ListboxSelectionWidget(tk.Frame):
	"""
	Frame to hold widgets for series selection. 
	The class is a frame containing all series selection widgets sepcified in init. 
	Originally developed by me at SMHI (https://github.com/sharksmhi/sharkpylib/tree/master/sharkpylib/tklib). 
	Now modified.
	"""
	
	def __init__(self, 
				 parent, 
				 prop_frame={}, 
				 prop_items={},
				 prop_selected={}, 
				 items=[], 
				 selected_items=[], 
				 title_items='',
				 title_selected='', 
				 font=None, 
				 include_button_move_all_items=True, 
				 include_button_move_all_selected=True, 
				 callback_match_in_file=None, 
				 callback_match_subselection=None,
				 callback_set_default=None,
				 sort_selected=False, 
				 include_blank_item=False, 
				 target=None,
				 target_select=None,
				 target_deselect=None, 
				 bind_tab_entry_items=None, 
				 widget_id='', 
				 allow_nr_selected=None, 
				 vertical=False,
				 search_case_sensitive=True,
				 **kwargs):
		
		# Update kwargs dict
		self.prop_frame = {}
		self.prop_frame.update(prop_frame)
		
		self.prop_listbox_items = {'bg': 'grey',
								   'width': 30,
								   'height': 10}
		self.prop_listbox_items.update(prop_items)
		
		self.prop_listbox_selected = {'width': 30,
									  'height': 10}
		self.prop_listbox_selected.update(prop_selected)
		
		
		self.grid_frame = {'row': 0,
						   'column': 0,
						   'sticky': 'nsew',
						   'padx': 5,
						   'pady': 5}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)
		
		self.sort_selected = sort_selected
		self.title_items = title_items
		self.title_selected = title_selected
		self.items = items[:] # List of items to choose from. Copy of list here is very important!
		self.selected_items = selected_items[:] # Copy of list here is very important!
		self.widget_id = widget_id
		self.bind_tab_entry_items = bind_tab_entry_items
		self.allow_nr_selected = allow_nr_selected
		self.vertical = vertical 
		self.search_case_sensitive = search_case_sensitive

		self.include_button_move_all_items = include_button_move_all_items
		self.include_button_move_all_selected = include_button_move_all_selected
		
		self.callback_match_in_file = callback_match_in_file
		self.callback_match_subselection = callback_match_subselection
		self.callback_set_default = callback_set_default
		
		if isinstance(target, list):
			self.targets = target
		elif not target:
			self.targets = []
		else:
			self.targets = [target]
			
		self.target_select = target_select
		self.target_deselect = target_deselect
		self.include_blank_item = include_blank_item
		
		# Swich to False if item is selected (moved to selected) or deselected (moved to items)
		# This is so that the right target can be called
		self.last_move_is_selected = True 
		
		if font:
			self.font = font
		else:
			self.font = Fonts().fontsize_medium
		
		self._remove_selected_items_from_items()
		self._set_frame()

		self._update_listboxes(update_targets=False)
		
	#===========================================================================
	def _set_frame(self):
		
		padx = 5
		pady = 2
		
		self.frame_items = tk.Frame(self)
		self.frame_selected = tk.Frame(self)
		self.frame_buttons = tk.Frame(self)
		
		button_r=1
		c = 0
		self.frame_items.grid(row=0, column=c, sticky='nw')
		if self.vertical:
			self.frame_selected.grid(row=1, column=c, sticky='nw')
			button_r += 1
		else:
			c+=1
			self.frame_selected.grid(row=0, column=c, sticky='nw')

			self.frame_buttons.grid(row=button_r, column=0, sticky='nw')

		grid_configure(self, nr_rows=button_r+1, nr_columns=c+1)

		self._set_frame_items()
		self._set_frame_selected()
		self._set_frame_buttons()

	def _set_frame_items(self):
		frame = self.frame_items
		padx = 5
		pady = 2

		r = 0
		if self.title_items:
			tk.Label(frame, text=self.title_items).grid(row=0, column=0)
			r+=1 
			
		self.listbox_items = tk.Listbox(frame, selectmode='single', font=self.font, **self.prop_listbox_items)
		self.listbox_items.grid(row=r, column=0, columnspan=2,
								 sticky=u'nsew', padx=(padx, 0), pady=pady)
		self.scrollbar_items = ttk.Scrollbar(frame,
											  orient='vertical', 
											  command=self.listbox_items.yview)
		self.scrollbar_items.grid(row=r, column=2, sticky='ns')
		self.listbox_items.configure(yscrollcommand=self.scrollbar_items.set)
		self.listbox_items.bind('<<ListboxSelect>>', self._on_click_items)
		self.listbox_items.bind('<Double-Button-1>', self._on_doubleclick_items)
		r+=1
		
		# Search field items
		self.stringvar_items = tk.StringVar()
		self.entry_items = tk.Entry(frame,
									textvariable=self.stringvar_items, 
									width=self.prop_listbox_items['width'], 
									state=u'normal')
		self.entry_items.grid(row=r, column=0, columnspan=2, sticky='e')
		self.stringvar_items.trace('w', self._search_item)
		self.entry_items.bind('<Return>', self._on_return_entry_items)
		self.entry_items.bind('<Tab>', self._on_tab_entry_items)
		r+=1
		
		# Information about number of items in list
		self.stringvar_nr_items = tk.StringVar()
		tk.Label(frame, textvariable=self.stringvar_nr_items, font=Fonts().fontsize_small).grid(row=r, column=1, sticky='e')
		
		
		if self.include_button_move_all_items:
			self.button_move_all_items = tk.Button(frame, text='Select all', command=self.select_all, font=Fonts().fontsize_small)
			self.button_move_all_items.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')
			r+=1

		grid_configure(frame, nr_rows=r, nr_columns=3, r0=10)

	def _set_frame_selected(self):
		frame = self.frame_selected
		padx = 5
		pady = 2

		r = 0
		if self.title_selected:
			tk.Label(frame, text=self.title_selected).grid(row=r, column=0)
			r+=1 
			
		self.listbox_selected = tk.Listbox(frame, selectmode='single', font=self.font, **self.prop_listbox_selected)
		self.listbox_selected.grid(row=r, column=0, columnspan=2,
								 sticky='nsew', padx=(padx, 0), pady=pady)
		self.scrollbar_selected = ttk.Scrollbar(frame,
											  orient='vertical',
											  command=self.listbox_selected.yview)
		self.scrollbar_selected.grid(row=r, column=2, sticky='ns')
		self.listbox_selected.configure(yscrollcommand=self.scrollbar_selected.set)
	#		 Hover(self.listbox_series, text=HelpTexts().listbox_seriesinformation, controller=self.controller)
		self.listbox_selected.bind('<<ListboxSelect>>', self._on_click_selected)
		self.listbox_selected.bind('<Double-Button-1>', self._on_doubleclick_selected)
		r+=1
		
		# Search field selected
		self.stringvar_selected = tk.StringVar()
		self.entry_selected = tk.Entry(frame,
									textvariable=self.stringvar_selected, 
									width=self.prop_listbox_selected['width'], 
									state='normal')
		self.entry_selected.grid(row=r, column=0, columnspan=2, sticky='e')
		self.stringvar_selected.trace('w', self._search_selected)
		self.entry_selected.bind('<Return>', self._on_return_entry_selected)
		r+=1
		
		# Information about number of items in list
		self.stringvar_nr_selected_items = tk.StringVar()
		tk.Label(frame, textvariable=self.stringvar_nr_selected_items, font=Fonts().fontsize_small).grid(row=r, column=1, sticky='e')
		
		if self.include_button_move_all_selected:
			self.button_move_all_selected = tk.Button(frame, text='Deselect all', command=self.deselect_all, font=Fonts().fontsize_small)
			self.button_move_all_selected.grid(row=r, column=0, pady=pady, sticky='w')
			r+=1

		grid_configure(frame, nr_rows=r, nr_columns=3, r0=10)

	def _set_frame_buttons(self):
		frame = self.frame_buttons
		padx = 5
		pady = 2

		r = 0
		if self.callback_match_in_file:
			self.button_match_in_file = tk.Button(frame, text='Match in file', command=self.callback_match_in_file, font=Fonts().fontsize_small)
			self.button_match_in_file.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')
			r += 1

		if self.callback_match_subselection:
			self.button_match_subselection = tk.Button(frame, text='Match subselection', command=self.callback_match_subselection, font=Fonts().fontsize_small)
			self.button_match_subselection.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')
			r += 1

		if self.callback_set_default:
			self.button_select_default = tk.Button(frame, text='Select default',
													   command=self.callback_set_default,
													   font=Fonts().fontsize_small)
			self.button_select_default.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')
			r += 1

		grid_configure(frame, nr_rows=r)
	
	def _on_tab_entry_items(self, event):
		if self.bind_tab_entry_items:
			self.bind_tab_entry_items()
		
	def _remove_selected_items_from_items(self):
		for selected in self.selected_items:
			if selected in self.items:
				self.items.pop(self.items.index(selected))
		
	def add_target(self, target):
		self.targets.append(target)
		
	def select_all(self):
		self.selected_items.extend(self.items)
		self.items = []
		self.stringvar_items.set('')
		self._update_listboxes()
	
	def deselect_all(self):
		self.items.extend(self.selected_items)
		self.selected_items = []
		self.stringvar_selected.set('')
		self._update_listboxes()
	
	def delete_selected(self):
		self.selected_items = []
		self.last_move_is_selected = False
		self._update_listboxes()
		
	def clear_lists(self):
		self.update_items()
		
	def add_items(self, items, move_to_selected=False):
		""" 
		Add items to self.items. 
		If "move_to_selected"=True the items are moved to selected. 
		"""  
		for item in items:
			# First check if item already present
			if item in self.items or item in self.selected_items:
				continue
			self.items.append(item)
		
		if move_to_selected:
			self.move_items_to_selected(items)
			
		self._update_listboxes(update_targets=False)
		
	def delete_items(self, items):
		""" Deletes items from widget """
		for item in items:
			if item in self.items:
				self.items.pop(self.items.index(item))
			elif item in self.selected_items:
				self.selected_items.pop(self.selected_items.index(item))
		self._update_listboxes(update_targets=False)
			
	def update_items(self, items=[], keep_selected=False):
		""" 
		Resets the listbox and updates it with given items. 
		If no items are given, all items in widget will be removed. 
		If "keep_selected"==True selected items will be still selected if they belong to the new item list.
		"""
		selected_items = self.get_selected()
		self.items = items[:]
		self.selected_items = []
		self._update_listboxes(update_targets=False)
		
		if keep_selected:
			self.move_items_to_selected(selected_items, update_targets=False)
		
	def _move_to_selected(self, item=None, index=None):
		""" Moves given item from self.items to self.selected_items list if allowed by self.allow_nr_selected """
		if item and item not in self.items:
			return
		
		if item != None:
			i = self.items.index(item)
		elif index != None:
			i = index
		
		if not self.allow_nr_selected or len(self.selected_items) < int(self.allow_nr_selected):
			selected_item = self.items.pop(i)
			self.selected_items.append(selected_item)
		else:
			# Replace the last item in self.selected_items 
			item = self.selected_items.pop(-1)
			self.items.append(item)
			
			selected_item = self.items.pop(i)
			self.selected_items.append(selected_item)
		
		
	def move_items_to_selected(self, items, update_targets=False):
		if type(items) != list:
			items = [items]
		for item in items:
			if item in self.items:
				self._move_to_selected(item=item)
		self._update_listboxes(update_targets=update_targets)
		
	def move_selected_to_items(self, items, update_targets=False):
		if type(items) != list:
			items = [items]
		for item in items:
			if item in self.selected_items:
				self.items.append(self.selected_items.pop(self.selected_items.index(item)))
		self._update_listboxes(update_targets=update_targets)

	def _update_listboxes(self, update_targets=True):
		self._update_listbox_items()
		self._update_listbox_selected()  
		
		# Update number of items
		nr_items = '%s items' % len(self.items)
		nr_selected_items = '%s items' % len(self.selected_items)
		self.stringvar_nr_items.set(nr_items)
		self.stringvar_nr_selected_items.set(nr_selected_items)
		
		if update_targets:
			if self.targets:
				for target in self.targets:
					target()
			
			if self.target_select and self.last_move_is_selected:
				self.target_select() 
				 
			if self.target_deselect and not self.last_move_is_selected:
				self.target_deselect()
		
	def _search_item(self, *dummy):
		self.listbox_items.selection_clear(0, u'end')
		search_string = self.stringvar_items.get()
		if not self.search_case_sensitive:
			search_string = search_string.lower()
			
		# print(search_string)
		index = []
		for i, item in enumerate(self.items):
			if not self.search_case_sensitive:
				item = item.lower()
			if search_string and item.startswith(search_string):
				index.append(i)
		if index:
			# print(index)
			self.listbox_items.selection_set(index[0], index[-1])
			self.listbox_items.see(index[0])
		
	def _search_selected(self, *dummy):
		self.listbox_selected.selection_clear(0, u'end')
		search_string = self.stringvar_selected.get()
		if not self.search_case_sensitive:
			search_string = search_string.lower()
		index = []
		for i, item in enumerate(self.selected_items):
			if not self.search_case_sensitive:
				item = item.lower()
			if search_string and item.startswith(search_string):
				index.append(i)
		if index: 
			self.listbox_selected.selection_set(index[0], index[-1])
			self.listbox_selected.see(index[0])

	def _on_return_entry_items(self, event):
		search_string = self.stringvar_items.get().lower()
		index = []
		for i, item in enumerate(self.items):
			if search_string and item.lower().startswith(search_string):
				index.append(i)
		if len(index) >= 1:
			for i in index[::-1]:
				self._move_to_selected(index=i)
			self.last_move_is_selected = True
			self._update_listboxes()
			self.stringvar_items.set(u'')
		
	def _on_return_entry_selected(self, event):
		search_string = self.stringvar_selected.get().lower()
		index = []
		for i, item in enumerate(self.selected_items):
			if search_string and item.lower().startswith(search_string):
				index.append(i)
		if len(index) >= 1:
			for i in index[::-1]:
				selected_item = self.selected_items.pop(i)
				self.items.append(selected_item)
			self.last_move_is_selected = False
			self._update_listboxes()
			self.stringvar_selected.set('')
		
	def _on_click_items(self, event):
		selection = self.listbox_items.curselection()
		if selection:
			self.stringvar_items.set(self.listbox_items.get(selection[0]))
			
	def _on_click_selected(self, event):
		selection = self.listbox_selected.curselection()
		if selection:
			self.stringvar_selected.set(self.listbox_selected.get(selection[0]))
			   
	def _on_doubleclick_items(self, event):
		selection = self.listbox_items.curselection()
		if selection:
			index_to_pop = int(selection[0])
			self._move_to_selected(index=index_to_pop)
			self.last_move_is_selected = True
			self._update_listboxes()
			self.stringvar_items.set('')
			self.listbox_items.see(max(0, index_to_pop))
	
	def _on_doubleclick_selected(self, event):
		selection = self.listbox_selected.curselection()
		if selection:
			index_to_pop = int(selection[0])
			selected_item = self.selected_items.pop(index_to_pop)
			if selected_item != '<blank>':
				self.items.append(selected_item)
			self.last_move_is_selected = False
			self._update_listboxes()
			self.stringvar_selected.set('')
			self.listbox_items.see(max(0, index_to_pop))
	
	def _update_listbox_items(self): 
		# Delete old entries
		self.listbox_items.delete(0, u'end')
		# Add new entries
		try:
			self.items = sorted(self.items, key=int)
		except:
			self.items = sorted(self.items)
			
		if self.include_blank_item: 
			if u'<blank>' in self.items:
				self.items.pop(self.items.index('<blank>'))
			self.items = ['<blank>'] + self.items 
		for item in self.items:  
			self.listbox_items.insert('end', item) 
	
	def _update_listbox_selected(self): 
		# Delete old entries
		self.listbox_selected.delete(0, u'end')
		# Add new entries
		if self.sort_selected:
			try:
				self.selected_items = sorted(self.selected_items, key=int)
			except:
				self.selected_items = sorted(self.selected_items)
		for item in self.selected_items:
			self.listbox_selected.insert('end', item)  
	 
	def get_items(self):
		return self.items[:]

	def get_value(self):
		"""
		returns selected items as a list.
		:return:
		"""
		return self.get_selected()

	def set_value(self, values, **kwargs):
		"""
		First deselect all. Then moves "values" to selected.
		:return:
		"""
		self.deselect_all()
		self.move_items_to_selected(values, **kwargs)
		 
	def get_selected(self):
		return self.selected_items[:]   
		 
	def get_all_items(self):
		return sorted(self.get_items() + self.get_selected())

	def set_prop_items(self, **prop):
		self.listbox_items.config(**prop)
		
	def set_prop_selected(self, **prop):
		self.listbox_selected.config(**prop)
		

def grid_configure(frame, nr_rows=1, nr_columns=1, **kwargs):
	""" 
	Created by me originaly for SMHI (https://github.com/sharksmhi/sharkpylib/tree/master/sharkpylib/tklib). 
	
	Put weighting on the given tkinter widget. Put weighting on the number of rows and columns given. 
	kwargs with tag "row"(r) or "columns"(c) sets the number in tag as weighting. 
	Example: 
		c1=2 sets frame.grid_columnconfigure(1, weight=2)
	"""
	row_weight = {}
	col_weight = {}
	
	# Get information from kwargs 
	for key, value in kwargs.items():
		rc = int(re.findall('\d+', key)[0])
		if 'r' in key:
			row_weight[rc] = value
		elif 'c' in key:
			col_weight[rc] = value 
					  
	# Set weight 
	for r in range(nr_rows): 
		frame.grid_rowconfigure(r, weight=row_weight.get(r, 1))
		
	for c in range(nr_columns):
		frame.grid_columnconfigure(c, weight=col_weight.get(c, 1))

