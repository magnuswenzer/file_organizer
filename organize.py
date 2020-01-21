
from pathlib import Path
import os 
import datetime 
import shutil

import utils

class NotAllowedToOverwrite(Exception):
	pass

def get_file_mapping(root_directory, suffix=None, nr_files=None):
	if suffix: 
		suffix = f'*.{suffix}'
	else:
		suffix = '*'
	data = {}
	n = 0
	for f in Path(root_directory).rglob(suffix):
		n += 1
		data[f.name] = f
		if nr_files and n == nr_files:
			return data
	return data


class FileOrganizer(object):
	def __init__(self, target_directory):
		self.target_directory = target_directory
		self.data = []
		self.file_types = set() 
		self.duplicate_files = [] 
		self.files_copied = {}

	def add_files(self, source_directory, suffix=None, source='Unknown'):

		if suffix: 
			suffix = f'*.{suffix}'
		else:
			suffix = '*'
		for f in Path(source_directory).rglob(suffix):
			if not f.is_file():
				continue
			file_object = File(f, self.target_directory, source=source)
			self.data.append(file_object)
			# if self.data.get(file_object.new_file_name):
			# 	self.duplicate_files.append((file_object.new_file_name, file_object.file_name))
			# 	continue
			# self.data[file_object.new_file_name] = file_object
			self.file_types.add(file_object.suffix)

	def __str__(self): 
		return self.root_directory

	def __repr__(self): 
		return 'class: FileOrganizer' 

	def get_nr_files(self): 
		return len(self.data)

	def get_nr_duplicate_files(self): 
		return len(self.duplicate_files)

	def copy_files_into_year_month_structure(self, suffix=[], overwrite=False):
		print(f'Start copying files to into year/month - structure')
		print(f'Overwrite is set to: {overwrite}')
		if type(suffix) == str:
			suffix = [suffix]
		for k, (fname, obj) in enumerate(self.data.items()):
			if not k%10:
				print(f'working on copying file nr: {k} ({fname})')
			if suffix and obj.suffix not in suffix:
				continue
			self.files_copied[fname] = True
			try:
				obj.copy_file(overwrite=overwrite) 
			except NotAllowedToOverwriteError:
				self.files_copied[fname] = False

	def get_path_objects(self):
		return self.data


class File(object):
	def __init__(self, file_path, target_directory, source='Unknown'):
		self.original_file_path = file_path
		self.original_path_object = Path(self.original_file_path)
		self.file_name = self.original_path_object.name
		self.source = source
		self.suffix = self.original_path_object.suffix

		# self.time_format = '%Y-%m-%d %H.%M.%S.%f'
		# self.time_format = '%Y-%m-%d %H.%M.%S.%f'

		mtime = self.original_path_object.stat().st_mtime
		self.time = datetime.datetime.fromtimestamp(mtime)

		self.new_path_object = Path(self.get_year_month_output_path(target_directory)) 
		self._save_location()

	def __str__(self): 
		return str(self.new_path_object)

	def __repr__(self): 
		return f'class: File({self.new_path_object})' 
	
	@property
	def year(self): 
		return self.time.year 

	@year.setter
	def year(self, year): 
		year = str(year)
		if len(year) != 4:
			raise ValueError(f'Invalid year: {year}')
		self.time = datetime.datetime.strptime(new_time_str, self.time_formats[0])
		self._save_location()

	@property
	def month(self): 
		return self.time.month 

	@property
	def day(self): 
		return self.time.day

	@property
	def hour(self): 
		return self.time.hour 

	@property
	def minute(self): 
		return self.time.minute 

	@property
	def second(self): 
		return self.time.second 

	def time_stamp_is_correct(self): 
		if self.time_stamp_file_name == self.time_stamp_time:
			return True 
		else:
			return False 
	
	def get_year_month_output_path(self, root_directory): 
		"""
		Returns Path object representing the file path for the file that follows the year/month stucture. 
		"""
		root_path = Path(root_directory)
		year = str(self.time.year)
		month = utils.Month(self.time.month).str
		file_path_object = root_path / year / month / f'{self.file_name}'
		return file_path_object

	def _save_location(self): 
		self.location = f'{self.year}/{self.month}'

	def copy_file(self, overwrite=False):
		"""
		Copies file from the original location the the new location year/month-structure.  
		"""
		target_directory = self.new_path_object.parent
		if not target_directory.exists(): 
			os.makedirs(target_directory)
		if self.new_path_object.exists() and not overwrite: 
			raise NotAllowedToOverwrite
		shutil.copyfile(str(self.original_path_object), str(self.new_path_object)) 

