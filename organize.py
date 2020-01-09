
from pathlib import Path
import os 
import datetime 
import shutil

import utils

class NotAllowedToOverwriteError(Exception):
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


class Files(object):
	def __init__(self, root_directory, new_root_directory, suffix=None, source='Unknown'):
		self.root_directory = root_directory
		self.new_root_directory = new_root_directory
		self.source = source 

		if suffix: 
			suffix = f'*.{suffix}'
		else:
			suffix = '*'
		self.data = {}
		self.incorrect_time_staps = []
		self.file_types = set() 
		for f in Path(root_directory).rglob(suffix):
			if not f.is_file():
				continue
			file_object = File(f, new_root_directory, source=self.source)
			
			self.data[f.name] = file_object
			self.file_types.add(file_object.suffix)
			if not file_object.time_stamp_is_correct():
				self.incorrect_time_staps.append(f)
		self.nr_of_files = len(self.data)

	def __str__(self): 
		return self.root_directory

	def __repr__(self): 
		return f'class: Files({self.root_directory})' 

	def copy_files_into_year_month_structure(self, suffix=[], overwrite=False):
		print(f'Start copying files to into structure year/month - structure')
		print(f'Overwrite is set to: {overwrite}')
		if type(suffix) == str:
			suffix = [suffix]
		for k, (fname, obj) in enumerate(self.data.items()):
			if not k%10:
				print(f'working on copying file nr: {k}')
			if suffix and obj.suffix not in suffix:
				continue
			obj.copy_file(overwrite=overwrite)


class File(object):
	def __init__(self, path_object, new_root_directory, source='Unknown'):
		self.file_name = path_object.name
		self.original_path_object = path_object
		self.source = source
		self.suffix = self.original_path_object.suffix

		# First time foramt in list is the mian toime format
		self.time_formats = ['%Y-%m-%d %H.%M.%S']

		mtime = self.original_path_object.stat().st_mtime
		self.time = datetime.datetime.fromtimestamp(mtime)

		self.time_stamp_file_name = self._get_time_stamp_from_file_name()
		self.time_stamp_time = self._get_time_stamp_from_time()

		self.new_path_object = Path(self.get_year_month_output_path(new_root_directory))

	def __str__(self): 
		return str(self.original_path_object)

	def __repr__(self): 
		return f'class: File({self.original_path_object})' 
	
	@property
	def year(self): 
		time = self.get_time_stamp()
		return time.year 

	@year.setter
	def year(self, year): 
		year = str(year)
		if len(year) != 4:
			raise ValueError(f'Invalid year: {year}')
		if self.time_stamp_file_name: 
			time_str = self.time_stamp_file_name.strftime(self.time_formats[0])
			new_time_str = year + time_str[4:]
			self.time_stamp_file_name = datetime.datetime.strptime(new_time_str, self.time_formats[0])
		if self.time_stamp_file_name: 
			time_str = self.time.strftime(self.time_formats[0])
			new_time_str = year + time_str[4:]
			self.time = datetime.datetime.strptime(new_time_str, self.time_formats[0])
			self.time_stamp_time = self._get_time_stamp_from_time()


	@property
	def month(self): 
		time = self.get_time_stamp()
		return time.month 

	@property
	def day(self): 
		time = self.get_time_stamp()
		return time.day

	@property
	def hour(self): 
		time = self.get_time_stamp()
		return time.hour

	@property
	def minute(self): 
		time = self.get_time_stamp()
		return time.minute

	@property
	def second(self): 
		time = self.get_time_stamp()
		return time.second

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
		time_object = self.get_time_stamp()
		time_str = time_object.strftime(self.time_formats[0])
		year = str(time_object.year)
		month = utils.Month(time_object.month).str
		file_path_object = root_path / year / month / f'{time_str}{self.suffix}'
		return file_path_object

	def get_time_stamp_diff(self):
		time_stamp_file_name = self._get_time_stamp_from_file_name()
		if not from_file_name:
			return False
		time_stamp_time = self._get_time_stamp_from_time()
		return abs(time_stamp_file_name - time_stamp_time).seconds

	def _get_time_stamp_from_time(self): 
		return self.time

	def _get_time_stamp_from_file_name(self): 
		time_str = self.file_name.strip(self.original_path_object.suffix)
		time_object = False
		for time_format in self.time_formats:
			try:
				time_object = datetime.datetime.strptime(time_str, time_format)
				break
			except:
				pass
		return time_object

	def get_time_stamp(self): 
		"""
		Returns the a datetime object representing the time of the file. 
		First looks at file name ane then looks at st_mtime in file. 
		"""
		if self.time_stamp_file_name:
			return self.time_stamp_file_name
		else:
			return self.time_stamp_time

	def copy_file(self, overwrite=False):
		"""
		Copies file from the origional location the the new location (year/month-structure.  
		"""
		target_directory = self.new_path_object.parent
		if not target_directory.exists():
			os.makedirs(target_directory)
		if target_path_object.exists() and not overwrite:
			raise NotAllowedToOverwriteError
		shutil.copyfile(str(self.original_path_object), str(self.new_path_object)) 

