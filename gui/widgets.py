import tkinter as tk 
from tkinter import ttk 

from PIL import ImageTk, Image

import re

import utils


class ImageWidget(tk.Frame):

	def __init__(self, 
				 parent, 
   				 image_size=None,
				 image_height=None,
				 prop_frame={},
				 rotation_info_object=None,
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
		self.rotation_info_object = rotation_info_object
		self.showed_image = False

		self.image_size = None
		self.image_height = image_height

		if image_size:
			if type(image_size) in [int, float]:
				if image_size > 1:
					image_size = image_size / 100
				self.image_size = image_size  # In percent
			else:
				self.image_size = image_size
		if image_height:
			self.image_height = image_height

		self._set_frame()

	def _set_frame(self):

		try:
			self.main_frame.destroy()
		except:
			pass

		self.main_frame = tk.Frame(self)
		self.main_frame.grid(row=0, column=0)
		grid_configure(self)

		self.stringvar = tk.StringVar()
		self.label = tk.Label(self.main_frame, textvariable=self.stringvar)
		self.label.grid(row=0, column=0) 
		grid_configure(self.main_frame)

	def show_image(self, image_path, rotate=None):
		self.image_path = image_path
		print('=')
		print('self.showed_image', self.showed_image)
		print('image_path', image_path)

		# if not self.showed_image:
		# 	self._set_frame()
		# self.original_image = Image.open(str(self.image_path))
		# width, height = self.original_image.size
		# if type(self.image_size) == float:
		# 	self.image = self.original_image.resize((int(width * self.image_size), int(height * self.image_size)))
		# else:
		# 	self.image = self.original_image.resize((self.image_size[0], self.image_size[1]))
		# if rotate:
		# 	if self.rotation_info_object:
		# 		rotate = self.rotation_info_object.get(self.image_path.name) + rotate
		# 		self.rotation_info_object.set(self.image_path.name, rotate)
		# else:
		# 	if self.rotation_info_object:
		# 		rotate = self.rotation_info_object.get(self.image_path.name)
		# 	else:
		# 		rotate = 0
		# self.image = self.image.rotate(rotate)
		# self.tk_image = ImageTk.PhotoImage(self.image)
		# # create new label here
		# self.label.configure(image=self.tk_image)
		# self.label.image = self.tk_image
		# self.showed_image = True
		#
		# print('self.label.winfo_width', self.label.winfo_width())
		# print('self.label.winfo_height', self.label.winfo_height())
		# print('self.image.size', self.image.size)
		try:
			if not self.showed_image:
				self._set_frame()
			self.original_image = Image.open(str(self.image_path))
			self.image = self.original_image
			if rotate:
				if self.rotation_info_object:
					rotate = self.rotation_info_object.get(self.image_path.name) + rotate
					self.rotation_info_object.set(self.image_path.name, rotate)
			else:
				if self.rotation_info_object:
					rotate = self.rotation_info_object.get(self.image_path.name)
				else:
					rotate = 0
			self.image = self.image.rotate(rotate)
			width, height = self.image.size
			if self.image_height:
				new_width = int(width * self.image_height / height)
				self.image = self.original_image.resize((new_width, self.image_height))
			elif self.image_size:
				if type(self.image_size) == float:
					self.image = self.original_image.resize((int(width*self.image_size), int(height*self.image_size)))
				else:
					self.image = self.original_image.resize((self.image_size[0], self.image_size[1]))
			else:
				self.image = self.original_image

			self.image = self.image.rotate(rotate)
			self.tk_image = ImageTk.PhotoImage(self.image)
			# create new label here
			self.label.configure(image=self.tk_image)
			self.label.image = self.tk_image
			self.showed_image = True

			print('self.label.winfo_width', self.label.winfo_width())
			print('self.label.winfo_height', self.label.winfo_height())
			print('self.image.size', self.image.size)
			return True
		except Exception as e:
			# raise e
			if self.showed_image:
				self._set_frame()
			self.stringvar.set(self.image_path)
			self.image_path = None
			self.showed_image = False
			return False

	def set_size(self, size): 
		if size > 1:
			size = size / 100
		self.size = size 
		self.show_image(self.image_path)

	def rotate_left(self):
		self.show_image(self.image_path, rotate=90)

	def rotate_right(self):
		self.show_image(self.image_path, rotate=-90)


class ImageViewWidget(tk.Frame): 

	def __init__(self, 
				 parent,
				 callback_change_image=None,
				 rotation_info_object=None,
				 image_size=None,
				 image_height=None,
				 prop_frame={}, 
				 **kwargs): 

		self.callback_change_image = callback_change_image
		self.image_size = image_size
		self.image_height = image_height
		self.prop_frame = {}
		self.prop_frame.update(prop_frame)

		self.grid_frame = {'padx': 5, 
						   'pady': 5, 
						   'sticky': 'nsew'}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)

		self.rotation_info_object = rotation_info_object

		self.current_index = None  # index in image list
		self.current_image = None

		self._set_frame()

		self._set_binding_keys()

	def _set_frame(self):
		layout = dict(padx=5,
					  pady=5,
					  sticky='nsew')
		# self.stringvar_file_name = tk.StringVar()
		# tk.Label(self, textvariable=self.stringvar_file_name).grid(row=0, column=0, **layout)
		self.image_widget = ImageWidget(self,
										image_size=self.image_size,
										image_height=self.image_height,
										rotation_info_object=self.rotation_info_object,
										row=0, columnspan=3, **layout)

		self.button_previous = tk.Button(self, text='Tillbaka', command=self._previous, state='disabled')
		self.button_previous.grid(row=1, column=0, **layout)

		self.stringvar_file_nr = tk.StringVar()
		self.label_file_nr = tk.Label(self, textvariable=self.stringvar_file_nr)
		self.label_file_nr.grid(row=1, column=1, **layout)

		self.button_next = tk.Button(self, text='Nasta', command=self._next, state='disabled')
		self.button_next.grid(row=1, column=2, **layout)

		self.button_rotate_left = tk.Button(self, text='Rotera vanster', command=self._rotate_left, state='disabled')
		self.button_rotate_left.grid(row=2, column=0, **layout)

		self.button_rotate_right = tk.Button(self, text='Rotera hoger', command=self._rotate_right, state='disabled')
		self.button_rotate_right.grid(row=2, column=2, **layout)

		grid_configure(self, nr_columns=3, nr_rows=3)

	def _set_binding_keys(self):
		self.bind('<Left>', self._previous)
		self.bind('<Right>', self._next)
		self.bind('l', self._rotate_left)
		self.bind('r', self._rotate_right)

	def _update_widgets(self):
		# Set status for buttons
		self.button_previous.config(state='normal')
		self.button_next.config(state='normal')
		self.button_rotate_left.config(state='normal')
		self.button_rotate_right.config(state='normal')
		if self.current_index == 0:
			self.button_previous.config(state='disabled')
		elif self.current_index == (self.nr_files - 1):
			self.button_next.config(state='disabled')

		# Display nr files
		self.stringvar_file_nr.set(f'{self.current_index+1} / {self.nr_files}')

	def _previous(self, event=None):
		self.current_index -= 1
		self._show_image()
		self.focus_set()

	def _next(self, event=None):
		self.current_index += 1
		self._show_image()
		self.focus_set()

	def _show_image(self):
		self._update_widgets()
		# print('='*40)
		# print(str(self.image_list[self.current_index]))
		# print('-'*40)
		# print('\n'.join([str(im) for im in self.image_list[(self.current_index-2):(self.current_index+2)]]))
		self.current_image = self.image_list[self.current_index]
		ok = self.image_widget.show_image(self.current_image)
		# self.stringvar_file_name.set(self.current_image)
		if self.callback_change_image:
			if ok:
				self.callback_change_image(self.current_image, True)
			else:
				self.callback_change_image(self.current_image, False)

	def _rotate_left(self, event=None):
		self.image_widget.rotate_left()
		self.focus_set()

	def _rotate_right(self, event=None):
		self.image_widget.rotate_right()
		self.focus_set()

	def set_image_list(self, image_list):
		"""
		image_list is a list of paths.
		"""
		if self.current_index is None:
			self.current_index = 0
		else:
			current_image = self.image_list[self.current_index]
			if current_image in image_list:
				self.current_index = image_list.index(current_image)
			else:
				self.current_index = 0
		self.image_list = image_list
		self.nr_files = len(self.image_list)
		self._show_image()

	def set_image_size(self, size):
		self.image_widget.set_size(size)


