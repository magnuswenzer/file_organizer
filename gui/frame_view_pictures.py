
import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import gui.widgets as tkw


class FrameViewPictures(tk.Frame):

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

        #file_list = self.controller.get_file_path_list(10)
        #print(file_list)
        #self.view_widget.set_image_list(file_list)

    def _set_frame(self):
        layout = dict(padx=5,
                      pady=5,
                      sticky='nsew')
        self.intvar_show_filter = tk.IntVar()
        self.checkbutton_show_filter = tk.Checkbutton(self, text='Visa filter', variable=self.intvar_show_filter,
                                                      command=self._on_show_filter)
        self.checkbutton_show_filter.grid(row=0, column=0, sticky='w')
        self.view_widget = tkw.ImageViewWidget(self,
                                               callback_change_image=self._on_change_image,
                                               rotation_info_object=self.controller.rotation_info_object,
                                               row=1, column=0, **layout)
        notebook_prop = {'width': 500}
        self.notebook_widget = tkw.NotebookWidget(self, tabs=['Tagga', 'Info'], notebook_prop=notebook_prop, row=1, column=1, **layout)
        self.frame_export = tk.LabelFrame(self, text='Exportera filer')
        self.frame_export.grid(row=2, column=0, columnspan=2, **layout)

        self.tag_widget = tkw.TagWidget(self.notebook_widget.get_frame('Tagga'),
                                        show_untagged=False, row=0, column=0, callback=self._on_tag_image, **layout)

        self._set_frame_export()
        self._set_frame_info()

    def _set_frame_info(self):
        frame = self.notebook_widget.get_frame('Info')
        items = ['Filnamn', 'Plats', 'Källa', 'Filtyp', 'Tid', 'År', 'Månad']
        self.info_stringvars = {}
        r = 0
        for item in items:
            tk.Label(frame, text=item).grid(row=r, column=0, sticky='w')
            self.info_stringvars[item] = tk.StringVar()
            tk.Label(frame, textvariable=self.info_stringvars[item]).grid(row=r, column=1, sticky='w')
            r += 1
        tkw.grid_configure(frame, nr_rows=r, nr_columns=2)

    def _set_frame_export(self):
        frame = self.frame_export
        self.button_get_export_directory = tk.Button(frame, text='Hamta mapp', command=self._get_export_directory)
        self.button_get_export_directory.grid(row=0, column=0, sticky='w')
        self.stringvar_export_directory = tk.StringVar()
        tk.Label(frame, textvariable=self.stringvar_export_directory).grid(row=0, column=1, sticky='w')
        self.button_export = tk.Button(frame, text='Exportera', command=self._export)
        self.button_export.grid(row=1, column=0, sticky='w')
        tkw.grid_configure(frame, nr_rows=2, nr_columns=2)

    def _get_export_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.stringvar_export_directory.set(directory)

    def _export(self):
        directory = self.stringvar_export_directory.get()
        if not directory:
            return
        if os.listdir(directory):
            if not messagebox.askyesno('Exportera filer', f"""Det finns filer i den angvinga exportmappen. 
                                                          'Vill du fortfarande exportera filerna till mapp: 
                                                          '{directory}"""):
                return
        for file_path in self.view_widget.image_list:
            target_path = Path(directory, file_path.name)
            shutil.copyfile(file_path, target_path)

    def _on_change_image(self, image_name, is_image):
        if not is_image:
            self.tag_widget.uncheck_all()
        else:
            tags = self.controller.get_tags_for_file(image_name.name)
            self.tag_widget.set_checked(tags)
        self._update_file_info(image_name)

    def _update_file_info(self, image_name):
        file_info = self.controller.get_file_info(image_name.name)
        for item in self.info_stringvars:
            self.info_stringvars[item].set(file_info.get(item, ''))

    def _on_tag_image(self, tag_name, checked):
        file_path = self.view_widget.current_image
        file_name = file_path.name
        if checked:
            self.controller.add_tag_to_file(tag_name, file_name)
        else:
            self.controller.remove_tag_from_file(tag_name, file_name)

    def _on_show_filter(self):
        if self.intvar_show_filter.get():
            tag_type_names = self.controller.get_tag_names_in_tag_types()
            self.filter_frame = tkw.FilterPopup(self,
                                                tag_type_names=tag_type_names,
                                                year_list=self.controller.get_year_list(),
                                                callback_ok=self._on_ok_filter,
                                                callback_cancel=self._on_cancel_filter)
        else:
            try:
                self.filter_frame.destroy()
            except:
                pass

    def _on_ok_filter(self, selection):

        if selection.get('otaggade'):
            file_list = self.controller.get_untagged_files()
        else:
            file_list = self.controller.get_file_list(tags=selection.get('tags'),
                                                      year=selection.get('year'),
                                                      month=selection.get('month'))
        if not file_list:
            print('return')
            return
        # Temp
        # file_list = self.controller.get_file_path_list(10)
        print('LEN', len(file_list))
        self.view_widget.set_image_list(file_list)
        self._on_cancel_filter()

    def _on_cancel_filter(self):
        self.filter_frame.destroy()
        self.intvar_show_filter.set(0)

    def update_frame(self, event=None):
        tag_types_names = self.controller.get_tag_names_in_tag_types()
        self.tag_widget.update_frame(tag_types_names)