import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import gui.widgets as tkw
from PIL import ImageTk, Image

class FrameTagPictures(tk.Frame):

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

        self.image_from = None
        self.image_to = None

        self._set_frame()

        self.bind("<Visibility>", self.update_frame)

        self.update_frame()

    def _set_frame(self):
        layout = dict(padx=5,
                      pady=5,
                      sticky='nsew')
        self.columns = ['namn']
        data = self.controller.get_tree_dict()
        self.tree_widget = tkw.FileTreeviewWidget(self, columns=self.columns, data=data,
                                                  callback=self._on_select_files, rowspan=2, **layout)
        self.frame_from = tk.LabelFrame(self, text='Fran')
        self.frame_from.grid(row=0, column=1, **layout)

        self.frame_to = tk.LabelFrame(self, text='Till')
        self.frame_to.grid(row=1, column=1, **layout)

        self.frame_tag = tk.LabelFrame(self, text='Tagga')
        self.frame_tag.grid(row=0, column=2, rowspan=2, **layout)

        tkw.grid_configure(self, nr_rows=2, nr_columns=3)

        self._set_image_frames()
        self._set_tag_frame()

    def _set_image_frames(self):
        self.image_widget_from = tkw.ImageWidget(self.frame_from, size=0.1)
        tkw.grid_configure(self.frame_from)
        self.image_widget_to = tkw.ImageWidget(self.frame_to, size=0.1)
        tkw.grid_configure(self.frame_to)

    def _set_tag_frame(self):
        layout = dict(padx=5,
                      pady=5,
                      sticky='nsew')
        self.tag_widget = tkw.TagWidget(self.frame_tag, show_untagged=False, columnspan=2, **layout)

        self.button_set_tags = tk.Button(self.frame_tag, text='Satt taggar', command=self._set_tags)
        self.button_set_tags.grid(row=1, column=0, **layout)

        self.button_remove_tags = tk.Button(self.frame_tag, text='Ta bort taggar', command=self._remove_tags)
        self.button_remove_tags.grid(row=1, column=1, **layout)

        tkw.grid_configure(self.frame_tag, nr_columns=2, nr_rows=2)

    def update_frame(self, event=None):
        tag_types_names = self.controller.get_tag_names_in_tag_types()
        self.tag_widget.update_frame(tag_types_names)

    def _on_select_files(self, selected_file_names):
        if not selected_file_names:
            return

        if selected_file_names[0] != self.image_from:
            self.image_from = selected_file_names[0]
            image_path = self.controller.get_file_path(self.image_from)
            self.image_widget_from.show_image(image_path)

        if selected_file_names[-1] != self.image_to:
            self.image_to = selected_file_names[-1]
            image_path = self.controller.get_file_path(self.image_to)
            self.image_widget_to.show_image(image_path)

    def _set_tags(self):
        tag_list =  self.tag_widget.get_checked()
        file_name_list = self.tree_widget.get_selected()
        for file_name in file_name_list:
            for tag in tag_list:
                self.controller.add_tag_to_file(tag_name=tag, file_name=file_name)
        self.tag_widget.uncheck_all()

    def _remove_tags(self):
        tag_list = self.tag_widget.get_checked()
        file_name_list = self.tree_widget.get_selected()
        for file_name in file_name_list:
            for tag in tag_list:
                self.controller.remove_tag_from_file(tag_name=tag, file_name=file_name)
        self.tag_widget.uncheck_all()