class SelectTagWidget(tk.Frame):
	def __init__(self,
				 parent,
				 controller=None,
				 tag_type_names=None,
				 year_list=[],
				 prop_frame={},
				 **kwargs):

		self.tag_type_names = tag_type_names
		self.intvars = {}
		self.prop_frame = {}
		self.prop_frame.update(prop_frame)

		self.grid_frame = {'padx': 5,
						   'pady': 5,
						   'sticky': 'nsew'}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)

		self.controller = controller

		self.year_list = [str(y) for y in year_list]

		self.month_list = [str(n).zfill(2) for n in range(1, 13)]
		self.month_to_num = {}
		# for n, m in enumerate(self.month_list):
		# 	self.month_to_num[m] = n + 1

		self._set_frame()

	def _set_frame(self):
		layout = dict(padx=5,
					  pady=5,
					  sticky='nsew')

		self.tag_widget = TagWidget(self, **layout)
		self.tag_widget.update_frame(self.tag_type_names)

		self.time_frame = tk.LabelFrame(self, text='Tid')
		self.time_frame.grid(row=0, column=1, **layout)

		grid_configure(self, nr_columns=2)

		self._set_frame_time()

	def _set_frame_time(self):
		frame = self.time_frame

		layout = dict(padx=5,
					  pady=5,
					  sticky='nsew')

		tk.Label(frame, text='År').grid(row=0, column=0, **layout)
		self.stringvar_year = tk.StringVar()
		self.combobox_year = ttk.Combobox(frame, textvariable=self.stringvar_year)
		self.combobox_year.grid(row=0, column=1, **layout)
		self.combobox_year['values'] = [''] + self.year_list
		self.combobox_year.config(state='readonly')
		self.combobox_year.bind("<<ComboboxSelected>>", self._on_select_year)

		tk.Label(frame, text='Månad').grid(row=1, column=0, **layout)
		self.stringvar_month = tk.StringVar()
		self.combobox_month = ttk.Combobox(frame, textvariable=self.stringvar_month)
		self.combobox_month.grid(row=1, column=1, **layout)
		self.combobox_month.config(state='readonly')

		grid_configure(self, nr_rows=2)

	def _on_select_year(self, event=None):
		year = self.stringvar_year.get()
		month_list = self.controller.get_months_for_year(year)
		self.combobox_month['values'] = [''] + month_list

	def get_filter(self):
		selected_filter = {}
		selected_filter['tags'] = self.tag_widget.get_checked()
		if 'otaggade' in selected_filter['tags']:
			selected_filter['tags'].pop(selected_filter['tags'].index('otaggade'))
			selected_filter['otaggade'] = True
		else:
			selected_filter['otaggade'] = False

		month = self.stringvar_month.get()
		if not month:
			month = None
		# else:
		# 	month = self.month_to_num.get(month)
		selected_filter['month'] = month

		year = self.stringvar_year.get().strip()
		if not year:
			year = None
		else:
			year = int(year)
		selected_filter['year'] = year

		return selected_filter



