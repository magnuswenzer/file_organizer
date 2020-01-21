import tkinter as tk 
from PIL import ImageTk, Image 

import gui.widgets as tkw

import gui 

from controller import Controller

class App(tk.Tk): 
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs) 

		self.protocol(u'WM_DELETE_WINDOW', self._quit_program)
		
		tk.Tk.wm_title(self, 'Python Bildvidsare') 

		self.controller = Controller(target_directory='C:/test_bilder', database_path='test_database.sqlite3')

		self._set_frame()

		self.update_frame()

	#===========================================================================
	def _quit_program(self): 

		self.destroy()  # Closes window
		self.quit()	 # Terminates program


	def _set_frame(self): 
		self.frame_main = tk.Frame(self)
		self.frame_main.grid(row=0, column=0, sticky='nsew')

		tkw.grid_configure(self) 

		self._set_frame_main()
		self._set_frame_view_picture()
		self._set_frame_tag_pictures()
		self._set_frame_add_pictures()
		self._set_frame_add_tags()

	def _set_frame_main(self):
		frame = self.frame_main
		self.widget_notebook = tkw.NotebookWidget(frame, 
												 tabs=['Bildvisning', 'Tagga bilder', 'Lägg till bilder', 'Lägg till taggar'], 
												 notebook_prop={}, 
												 row=0, 
												 column=0, 
												 sticky='nsew')
		tkw.grid_configure(frame) 

	def _set_frame_view_picture(self): 
		frame = self.widget_notebook.get_frame('Bildvisning')

		tkw.grid_configure(frame) 

	def _set_frame_tag_pictures(self):
		frame = self.widget_notebook.get_frame('Tagga bilder')

		tkw.grid_configure(frame)

	def _set_frame_add_pictures(self):
		frame = self.widget_notebook.get_frame('Lägg till bilder') 

		tkw.grid_configure(frame)

	def _set_frame_add_tags(self): 
		frame = self.widget_notebook.get_frame('Lägg till taggar')
		self.frame_add_tags = gui.FrameAddTags(frame, controller=self.controller)
		tkw.grid_configure(frame) 

	def update_frame(self):
		self.widget_notebook.select_tab('Lägg till taggar')

