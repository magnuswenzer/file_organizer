import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import gui.widgets as tkw
import utils


class FrameAddPictures(tk.Frame):

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
                      sticky='nw')

        self.button_open_folder = tk.Button(self, text='Hämta mapp', command=self._open_folder)
        self.button_open_folder.grid(row=0, column=0, **layout)

        self.stringvar_source_path = tk.StringVar()
        self.label_source_path = tk.Label(self, textvariable=self.stringvar_source_path)
        self.label_source_path.grid(row=0, column=1, **layout)

        tk.Label(self, text='Filtyper i mapp:').grid(row=1, column=0, **layout)
        self.stringvar_suffix_text = tk.StringVar()
        self.label_suffix = tk.Label(self, textvariable=self.stringvar_suffix_text)
        self.label_suffix.grid(row=1, column=1, **layout)

        tk.Label(self, text='Välj filtyp:').grid(row=2, column=0, **layout)
        self.stringvar_suffix = tk.StringVar()
        self.combobox_suffix = ttk.Combobox(self, textvariable=self.stringvar_suffix)
        self.combobox_suffix.grid(row=2, column=1, **layout)
        self.combobox_suffix.config(state='readonly')

        tk.Label(self, text='Källa:').grid(row=3, column=0, **layout)
        self.stringvar_source = tk.StringVar()
        self.entry_source = tk.Entry(self, textvariable=self.stringvar_source)
        self.entry_source.grid(row=3, column=1, **layout)

        tk.Label(self, text='Ändra år till:').grid(row=4, column=0, **layout)
        self.stringvar_year = tk.StringVar()
        self.entry_year = tk.Entry(self, textvariable=self.stringvar_year)
        self.entry_year.grid(row=4, column=1, **layout)

        self.button_add_images = tk.Button(self, text='Lägg till bilder', command=self._add_images)
        self.button_add_images.grid(row=5, column=0, columnspan=2, **layout)

        tkw.grid_configure(self, nr_rows=6, nr_columns=2)

    def _open_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.stringvar_source_path.set(folder)
        suffix_list = sorted(utils.get_file_types_in_directory_tree(folder))
        if '' in suffix_list:
            suffix_list.pop(suffix_list.index(''))
        self.stringvar_suffix_text.set(', '.join(suffix_list))
        self.combobox_suffix['values'] = suffix_list[:]

    def _add_images(self):
        source_path = self.stringvar_source_path.get()
        if not source_path:
            messagebox.showinfo('Lägg till bilder', 'Du har inte angivit någon mapp med bilder!')
            return
        source = self.stringvar_source.get().strip()
        if not source:
            messagebox.showinfo('Lägg till bilder', 'Du måste ange källa!')
            return
        suffix = self.stringvar_suffix.get().strip('.')
        if not suffix:
            messagebox.showinfo('Lägg till bilder', 'Du har inte angivit ett giltigt suffix!')
            return

        year = self.stringvar_year.get().strip()
        if not year:
            year = None
        else:
            if len(year) != 4:
                messagebox.showinfo('Lägg till bilder', 'År måste ha fyra siffror!')
                return

        self.button_add_images.config(state='disabled', bg='red')
        self.button_add_images.update_idletasks()
        self.controller.add_files(source_directory=source_path, source=source, file_suffix=suffix, change_year_to=year)
        self.button_add_images.config(state='normal', bg='green')
        self.button_add_images.update_idletasks()

        files_copied = [key for key, value in self.controller.files_copied.items() if value == 'file copied']
        files_same_size = [key for key, value in self.controller.files_copied.items() if value == 'same size']
        files_different_size = [key for key, value in self.controller.files_copied.items() if value == 'different size']
        files_not_in_db = [key for key, value in self.controller.files_copied.items() if value == 'not in db']

        if files_different_size:
            with open('files_different_size.txt', 'w') as fid:
                fid.write('\n'.join(files_different_size))

        text = [f'{len(files_copied)} filer kopierades',
                f'{len(files_same_size)} filer hade samma storlek (troligen dubletter)',
                f'{len(files_different_size)} filer hade olika storlek (kolla dessa i files_different_size.txt)',
                f'{len(files_not_in_db)} filer finns inte eller kunde inte loggas till i databasen']

        messagebox.showinfo('Lagg till bilder', '\n'.join(text))

    def update_frame(self, event=None):
        pass