class TagWidget(tk.Frame):
	def __init__(self,
				 parent,
				 callback=None,
				 show_untagged=True,
				 prop_frame={},
				 **kwargs):

		self.callback = callback
		self.show_untagged = show_untagged
		self.intvars = {}
		self.prop_frame = {}
		self.prop_frame.update(prop_frame)

		self.grid_frame = {'padx': 5,
						   'pady': 5,
						   'sticky': 'nsew'}
		self.grid_frame.update(kwargs)

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)

	def update_frame(self, tag_types_names):
		"""
		tag_types_names is a dict with tag type as keys and corresponding tag names as values (in a list)
		"""
		try:
			self.main_frame.destroy()
		except:
			print('Could not destroy main frame')

		layout = dict(padx=5,
					  pady=5,
					  sticky='nsew')

		self.main_frame = tk.Frame(self)
		self.main_frame.grid(row=0, column=0, **layout)

		self.frame_untagged = tk.Frame(self)
		self.frame_untagged.grid(row=1, column=0, **layout)

		grid_configure(self, nr_rows=2, r1=10)

		self.layout = dict(padx=5,
						   pady=5,
						   sticky='nsew')

		self._set_frame_main(tag_types_names)
		self._set_frame_untagged()

	def _set_frame_main(self, tag_types_names):
		r = 0
		c = 0
		self.intvars = {}
		self.labelframes = {}
		for tag_type in sorted(tag_types_names):
			self.labelframes[tag_type] = tk.LabelFrame(self.main_frame, text=tag_type.capitalize())
			self.labelframes[tag_type].grid(row=r, column=c, **self.layout)
			nr = 0
			for tag_name in tag_types_names[tag_type]:
				self.intvars[tag_name] = tk.IntVar()
				cb = tk.Checkbutton(self.labelframes[tag_type], text=tag_name.capitalize(), variable=self.intvars[tag_name],
								    command=lambda x=tag_name: self._check(x))
				cb.grid(row=nr, column=0, padx=5, sticky='w')
				nr += 1
			grid_configure(self.labelframes[tag_type], nr_columns=1, nr_rows=nr)
			r += 1
			if not r % 4:
				r = 0
				c += 1
		grid_configure(self.main_frame, nr_rows=5, nr_columns=c+1)

	def _set_frame_untagged(self):
		self.intvar_untagged = tk.IntVar()
		self.checkbutton_untagged = tk.Checkbutton(self.frame_untagged, text='Otaggade', variable=self.intvar_untagged)
		if self.show_untagged:
			self.checkbutton_untagged.grid(row=0, column=0, **self.layout)
		grid_configure(self.frame_untagged)


	def set_checked(self, tags):
		for tag, value in self.intvars.items():
			if tag in tags:
				value.set(1)
			else:
				value.set(0)

	def uncheck_all(self):
		for tag, value in self.intvars.items():
			value.set(0)

	def _check(self, tag_name):
		if not self.callback:
			return
		if self.intvars[tag_name].get():
			return self.callback(tag_name, True)
		else:
			return self.callback(tag_name, False)

	def get_checked(self):
		checked_tags = [tag_name for tag_name in self.intvars if self.intvars[tag_name].get()]
		if self.intvar_untagged.get():
			checked_tags.append('otaggade')
		return checked_tags


