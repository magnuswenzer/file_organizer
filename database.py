import os
import sqlite3
from sqlite3 import Error

from database_exceptions import * 


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

		self.file_items = ['Filnamn', 'Plats', 'Källa', 'Filtyp', 'Tid', 'År', 'Månad']
		
		# Create table Files 
		sql_files = """
			CREATE TABLE IF NOT EXISTS File (
			file_name text PRIMARY KEY,
			location text NOT NULL,
			source text NOT NULL, 
			suffix text NOT NULL, 
			time timestamp, 
			year text NOT NULL, 
			month text NOT NULL 
			);
			"""
		self._execute(sql_files)

		# Create table TagNames 
		sql_tag_names = """
			CREATE TABLE IF NOT EXISTS TagName (
			tag_name text NOT NULL PRIMARY KEY,
			tag_type text NOT NULL,
			FOREIGN KEY (tag_type) REFERENCES TagTypes (tag_type)
			);
			"""
		self._execute(sql_tag_names)

		# Create table TagTypes 
		sql_tag_types = """
			CREATE TABLE IF NOT EXISTS TagType (
			tag_type text PRIMARY KEY
			);
			"""
		self._execute(sql_tag_types)

		# Create table FileTagNames 
		sql_file_tag_names = """
			CREATE TABLE IF NOT EXISTS FileTagName (
			file_name text NOT NULL, 
			tag_name text NOT NULL, 
			PRIMARY KEY (file_name, tag_name)
			FOREIGN KEY (file_name) REFERENCES File (file_name), 
			FOREIGN KEY (tag_name) REFERENCES TagName (tag_name)
			); 
			""" 
		self._execute(sql_file_tag_names)

	def add_file(self, file_object):
		"""
		Adds a file to the database. file_object is a organize.File object. 
		""" 
		# First check if file is already in database. Check original file name!
		# sql_select = """SELECT * FROM File WHERE original_file_name=(?)"""
		# variables = (file_object.original_path_object.name, )
		# result = self._execute(sql_select, variables=variables, fetchall=True)
		
		# if result: 
		# 	raise OriginalFileExistsError(file_object.original_path_object.name)

		# Check if file name already exists in database.
		file_name_list = self.get_file_name_list()
		# data = self.get_selection('File', 'file_name', 'location', file_name=file_object.file_name)

		# sql_select = """SELECT * FROM File WHERE file_name=(?)"""
		# variables = (file_object.new_path_object.name, )
		# result = self._execute(sql_select, variables=variables, fetchall=True)
		if file_object.file_name in file_name_list:
			return
		# if data['file_name']:
		# 	if data['location'][0] != file_object.location:
		# 		raise WrongLocation(file_object.location)
		# 	else:
		# 		raise FileAlreadyInDatabase(file_object.file_name)

		sql_insert = """
			INSERT INTO File (file_name, location, source, suffix, time, year, month) 
			VALUES (?, ?, ?, ?, ?, ?, ?)
			"""
		variables = (file_object.file_name, 
					 file_object.location, 
					 file_object.source, 
					 file_object.suffix, 
					 file_object.time,
					 file_object.year,
					 file_object.month)

		return self._execute(sql_insert, variables=variables) 

	def add_files(self, file_object_list): 
		not_added = []
		for file_object in file_object_list:
			try:
				self.add_file(file_object)
			except NewFileExistsError:
				not_added.append(file_object)
		return not_added

	def add_tag_type(self, tag_type):
		"""
		Adds a tag type to the TagType table. 
		"""
		current_list = self.get_tag_type_list()
		if tag_type in current_list:
			raise ItemAlreadyInDatabase(f'tag_type: {tag_type}')

		sql_insert = """
			INSERT INTO TagType (tag_type) 
			VALUES (?)
			"""
		variables = (tag_type,)

		self._insert(sql_insert, variables)

	def remove_tag_type(self, tag_type): 
		# Remove from TagType 
		sql_delete = f"""
			DELETE FROM TagType 
			WHERE tag_type = "{tag_type}"
			"""
		self._delete(sql_delete, commit=True) 

		# Find tag_names 
		sql = f"""
			SELECT tag_name FROM TagName
			WHERE tag_type = "{tag_type}"
			"""
		result = [item[0] for item in self._select(sql, fetchall=True)]

		# Remove tag_names in result 
		for tag in result:
			self.remove_tag_name(tag)

	def add_tag_name(self, tag_name, tag_type):
		"""
		Adds a tag name to the TagName table. 
		"""
		sql_insert = """
			INSERT INTO TagName (tag_name, tag_type) 
			VALUES (?, ?)
			"""
		variables = (tag_name, tag_type)
		
		self._insert(sql_insert, variables)

	def remove_tag_name(self, tag_name): 
		# Remove from TagName 
		sql_delete = f"""
			DELETE FROM TagName 
			WHERE tag_name = "{tag_name}"
			"""
		self._delete(sql_delete, commit=True)

		# Remove from FileTagName
		sql_delete = f"""
			DELETE FROM FileTagName 
			WHERE tag_name = "{tag_name}"
			"""
		self._delete(sql_delete, commit=True)


	def add_tag(self, tag_name, file_name):
		"""
		Adds a tag to the given file_name. 
		"""
		# Check if file_name exists 
		if file_name not in self.get_file_name_list():
			raise UnvalidOption(f'file_name: {file_name}') 
		# Check if tag_name exists (is valid)
		if type(tag_name) == list:
			tag_list = self.get_tag_name_list()
			if not all([tag in tag_list for tag in tag_name]):
				raise UnvalidOption(f'tag_name: {tag_name}') 
		else:
			if tag_name not in self.get_tag_name_list():
				raise UnvalidOption(f'tag_name: {tag_name}') 
		
		# Add tag 
		sql_insert = """
			INSERT INTO FileTagName (file_name, tag_name) 
			VALUES (?, ?)
			"""
		if type(tag_name) == list:
			variables = [(file_name, tag) for tag in tag_name]
		else:
			variables = (file_name, tag_name)

		self._insert(sql_insert, variables)

	def remove_tag(self, tag_name, file_name):
		"""
		Removes a tag from the given file_name. 
		"""
		sql_delete = f"""
		DELETE FROM FileTagName 
		WHERE file_name = "{file_name}" AND tag_name = "{tag_name}"
		"""
		self._delete(sql_delete, commit=True)

	def get_file_name_list(self, nr=None): 
		"""
		Returns a list of the all file_names. 
		"""
		sql = """
		SELECT file_name FROM File
		"""
		return_list = [item[0] for item in self._select(sql, fetchall=True)] 
		if nr:
			return_list = return_list[:nr] 
		return return_list

	def old_get_file_names_with_tags(self, tags=None, and_or='AND', year=None, month=None):
		def add_year():
			string = """"""
			if year:
				string = f""" 
				AND year = "{year}"
				"""
			return string

		def add_month():
			string = """"""
			if month:
				string = f""" 
				AND month = "{month}"
				"""
			return string

		if type(tags) == str:
			sql = f"""
				SELECT file_name FROM FileTagName 
				WHERE tag_name = "{tags}"
				"""
			sql = sql + add_year() + add_month()
			return [item[0] for item in self._select(sql, fetchall=True)] 

		else:
			set_result = None
			for tag in tags:
				sql = f"""
					SELECT file_name FROM FileTagName 
					WHERE tag_name = "{tag}"
					"""
				sql = sql + add_year() + add_month()
				result = [item[0] for item in self._select(sql, fetchall=True)] 
				if not set_result:
					set_result = set(result)
					continue
				set_r = set(result)
				if and_or.upper() == 'OR': 
					set_result.update(set_r)
				elif and_or.upper() == 'AND': 
					set_result = set_result.intersection(set_r)
			return list(set_result)

	def old_get_selection(self, table, *args, and_or='AND', by_column=True, **kwargs):
		"""
		Crates a dynamic sql select query and returns a dictionary with the result.  
		""" 
		def _where(key, value):
			if type(value) == str:
				return f'{key} = "{value}"'
			else:
				return f"""{key} IN ("{'", "'.join(value)}")"""

		sql = f"""
			 SELECT {', '.join(args)}
			 FROM {table} 
			 """
		if kwargs: 
			and_or = ' ' + and_or + ' '
			sql = sql + f"""
			WHERE {and_or.join([_where(key, value) for key, value in kwargs.items()])}

		"""
		result = self._select(sql, fetchall=True) 
		if by_column:
			data = {}
			for c, arg in enumerate(args):
				data[arg] = [item[c] for item in result]
		else: 
			data = []
			for row in result:
				data.append(dict(zip(args, row)))
		return data

	def get_tag_type_list(self): 
		"""
		Returns a list of all availbale tag types. 
		"""
		sql = """
		SELECT tag_type FROM TagType
		"""
		return [item[0] for item in self._select(sql, fetchall=True)]

	def get_tag_name_list(self, tag_type=False):
		"""
		Returns a list of all availabale tag names. 
		If tag_type is given only tag_names belonging to that tag_type is returned. 
		"""
		if tag_type:
			sql = f"""
			SELECT tag_name 
			FROM TagName
			WHERE tag_type = "{tag_type}"
			"""
		else:
			sql = """
			SELECT tag_name 
			FROM TagName
			"""
		return [item[0] for item in self._select(sql, fetchall=True)]

	def get_tags_for_file(self, file_name):
		"""
		Returns a list of all tags linked to the given file_name. 
		SELECT a1, a2, b1, b2
		FROM A
		INNER JOIN B on B.f = A.f;
		"""
		sql = f"""
				SELECT tag_name
				FROM FileTagName
				WHERE file_name = "{file_name}"
				"""
		return [item[0] for item in self._select(sql, fetchall=True)]

	def old_get_file_list(self, tags=[], year=None, month=None, sort_by='time'):
		"""
		"""
		if not any([tags, year, month]):
			sql = f"""
						SELECT file_name 
						From File
						ORDER BY File.{sort_by}
					"""
			print('SQL:', sql)
			return [item[0] for item in self._select(sql, fetchall=True)]

		file_set = None
		for tag in tags:
			sql = f"""
				SELECT File.file_name
				FROM File LEFT JOIN FileTagName ON File.file_name = FileTagName.file_name
				WHERE FileTagName.tag_name = "{tag}"
				ORDER BY File.{sort_by}

			"""
			print('SQL:', sql)
			result_list = [item[0] for item in self._select(sql, fetchall=True)]
			print(result_list)
			if not file_set:
				file_set = set(result_list)
			else:
				file_set = file_set.intersection(set(result_list))

		if year:
			sql = f"""
				SELECT file_name
				FROM File
				WHERE year = {year}
				ORDER BY {sort_by}

			"""
			result_list = [item[0] for item in self._select(sql, fetchall=True)]
			print(result_list)
			file_set = file_set.intersection(set(result_list))
		if month:
			sql = f"""
				SELECT file_name
				FROM File
				WHERE month = {month}
				ORDER BY {sort_by}

			"""
			result_list = [item[0] for item in self._select(sql, fetchall=True)]
			print(result_list)
			file_set = file_set.intersection(set(result_list))
		print('file_set', file_set)
		return list(file_set)

	def _file_names_tag_statement(self, tag_list):
		tag = tag_list.pop(0)
		sql =  f"""
				file_name IN (
				SELECT file_name 
				FROM FileTagName 
				WHERE tag_name = "{tag}"
				)
				"""
		if tag_list:
			sql = sql + f""" AND {self._file_names_tag_statement(tag_list)} """
			return sql
		else:
			return sql

	def get_file_list(self, tags=[], year=None, month=None, sort_by='file_name'):
		"""
		"""
		sql = """
				SELECT file_name 
				FROM File 
		"""
		# Add year and month
		year_month_str_list = []
		if year:
			year_month_str_list.append(f"""
						year = "{year}"
						""")
		if month:
			year_month_str_list.append(f"""
						month = "{month}"
						""")
		if year_month_str_list:
			sql = sql + ' WHERE ' + ' AND '.join(year_month_str_list)

		if tags:
			if year_month_str_list:
				sql = sql + ' AND '
			else:
				sql = sql + ' WHERE '
			sql = sql + self._file_names_tag_statement(tags)

		sql = sql + f" ORDER BY {sort_by}"
		# print('='*30)
		# print(sql)
		# print('-'*30)
		result_list = [item[0] for item in self._select(sql, fetchall=True)]
		return result_list

	def get_file_info(self, file_name):
		sql = f"""
				SELECT *
				FROM File 
				WHERE file_name = "{file_name}"
				"""
		info = dict(zip(self.file_items, self._select(sql, fetchall=True)[0]))
		return info

	def get_untagged_files(self):
		sql = f"""
				SELECT file_name
				FROM File
				"""
		all_files = set([item[0] for item in self._select(sql, fetchall=True)])

		sql = f"""
			SELECT file_name
			FROM FileTagName 
			"""
		tagged_files = set([item[0] for item in self._select(sql, fetchall=True)])

		return sorted(all_files - tagged_files)

	def get_location(self, file_name):
		sql = f"""
					SELECT location
					FROM File
					WHERE file_name = "{file_name}"
					"""
		return self._select(sql, fetchall=True)[0][0]

	def get_year_list(self):
		sql = f"""
				SELECT year
				FROM File
				"""
		return sorted(set([item[0] for item in self._select(sql, fetchall=True)]))

	def get_months_for_year(self, year):
		sql = f"""
				SELECT month
				FROM File 
				WHERE year = "{year}"
				"""
		return sorted(set([item[0] for item in self._select(sql, fetchall=True)]))

	def _insert(self, *args, **kwargs):
		"""
		Call this to insert values into tables. 
		"""
		try: 
			return self._execute(*args, **kwargs)
		except Error as e:
			if 'UNIQUE' in str(e): 
				raise ItemAlreadyInDatabase(e)
			else:
				raise e
			raise InsertError(e)

	def _delete(self, *args, **kwargs): 
		"""
		Call this to delete values in tables. 
		"""
		try: 
			return self._execute(*args, **kwargs)
		except Error as e:
			raise DeleteError(e)

	def _select(self, *args, **kwargs): 
		"""
		Call this to select values from tables. 
		"""
		try: 
			return self._execute(*args, **kwargs)
		except Error as e:
			raise SelectError(e)

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
			raise 
		finally:
			if conn:
				conn.close()

		return result

	def _from_join_string_file_name(self):
		return



