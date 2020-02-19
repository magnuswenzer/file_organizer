import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image 
import socket

import gui.widgets as tkw

import gui 

from controller import Controller, Databases

class App(tk.Tk): 
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs) 

		self.protocol('WM_DELETE_WINDOW', self._quit_program)
		
		tk.Tk.wm_title(self, 'Python Bildvidsare')
		print('socket.gethostname()', socket.gethostname())

		self.database_name = None
		self.location = None

		self.databases = Databases()
		self.controller = Controller()

		self._show_start_window()
		self._update_popup_start_window()
		self._on_select_db()

	def _show_start_window(self):
		self.window_select_db = tk.Frame(self)
		self.window_select_db.grid(sticky='nsew')
		tkw.grid_configure(self)


		layout = dict(padx=5,
					  pady=5,
					  sticky='nw')

		tk.Label(self.window_select_db, text='Databasnamn:').grid(row=0, column=0, **layout)
		self.stringvar_db = tk.StringVar()
		self.combobox_db = ttk.Combobox(self.window_select_db, textvariable=self.stringvar_db)
		self.combobox_db.grid(row=0, column=1, **layout)
		self.combobox_db.config(state='readonly')
		self.combobox_db.bind("<<ComboboxSelected>>", self._on_select_db)
		self.button_ok = tk.Button(self.window_select_db, text='Valj',
								   command=self._on_ok_start_window)
		self.button_ok.grid(row=0, column=2, **layout)

		self.button_get_location = tk.Button(self.window_select_db, text='Plats',
												 command=self._get_location)
		self.button_get_location.grid(row=1, column=0, **layout)
		self.stringvar_location = tk.StringVar()
		tk.Label(self.window_select_db, textvariable=self.stringvar_location).grid(row=1, column=1, **layout)

		self.labelframe_add_db = tk.LabelFrame(self.window_select_db, text='Lagg till databas')
		self.labelframe_add_db.grid(row=2, column=0, columnspan=2, **layout)

		tk.Label(self.labelframe_add_db, text='Databasnamn').grid(row=0, column=0, **layout)
		self.stringvar_new_db = tk.StringVar()
		self.entry_new_db = tk.Entry(self.labelframe_add_db, textvariable=self.stringvar_new_db)
		self.entry_new_db.grid(row=0, column=1, **layout)

		self.button_add_new_db = tk.Button(self.labelframe_add_db, text='Lagg till db',
												 command=self._add_new_db)
		self.button_add_new_db.grid(row=2, column=1, **layout)

		#self.window_select_db.grab_set()

		# self.window_select_db.lift()
		# self.window_select_db.focus_force()
		# self.window_select_db.grab_set()
		# self.window_select_db.grab_release()

	def _add_new_db(self):
		db_name = self.stringvar_new_db.get().strip()
		if not db_name:
			messagebox.showinfo('Skapa databas', 'Du maste ange ett databasnamn')
			return
		db_name = db_name.split('.')[0] + '.sqlite3'
		self.stringvar_new_db.set('')
		self.databases.new(db_name, '')
		self._update_popup_start_window()
		self.stringvar_db.set(db_name)
		self._on_select_db()

	def _get_location(self):
		folder = filedialog.askdirectory()
		if not folder:
			return
		self.databases.set_location(self.stringvar_db.get(), folder)
		self._on_select_db()

	def _on_select_db(self, event=None):
		current_db = self.stringvar_db.get().strip()
		self.stringvar_location.set(self.databases.get_location(current_db))

	def _update_popup_start_window(self):
		all_db = self.databases.get_all()
		self.combobox_db['values'] = sorted(all_db)

	def _on_ok_start_window(self):
		db_name = self.stringvar_db.get().strip()
		location = self.stringvar_location.get().strip()
		if not all([db_name, location]):
			messagebox.showinfo('Valj databas', 'Du har inte angett nagon databas')
			return
		self.database_name = db_name
		print(self.database_name)
		self.location = location
		self.controller.set_database(db_name, location)
		self.window_select_db.destroy()
		self._set_frame()
		self.update_app()

	def _quit_program(self):

		self.destroy()  # Closes window
		self.quit()	 # Terminates program

	def _set_frame(self): 
		self.frame_main = tk.Frame(self)
		self.frame_main.grid(row=0, column=0, sticky='nsew')

		tkw.grid_configure(self) 

		self._set_frame_main()
		self._set_frame_view_pictures()
		self._set_frame_tag_pictures()
		self._set_frame_add_pictures()
		self._set_frame_add_tags()
		self._set_frame_info()

	def _set_frame_main(self):
		frame = self.frame_main
		self.widget_notebook = tkw.NotebookWidget(frame, 
												 tabs=['Bildvisning', 'Tagga bilder', 'Lägg till bilder', 'Lägg till taggar', 'Info'],
												 notebook_prop={}, 
												 row=0, 
												 column=0, 
												 sticky='nsew')
		tkw.grid_configure(frame) 

	def _set_frame_view_pictures(self):
		frame = self.widget_notebook.get_frame('Bildvisning')
		self.frame_view_pictures = gui.FrameViewPictures(frame, controller=self.controller)
		tkw.grid_configure(frame) 

	def _set_frame_tag_pictures(self):
		frame = self.widget_notebook.get_frame('Tagga bilder')
		self.frame_tag_pictures = gui.FrameTagPictures(frame, controller=self.controller)
		tkw.grid_configure(frame)

	def _set_frame_add_pictures(self):
		frame = self.widget_notebook.get_frame('Lägg till bilder')
		self.frame_add_pictures = gui.FrameAddPictures(frame, controller=self.controller)
		tkw.grid_configure(frame)

	def _set_frame_add_tags(self): 
		frame = self.widget_notebook.get_frame('Lägg till taggar')
		self.frame_add_tags = gui.FrameAddTags(frame, controller=self.controller)
		tkw.grid_configure(frame)

	def _set_frame_info(self):
		frame = self.widget_notebook.get_frame('Info')
		layout = dict(padx=5,
					 pady=5,
					 sticky='nw')
		tk.Label(frame, text='Databasnamn:').grid(row=0, column=0, **layout)
		tk.Label(frame, text=self.database_name).grid(row=0, column=1, **layout)
		tk.Label(frame, text='Plats:').grid(row=1, column=0, **layout)
		tk.Label(frame, text=self.location).grid(row=1, column=1, **layout)

	def update_app(self):
		self.frame_view_pictures.update_frame()
		self.widget_notebook.select_tab('Tagga bilder')