class FilterPopup(tk.Toplevel):

	def __init__(self, parent,
				 controller=None,
				 tag_type_names=None,
				 year_list=[],
				 callback_ok=None,
				 callback_cancel=None):
		self.controller = controller
		self.tag_type_names = tag_type_names
		self.year_list = year_list
		self.callback_ok = callback_ok
		self.callback_cancel = callback_cancel
		tk.Toplevel.__init__(self, parent)

		self.protocol('WM_DELETE_WINDOW', self._close_window)

		self._set_frame()

	def _close_window(self):
		if self.callback_cancel:
			self.callback_cancel()

	def _set_frame(self):
		layout = dict(padx=5,
					  pady=5,
					  sticky='nsew')
		self.select_tag_widget = SelectTagWidget(self,
												 controller=self.controller,
												 tag_type_names=self.tag_type_names,
												 year_list=self.year_list,
												 row=0, column=0,
												 columnspan=2,
												 **layout)

		self.button_ok = tk.Button(self, text='Valj', command=self._callback_ok)
		self.button_ok.grid(row=1, column=0, **layout)

		self.button_cancel = tk.Button(self, text='Avbryt', command=self.callback_cancel)
		self.button_cancel.grid(row=1, column=1, **layout)

	def _callback_ok(self):
		if not self.callback_ok:
			return

		selected_filter = self.select_tag_widget.get_filter()
		self.callback_ok(selected_filter)

	def callback_cancel(self):
		if not self.callback_cancel:
			return
		self.callback_cancel()



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

	def get_frame(self, tab):
		return self.tab_dict[tab]


class FileTreeviewWidget(tk.Frame):
	"""
	"""

	def __init__(self,
				 parent,
				 prop_frame={},
				 prop_listbox={},
				 columns=[],
				 data={},
				 callback=None,
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

		self.columns = columns
		self.data = data
		self.callback = callback

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)

		self._set_frame()

	def _set_frame(self):

		padx = 2
		pady = 2
		frame = tk.Frame(self)
		frame.grid(row=0, column=0, padx=padx, pady=pady, sticky='nsew')
		grid_configure(self)

		self.tree = ttk.Treeview(frame)
		self.tree.grid(row=0, column=0, padx=padx, pady=pady, sticky='nsew')
		self.tree.bind('<<TreeviewSelect>>', self._on_select)

		self.column_mapping = dict((item, f'#{i}') for i, item in enumerate(self.columns))

		self.tree['columns'] = self.columns[1:]
		for c, name in enumerate(self.columns):
			self.tree.column(self.column_mapping.get(name), width=270, minwidth=270, stretch=tk.NO)
			self.tree.heading(self.column_mapping.get(name), text=name.capitalize(), anchor='w')

		# tree["columns"] = ("one", "two", "three")
		# tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
		# tree.column("one", width=150, minwidth=150, stretch=tk.NO)
		# tree.column("two", width=400, minwidth=200)
		# tree.column("three", width=80, minwidth=50, stretch=tk.NO)

		self.items = dict()
		for year in sorted(self.data):
			iid = '-year-' + str(year)
			self.items[year] = dict()
			self.items[year]['value'] = self.tree.insert("", 1, iid=iid, text=str(year), values=(''))
			for month in sorted(self.data[year]):
				iid = '-year-month-' + str(year)+str(month)
				self.items[year][month] = dict()
				self.items[year][month]['value'] = self.tree.insert(self.items[year]['value'], 'end', iid=iid,
																	text=str(month), values=(''))
				for file_name in self.data[year][month]:
					iid = file_name
					self.items[year][month][file_name] = dict()
					self.items[year][month][file_name]['value'] = self.tree.insert(self.items[year][month]['value'],
																				   "end", iid=iid, text=file_name,
																				   values=(''))

	def _on_select(self, event=None):
		selected_files = [item for item in self.tree.selection() if not item.startswith('-year-')]
		print(selected_files)
		if self.callback:
			self.callback(selected_files)

	def get_selected(self):
		return [item for item in self.tree.selection() if not item.startswith('-year-')]

