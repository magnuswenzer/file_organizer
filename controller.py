import os 

import database 
import organize
from database import FileDatabase 
from organize import File
import utils
from pathlib import Path
from collections import OrderedDict
import json
import socket

from database_exceptions import * 


class Controller(object):

	def __init__(self):
		self.location = None
		self.db_path = None
		self.db = None
		self.databases = Databases()
		self.rotation_info_object = RotateInfo()
		self.save_object = Saves()

	def _add_database(self, db_path, location):
		try:
			self.databases.new(db_path, location)
		except DatabaseExists:
			raise NotAValidDatabase(f'Databas {db_path} finns redan!')
		self.set_database(db_path)

	def set_database(self, db_path, location=None):
		loc = self.databases.get_location(db_path)
		if not loc:
			if not location:
				raise NotAValidDatabase
			self._add_database(db_path, location)
		elif location:
			self.databases.set_location(db_path, location)
		else:
			location = self.databases.get_location(db_path)

		self.location = location
		self.db_path = db_path

		self.file_objects = []
		self.db = FileDatabase(self.db_path) 
		self.db.setup_database()

		self.files_copied = {} 
		self.files_added_to_db = {} 
		# For the above: 
		# True means file was added/copied 
		# None means that file were not copied/added due to already in target location or in db. 
		# False mean something else 

		self._reset_info() 

	def _reset_info(self):
		if not self.db_path:
			raise('No database loaded')
		self.info = []  # Hold information of latest call 
		self.error = []  # Hold information of latest call

	def _add_info(self, info):
		if not self.db_path:
			raise('No database loaded')
		self.info.append(info)

	def _add_error(self, err):
		if not self.db_path:
			raise('No database loaded')
		self.error.append(err)

	def add_files(self, source_directory=None, source=None, file_suffix=None, change_year_to=None):
		self._reset_info()
		self.files_copied = {}
		for root, dirs, files in os.walk(source_directory, topdown=True):
			for name in files: 
				if file_suffix and not name.endswith(file_suffix): 
					continue
				file_path = os.path.join(root, name) 
				file_object = File(file_path, self.location, source=source, change_year_to=change_year_to)
				self.file_objects.append(file_object) 
				in_database = self._add_file_to_database(file_object)
				self.files_added_to_db[file_object] = in_database

				if in_database is True or in_database is None: 
					was_copied = self._copy_file(file_object)
					self.files_copied[file_object] = was_copied
				else: 
					self.files_copied[file_object] = 'not in db'

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
			return 'file copied'
		except organize.FileOfSameSize:
			return 'same size'
		except organize.FileOfDifferentSize:
			return 'different size'

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

	def get_tag_names_in_tag_types(self):
		self._reset_info()
		data = {}
		for tag_type in self.get_tag_type_list():
			data[tag_type] = sorted(self.get_tag_name_list(tag_type))
		return data

	def get_tags_for_file(self, file_name):
		self._reset_info()
		return self.db.get_tags_for_file(file_name) 

	def get_file_name_list(self, nr=None):
		self._reset_info()
		return self.db.get_file_name_list(nr)

	def get_file_path_list(self, nr=None):
		self._reset_info()
		return_list = []
		for file_name in self.get_file_name_list(nr):
			return_list.append(self.get_file_path(file_name))
		return return_list

	def get_file_path(self, file_name):
		self._reset_info()
		location = self.db.get_location(file_name)
		year, month_nr = location.split('/')
		# m = utils.Month(month_nr)
		file_path = Path(f'{self.location}/{year}/{month_nr}/{file_name}')
		return file_path

	def get_file_list(self, tags=None, year=None, month=None):
		self._reset_info()
		file_list = self.db.get_file_list(tags=tags, year=year, month=month)
		if not file_list:
			return []
		return [self.get_file_path(file_name) for file_name in file_list]

	def get_untagged_files(self):
		self._reset_info()
		file_list = self.db.get_untagged_files()
		if not file_list:
			return []
		return [self.get_file_path(file_name) for file_name in file_list]

	def get_file_info(self, file_name):
		info = self.db.get_file_info(file_name)
		if 'Plats' in info:
			info['Plats'] = str(Path(self.location, info['Plats']))
		return info

	def get_tree_dict(self, nr=None):
		"""
		Returns the content of te database as a dict.
		Structure is data[year][month][file_name]
		"""
		self._reset_info()
		data = {}
		for file_name in self.get_file_name_list(nr=nr):
			location = self.db.get_location(file_name)
			year, month = location.split('/')
			data.setdefault(year, {})
			data[year].setdefault(month, OrderedDict())
			data[year][month][file_name] = {}

		return data

	def get_year_list(self):
		self._reset_info()
		return self.db.get_year_list()


class Databases(object):

	def __init__(self, file_path='databases.txt'):
		self.file_path = file_path
		self.data = {}
		if os.path.exists(file_path):
			self._load()

	def _save(self):
		with open(self.file_path, 'w') as fid:
			json.dump(self.data, fid)

	def _load(self):
		with open(self.file_path) as fid:
			self.data = json.load(fid)

	def new(self, db_path, location):
		if db_path in self.data:
			raise DatabaseExists(db_path)
		self.data[db_path] = {}
		self.data[db_path][socket.gethostname()] = location
		self._save()

	def set_location(self, db_path, location):
		self.data[db_path][socket.gethostname()] = location
		self._save()

	def get_location(self, db_path):
		return self.data.get(db_path, {}).get(socket.gethostname(), '')

	def get_all(self):
		return self.data


class RotateInfo(object):
	def __init__(self, file_path='rotation.txt'):
		self.file_path = file_path
		self.data = {}
		if os.path.exists(file_path):
			self._load()

	def _save(self):
		with open(self.file_path, 'w') as fid:
			json.dump(self.data, fid)

	def _load(self):
		with open(self.file_path) as fid:
			self.data = json.load(fid)

	def set(self, file_name, rotation):
		self.data[file_name] = rotation
		self._save()

	def get(self, file_name):
		return self.data.get(file_name, 0)


class Saves(object):
	def __init__(self, file_path='saves.txt'):
		self.file_path = file_path
		self.data = {}
		if os.path.exists(file_path):
			self._load()

	def _save(self):
		with open(self.file_path, 'w') as fid:
			json.dump(self.data, fid)

	def _load(self):
		with open(self.file_path) as fid:
			self.data = json.load(fid)

	def set(self, key, value):
		self.data[key] = value
		self._save()

	def get(self, key):
		return self.data.get(key, None)

	def setdefault(self, key, value):
		val = self.get(key)
		if val is not None:
			return val
		else:
			self.set(key, value)
			return value


class DatabaseExists(Exception):
	pass


class ControllerException(Exception):
	pass


class MissingInformation(ControllerException):
	pass 


class MissingAttribute(ControllerException):
	pass


class NotAValidDatabase(ControllerException):
	pass
