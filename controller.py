import os 

import database 
import organize
from database import FileDatabase 
from organize import File 

from database_exceptions import * 


class Controller(object):

	def __init__(self, target_directory=None, database_path=None): 
		if not target_directory:
			raise MissingAttribute('target_directory')
		if not database_path:
			raise MissingAttribute('database_path')

		self.target_directory = target_directory 
		self.database_path = database_path 

		self.file_objects = []
		self.db = FileDatabase(database_path) 
		self.db.setup_database()

		self.files_copied = {} 
		self.files_added_to_db = {} 
		# For the above: 
		# True means file was added/copied 
		# None means that file were not copied/added due to already in target location or in db. 
		# False mean something else 

		self._reset_info() 

	def _reset_info(self):
		self.info = []  # Hold information of latest call 
		self.error = []  # Hold information of latest call

	def _add_info(self, info):
		self.info.append(info)

	def _add_error(self, err):
		self.error.append(err)

	def add_files(self, source_directory=None, source=None, file_suffix=None): 
		self._reset_info()
		for root, dirs, files in os.walk(source_directory, topdown=True):
			for name in files: 
				if file_suffix and not name.endswith(file_suffix): 
					continue
				file_path = os.path.join(root, name) 
				file_object = File(file_path, self.target_directory, source=source)
				self.file_objects.append(file_object) 
				in_database = self._add_file_to_database(file_object)
				self.files_added_to_db[file_object] = in_database

				if in_database is True or in_database is None: 
					was_copied = self._copy_file(file_object)
					self.files_copied[file_object] = was_copied
				else: 
					self.files_copied[file_object] = False

	def _add_file_to_database(self, file_object): 
		try:
			self.db.add_file(file_object) 
			return True
		except database.FileAlreadyInDatabase:  
			return None
		return False

	def _copy_file(self, file_object): 
		"""
		Copies the added files. 
		""" 
		try:
			file_object.copy_file()
			return True 
		except organize.NotAllowedToOverwrite: 
			return None
		return False 

	def add_tag_type(self, tag_type):
		self._reset_info()
		if type(tag_type) == str:
			tag_type = [tag_type]
		tags_added = []
		already_added = []
		for tag in tag_type:
			try:
				self.db.add_tag_type(tag)
				tags_added.append(tag)
			except ItemAlreadyInDatabase as e: 
				already_added.append(tag)
		self._add_info(f'Tags types added: {", ".join(tags_added)}')
		self._add_info(f'Tags types already added: {", ".join(already_added)}')

	def remove_tag_type(self, tag_type):
		self._reset_info()
		if type(tag_type) == str:
			tag_type = [tag_type]
		tags_removed = []
		with_error = []
		for tag in tag_type:
			try:
				self.db.remove_tag_type(tag)
				tags_removed.append(tag)
			except DeleteError as e:
				with_error.append(tag)
		self._add_info(f'Tags removed: {", ".join(tags_removed)}')
		self._add_error(f'Errors for tag types: {", ".join(with_error)}')

	def add_tag_name(self, tag_name, tag_type): 
		self._reset_info()
		if type(tag_name) == str:
			tag_name = [tag_name]
		tags_added = []
		already_added = []
		for tag in tag_name:
			try:
				self.db.add_tag_name(tag, tag_type)
				tags_added.append(tag)
			except ItemAlreadyInDatabase as e: 
				already_added.append(tag)
		self._add_info(f'Tags name added: {", ".join(tags_added)}')
		self._add_info(f'Tags name already added: {", ".join(already_added)}') 

	def remove_tag_name(self, tag_name):
		self._reset_info()
		if type(tag_name) == str:
			tag_name = [tag_name]
		tags_removed = []
		with_error = []
		for tag in tag_name:
			try:
				self.db.remove_tag_name(tag)
				tags_removed.append(tag)
			except DeleteError as e:
				with_error.append(tag)
		self._add_info(f'Tags removed: {", ".join(tags_removed)}')
		self._add_error(f'Errors for tag names: {", ".join(with_error)}')

	def add_tag_to_file(self, tag_name, file_name): 
		self._reset_info()
		if type(tag_name) == str:
			tag_name = [tag_name]
		tags_added = []
		already_added = []
		for tag in tag_name:
			try:
				self.db.add_tag(tag, file_name)
				tags_added.append(tag)
			except ItemAlreadyInDatabase as e: 
				already_added.append(tag)
		self._add_info(f'Tags added: {", ".join(tags_added)}')
		self._add_info(f'Tags already added: {", ".join(already_added)}')

	def remove_tag_from_file(self, tag_name, file_name):
		self._reset_info()
		if type(tag_name) == str:
			tag_name = [tag_name]
		tags_removed = []
		with_error = []
		for tag in tag_name:
			try:
				self.db.remove_tag(tag, file_name)
				tags_removed.append(tag)
			except DeleteError as e:
				with_error.append(tag)
		self._add_info(f'Tags removed: {", ".join(tags_removed)}')
		self._add_error(f'Errors: {", ".join(with_error)}')

	def get_tag_type_list(self):
		self._reset_info()
		return self.db.get_tag_type_list()

	def get_tag_name_list(self, tag_type=False):
		self._reset_info()
		return self.db.get_tag_name_list(tag_type=tag_type)

	def get_tags_for_file(self, file_name):
		self._reset_info()
		return self.db.get_tags_for_file(file_name) 

	def get_file_name_list(self, nr=None):
		self._reset_info()
		return self.db.get_file_name_list(nr) 

	def get_files_with_tags(self, tags, and_or='AND'): 
		self._reset_info()
		return self.db.get_file_names_with_tags(tags, and_or=and_or) 

	

class ControllerException(Exception):
	pass


class MissingInformation(ControllerException):
	pass 


class MissingAttribute(ControllerException):
	pass