# # Level 1
# folder1=tree.insert("", 1, "", text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
# tree.insert("", 2, "", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
# # Level 2
# tree.insert(folder1, "end", "", text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
# tree.insert(folder1, "end", "", text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
# tree.insert(folder1, "end", "", text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))


class test_ListboxMultiselectWidget(tk.Frame):
	"""
	"""

	def __init__(self,
				 parent,
				 prop_frame={},
				 prop_listbox={},
				 items=[],
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

		self.items = items
		self.selected_items = []

		tk.Frame.__init__(self, parent, **self.prop_frame)
		self.grid(**self.grid_frame)

		self._set_frame()

		self.index_min = None
		self.index_max = None
		self.index_last = None


	def _set_frame(self):

		padx = 2
		pady = 2
		frame = tk.Frame(self)
		frame.grid(row=0, column=0, padx=padx, pady=pady, sticky='nsew')
		grid_configure(self)

		r = 0
		self.listbox = tk.Listbox(frame, selectmode='single', **self.prop_listbox)
		self.listbox.grid(row=r, column=0, padx=padx, pady=pady, sticky='nsew')
		self.scrollbar = ttk.Scrollbar(frame,
									   orient='vertical',
									   command=self.listbox.yview)
		self.scrollbar.grid(row=r, column=1, pady=pady, sticky='nsw')
		self.listbox.configure(yscrollcommand=self.scrollbar.set)
		self.listbox.bind('<<ListboxSelect>>', self._on_select)

		grid_configure(frame, nr_rows=1, nr_columns=2, c0=10)

	def _on_select(self, event):
		selection = self.listbox.curselection()
		clicked_index = selection[0]
		print('Clicked index ', clicked_index)

		if self.index_last is None:
			self.index_last = clicked_index

		if all([self.index_min is None, self.index_max is None]):
			self.index_min = self.index_max = clicked_index
		else:
			if clicked_index == self.index_max:
				self.index_min = self.index_max
			elif clicked_index == self.index_min:
				self.index_max = self.index_min
			elif clicked_index > self.index_min:
				self.index_max = clicked_index
			else:
				self.index_min = clicked_index

		self.listbox.selection_clear(0, u'end')
		self.listbox.update_idletasks()
		self.listbox.selection_set(self.index_min, self.index_max)
		self.selected_items = self.items[self.index_min:self.index_max+1]
		print(self.selected_items)

		self.index_last = clicked_index

	def update_items(self, items):
		self.items = items
		self._update_items()

	def _update_items(self):
		# Delete old entries
		self.listbox.delete(0, 'end')

		# Add new entries
		try:
			self.items = sorted(self.items, key=int)
		except:
			self.items = sorted(self.items)

		for item in self.items:
			self.listbox.insert('end', item)

	def get_items(self):
		return self.items[:]

	def get_selected(self):
		selection = self.listbox.curselection()
		if selection:
			index_to_pop = int(selection[0])
			return self.items[index_to_pop]


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

		r = 0
		self.listbox = tk.Listbox(frame, selectmode='single', **self.prop_listbox)
		self.listbox.grid(row=r, column=0, padx=padx, pady=pady, sticky='nsew')
		self.scrollbar = ttk.Scrollbar(frame,
									   orient='vertical',
									   command=self.listbox.yview)
		self.scrollbar.grid(row=r, column=1, pady=pady, sticky='nsw')
		self.listbox.configure(yscrollcommand=self.scrollbar.set)

		if self.include_delete_button:
			r += 1
			button_text = 'Delete'
			if type(self.include_delete_button) == str:
				button_text = self.include_delete_button
			self.button_delete = ttk.Button(frame, text=button_text, command=self._on_delete_item)
			self.button_delete.grid(row=r, column=0, padx=padx, pady=pady, sticky='w')

		grid_configure(frame, nr_rows=r + 1, nr_columns=2, c0=10)

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

	def get_selected(self):
		selection = self.listbox.curselection()
		if selection:
			index_to_pop = int(selection[0])
			return self.items[index_to_pop]

	def pop_selected(self):
		selection = self.listbox.curselection()
		if selection:
			index_to_pop = int(selection[0])
			self.items.pop(index_to_pop)
			self._update_items()


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

