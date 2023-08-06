
class Extractor:

	def extract(doc):
		raise NotImplementedError( "Need to implement extract function" )

	# should create a new dictionary each time
	def get_metadata():
		raise NotImplementedError( "Need to implement get_metadata function" )

	def get_renamed_input_fields(self, renamed_input_fields):
		raise NotImplementedError( "Need to implement get_renamed_input_fields function" )

	def set_renamed_input_fields(self, renamed_input_fields):
		if not (isinstance(renamed_input_fields, basestring) or isinstance(renamed_input_fields, types.ListType)):
			raise ValueError("renamed_input_fields must be a string or a list")
		self.renamed_input_fields = renamed_input_fields
		return self	