import os
import sqlite3
from sqlite3 import Error

class OriginalFileExistsError(Exception):
	pass

class NewFileExistsError(Exception):
	pass

class FileDatabase(object):

	def __init__(self, location=':memory:'): 
		self.location = location 

	def setup_database(self):
		if self.location == ':memory:' or not os.path.exists(self.location): 
			self._create_database() 
		self._create_tables()

	def _create_database(self): 
		"""
		Creates the database by simply connecting to it. 
		"""
		print(f'Creating the database at: {self.location}')
		conn = None
		try:
			conn = sqlite3.connect(self.location)
		except Error as e:
			print(e)
		finally:
			if conn:
				conn.close()

	def _create_tables(self): 
		"""
		Creates the database by simply connecting to it. 
		"""
		print(f'Creating tables at: {self.location}')
		
		# Create table Files 
		sql_files = """
			CREATE TABLE IF NOT EXISTS Files (
			file_id integer PRIMARY KEY,
			file_name text NOT NULL,
			original_file_name text NOT NULL,
			source text NOT NULL,
			year integer NOT NULL,
			month integer NOT NULL,
			day integer NOT NULL
			);
			"""
		self._execute(sql_files)

		# Create table TagNames 
		sql_tag_names = """
			CREATE TABLE IF NOT EXISTS TagNames (
			tag_name_id integer PRIMARY KEY,
			tag_name text NOT NULL,
			tag_type_id text NOT NULL,
			FOREIGN KEY (tag_type_id) REFERENCES TagTypes (tag_type_id)
			);
			"""
		self._execute(sql_tag_names)

		# Create table TagTypes 
		sql_tag_types = """
			CREATE TABLE IF NOT EXISTS TagTypes (
			tag_type_id integer PRIMARY KEY,
			tag_type text NOT NULL
			);
			"""
		self._execute(sql_tag_types)

		# Create table FileTagNames 
		sql_file_tag_names = """
			CREATE TABLE IF NOT EXISTS FileTagNames (
			file_id integer NOT NULL,
			tag_name_id integer NOT NULL,
			FOREIGN KEY (file_id) REFERENCES Files (file_id), 
			FOREIGN KEY (tag_name_id) REFERENCES TagNames (tag_name_id)
			);
			"""
		self._execute(sql_file_tag_names)

	def add_file(self, file_object):
		"""
		Adds a file to the database. file_object is a organize.File object. 
		""" 
		# First check if file is already in database. Check original file name!
		sql_select = """SELECT * FROM Files WHERE original_file_name=(?)"""
		variables = (file_object.original_path_object.name, )
		result = self._execute(sql_select, variables=variables, fetchall=True)
		
		if result: 
			raise OriginalFileExistsError(file_object.original_path_object.name)

		# Now check if new file name already exists in database. 
		sql_select = """SELECT * FROM Files WHERE new_file_name=(?)"""
		variables = (file_object.new_path_object.name, )
		result = self._execute(sql_select, variables=variables, fetchall=True)
		
		if result: 
			"This means that a picture has been taken at the same time. Raise an exception"
			raise NewFileExistsError(file_object.new_path_object.name)

		sql_insert = """
			INSERT INTO Files (file_name, original_file_name, source, year, month, day) 
			VALUES (?, ?, ?, ?, ?, ?)
			"""
		variables = (file_object.new_path_object.name, 
					 file_object.original_path_object.name, 
					 file_object.source, 
					 file_object.year, 
					 file_object.month, 
					 file_object.day)

		return self._execute(sql_insert, variables=variables)

	def add_tag_type(self, tag_type):
		"""
		Adds a tag type to the TagType table. 
		"""
		current_list = [item[0] for item in self.get_tag_type_list()]
		print(current_list)
		if tag_type in current_list:
			return

		sql_insert = """
			INSERT INTO TagTypes (tag_type) 
			VALUES (?)
			"""
		variables = (tag_type,)

		self._execute(sql_insert, variables)


	def add_tag_name(self, tag_name, tag_type):
		"""
		Adds a tag name to the TagName table. 
		"""
		pass

	def add_tag(self, file_name, tag_name):
		"""
		Adds a tag to the given file_name. 
		"""
		pass

	def remove_tag(self, file_name, tag_name):
		"""
		Removes a tag from the given file_name. 
		"""
		pass

	def get_tag_type_list(self): 
		"""
		Returns a list of all availbale tag types. 
		"""
		sql = """
		SELECT tag_type FROM TagTypes
		"""
		return self._execute(sql, fetchall=True)

	def get_tag_name_list(self, tag_type=False):
		"""
		Returns a list of all availbale tag names. 
		If tag_type is given only tag_names belonging to that tag_type is returned. 
		"""
		pass

	def _execute(self, sql_command, variables=None, commit=False, fetchall=False):
		"""
		Execute the given sql command. 
		"""
		conn = None
		result = True
		try:
			conn = sqlite3.connect(self.location)
			c = conn.cursor()

			if variables:
				c.execute(sql_command, variables)
			else:
				c.execute(sql_command)

			if fetchall:
				result = c.fetchall()
			
			if commit or fetchall or variables:
				conn.commit()

		except Error as e:
			print(e)
			result = False
		finally:
			if conn:
				conn.close()

		return result

