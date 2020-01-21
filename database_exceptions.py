class DatabaseException(Exception):
	pass

class NewFileExistsError(DatabaseException):
	pass

class ItemAlreadyInDatabase(DatabaseException):
	pass

class FileAlreadyInDatabase(DatabaseException):
	pass

class WrongLocation(DatabaseException):
	pass

class InsertError(DatabaseException):
	pass

class SelectError(DatabaseException):
	pass

class DeleteError(DatabaseException):
	pass

class UnvalidOption(DatabaseException):
	pass