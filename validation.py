import re, datetime, sys

class Validation():
	#List to store the error messages
	errors = []

	error_message_templates = {
		'alpha':' can have only alphabets',
		'alpha_num':' can have alphabets or numbers',
		'between':' must be between',
		'boolean':' must be one of the following ',
		'confirmed':' must have a pair field named ',
		'date':' value does not match date format ',
		'digits':' must be an integer',
		'different':' must not be the same as ',
		'email':' must be a valid email address',
		'in':' must not be one of these: ',
		'ip':' must be a valid IP address',
		'integer':' must be an integer',
		'max':'The maximum value for the field ',
		'min':'The minimum value for the field ',
		'not_in':' must not be one of these: ',
		'before':" is invalid. Rule: ",
		'after': " is invalid. Rule: ",
		'present':'The data dictionary must have a nullable ',
		'phone':' must be a valid Phone Number',
		'regex':' field does not match the RE',
		'required':' must be filled',
		'same':' should be the same as ',
		'size':'The maximum number of characters in a ',
		'website':' must be a valid Website URL',
		'no_field':'No field named ',
	}

	def validate(self, data, rules):
		"""Validate the 'data' according to the 'rules' given, returns a list of errors named 'errors'"""

		errors = []
		
		#iterate through the rules dictionary, fetching each rule name (dictionary key) one by one
		for field_name in rules:

			#fetch the rule (value of dictionary element) from "rules" dictionary for the current rule name (dictionary key) and split it to get a list
			field_rules = rules[field_name].split('|')
			
			#field_errors will keep the errors for a particular field, which will be appended to the main "errors" list
			field_errors = []

			#now looping through rules of one field one rule at a time with each iteration
			for rule in field_rules:

				#if the field has an "after" rule assigned
				if rule.startswith("after"):
					field_errors.extend(self.__validate_after_date_fields(data,field_name,field_rules,rule))

				#if the field has an "alpha" rule assigned
				elif rule == "alpha":
					field_errors.extend(self.__validate_alpha_fields(data,field_name))

				#if the field has an "alpha_num" rule assigned
				elif rule == "alpha_num":
					field_errors.extend(self.__validate_alpha_num_fields(data,field_name))

				#if the field has a "before" rule assigned
				elif rule.startswith("before"):
					field_errors.extend(self.__validate_before_date_fields(data,field_name,field_rules,rule))

				#if the field has a "between" rule assigned
				elif rule.startswith("between"):
					field_errors.extend(self.__validate_between_fields(data, field_name, rule))

				#if the field has a "boolean" rule assigned
				elif rule == "boolean":
					field_errors.extend(self.__validate_boolean_fields(data,field_name))

				#if the field has a "confirmed" rule assigned
				elif rule.startswith("confirmed"):
					field_errors.extend(self.__validate_confirmed_fields(data,field_name))

				#if the field has a "date" rule assigned
				elif rule == "date":
					field_errors.extend(self.__validate_date_fields(data,field_name,field_rules))

				#if the field has a "digit" rule assigned
				elif rule == "digits":
					field_errors.extend(self.__validate_integer_fields(data,field_name))

				#if the field has a "different" rule assigned
				elif rule.startswith("different"):
					field_errors.extend(self.__validate_different_fields(data,field_name, rule))

				#if the field has a "email" rule assigned
				elif rule == "email":
					field_errors.extend(self.__validate_email_fields(data,field_name))

				#if the field has a "in" rule assigned
				elif rule.startswith("in"):
					field_errors.extend(self.__validate_in_fields(data,field_name, rule))

				#if the field has a "ip" rule assigned
				elif rule == "ip":
					field_errors.extend(self.__validate_ip_fields(data,field_name))

				#if the field has a "max" rule assigned
				elif rule.startswith("max"):
					field_errors.extend(self.__validate_max_fields(data,field_name,rule))

				#if the field has a "min" rule assigned
				elif rule.startswith("min"):
					field_errors.extend(self.__validate_min_fields(data,field_name,rule))

				#if the field has a "not_in" rule assigned
				elif rule.startswith("not_in"):
					field_errors.extend(self.__validate_not_in_fields(data,field_name,rule))

				#if the field has a "present" rule assigned
				elif rule == "present":
					field_errors.extend(self.__validate_present_fields(data,field_name))

				#if the field has a "phone" rule assigned
				elif rule == "phone":
					field_errors.extend(self.__validate_phone_fields(data, field_name))

				#if the field has a "regex" rule assigned
				elif rule.startswith("regex"):
					field_errors.extend(self.__validate_regex_fields(data,field_name, rule))

				#if the field has a "required" rule assigned
				elif rule == "required":
					field_errors.extend(self.__validate_required_fields(data, field_name))

				#if the field has a "same" rule assigned
				elif rule.startswith("same"):
					field_errors.extend(self.__validate_same_fields(data, field_name, rule))

				#if the field has a "size" rule assigned
				elif rule.startswith("size"):
					field_errors.extend(self.__validate_size_fields(data,field_name,rule))

				#if the field has a "website" rule assigned
				elif rule == "website":
					field_errors.extend(self.__validate_website_fields(data,field_name))

			#combine the errors of current field with the global errors list
			errors.extend(field_errors)
		self.errors = errors
		return errors

	def __validate_required_fields(self, data, field_name):
		"""Used for validating required fields, returns a list of error messages"""

		errs = []
		try:
			if data[field_name] == '':
				 errs.append(field_name + self.error_message_templates['required'])
		except KeyError:
			errs.append(self.error_message_templates['no_field'] + field_name)

		return errs        

	def __validate_date_fields(self, data, field_name, field_rules):
		"""Used for validating date fields, returns a list of error messages"""

		errs = []
		date_format = None

		#loop through each rule for the particular field to check if there is any date_format rule assigned
		for rule in field_rules:

			#if there is a date_format rule assigned then fetch the date format from that
		 	if rule.startswith("date_format"):
				df_format_index = field_rules.index(rule)
				date_format = field_rules[df_format_index].split(":")[1]

		#or if there is no date_format assigned then use a default format for validation
		if not date_format:
			date_format = '%m/%d/%Y'

		try:
			 datetime.datetime.strptime(data[field_name], date_format)
		except ValueError,e:
			 errs.append(field_name + self.error_message_templates['date'] + date_format)
		except KeyError:
			 errs.append(self.error_message_templates['no_field'] + (field_name))
			
		return errs

	def __validate_before_date_fields(self, data, field_name, field_rules,rule):
		 """Used for validating fields for a date before the specified date value, returns a list of error messages"""

		 #retrieve the value for that before rule
		 before_date_value = rule.split(':')[1]

		 errs = []
		 date_format = None

		 #loop through each rule for the particular field to check if there is any date_format rule assigned
		 for rule in field_rules:
			#if there is a date_format rule assigned then fetch the date format from that
		 	if rule.startswith("date_format"):
				df_format_index = field_rules.index(rule)
				date_format = field_rules[df_format_index].split(":")[1]

		 #or if there is no date_format rule assigned then use a default format for validation
		 if not date_format:
			date_format = '%m/%d/%Y'

		 try:
			date_entered = datetime.datetime.strptime(data[field_name], date_format).date()
			before_date = datetime.datetime.strptime(before_date_value, date_format).date()
			if date_entered >= before_date:
				 errs.append(field_name + self.error_message_templates['before']+ rule)
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 except ValueError:
			 errs.append(sys.exc_info()[1])
		 return errs


	def __validate_after_date_fields(self, data, field_name, field_rules,rule):
		 """Used for validating fields for a date after the specified date value, returns a list of error messages"""

		 #retrieve the value for that after rule
		 after_date_value = rule.split(':')[1]

		 errs = []
		 date_format = None

		 #loop through each rule for the particular field to check if there is any date_format rule assigned
		 for rule in field_rules:
			#if there is a date_format rule assigned then fetch the date format from that
		 	if rule.startswith("date_format"):
				df_format_index = field_rules.index(rule)
				date_format = field_rules[df_format_index].split(":")[1]

		 #or if there is no date_format rule assigned then use a default format for validation
		 if not date_format:
			date_format = '%m/%d/%Y'

		 try:
			date_entered = datetime.datetime.strptime(data[field_name], date_format).date()
			after_date = datetime.datetime.strptime(after_date_value, date_format).date()
			if date_entered <= after_date:
				 errs.append(field_name + self.error_message_templates['before'] + rule)
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 except ValueError:
			 errs.append(sys.exc_info()[1])
		 return errs

	def __validate_integer_fields(self, data, field_name):
		"""Used for validating integer fields, returns a list of error messages"""

		errs = []
		try:
			if not data[field_name].isdigit():
				errs.append(field_name + self.error_message_templates['digits'])
		except KeyError:
			errs.append("No Field named " + field_name + " to validate for integer value")
		return errs


	def __validate_email_fields(self, data, field_name):
		"""Used for validating email fields, returns a list of error messages"""

		comp_re = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
		errs = []
		try:	
			result = comp_re.match(data[field_name])
		except KeyError:
			errs.append(self.error_message_templates['no_field'] + field_name)
			result = "error"

		#in case the re did not match or their was a key error
		if not result:
			errs.append(field_name + self.error_message_templates['email'])
		return errs


	def __validate_regex_fields(self, data, field_name, rule):
		"""Used for validating field data to match a regular expression, returns a list of error messages"""

		regex = str(rule.split(':')[1])
		comp_re = re.compile(regex)

		errs = []
		try:	
			result = comp_re.match(data[field_name])
		except KeyError:
			errs.append(self.error_message_templates['no_field'] + (field_name))
			result = "error"

		#in case the re did not match or their was a key error
		if not result:
			errs.append(field_name + self.error_message_templates['regex'] + regex)
		return errs


	def __validate_present_fields(self, data, field_name):
		"""Used for validating present fields, returns a list of error messages"""

		errs = []
		try:
			if not data.has_key(field_name):
				errs.append(self.error_message_templates['present'] + field_name + " field")	
		except KeyError:
			errs.append(self.error_message_templates['present'] + field_name + " field")
			
		return errs

	def __validate_boolean_fields(self, data, field_name):
		"""Used for validating boolean fields, returns a list of error messages"""

		errs = []

		bool_values = [1,0,"1","0","false","true",False,True]
		try:
			if data[field_name] not in bool_values:
				errs.append(field_name + self.error_message_templates['boolean'] + str(bool_values))
		except KeyError:
			errs.append(self.error_message_templates['no_field'] + field_name)
		return errs

	def __validate_ip_fields(self, data, field_name):
		"""Used for validating fields having IP Address, returns a list of error messages"""

		comp_re = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

		errs = []
		try:
			result = comp_re.match(data[field_name])
		except KeyError:
			errs.append(self.error_message_templates['no_field'] + field_name)
			result = "error"

		#in case the re did not match or their was a key error
		if not result:
			errs.append(field_name + " must be a valid IP address")
		return errs

	def __validate_phone_fields(self, data, field_name):
		 """Used for validating fields having phone numbers, returns a list of error messages"""

		 comp_re = re.compile(r'^(?:\+?93)?[07]\d{9,13}$')

		 errs = []
		 try:
			 result = comp_re.match(data[field_name])
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
			 result = "error"

		#in case the re did not match or their was a key error
		 if not result:
			 errs.append(field_name + self.error_message_templates['phone'])
			
		 return errs

	def __validate_website_fields(self, data, field_name):
		 """Used for validating fields having website addresses, returns a list of error messages"""

		 comp_re = re.compile(r'(http(s)?://)?([\w-]+\.)+[\w-]+[\w-]+[\.]+[\.com]+([./?%&=]*)?', re.IGNORECASE)
		 errs = []

		 try:
		 	 result = comp_re.match(data[field_name])
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
			 result = "error"

		#in case the re did not match or their was a key error
		 if not result:
			 errs.append(field_name + self.error_message_templates['website'])

		 return errs

	def __validate_alpha_fields(self, data, field_name):
		 """Used for validating fields for alphabets only, returns a list of error messages"""

		 errs = []
		 try:
		 	 if not data[field_name].isalpha():
				  errs.append(field_name + self.error_message_templates['alpha'])
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		
		 return errs

	def __validate_alpha_num_fields(self, data, field_name):
		 """Used for validating fields for alphabets and numbers, returns a list of error messages"""

		 errs = []
		 try:
		 	 if not data[field_name].isalnum():
				errs.append(field_name + self.error_message_templates['alpha_num'])
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)

		 return errs

	def __validate_max_fields(self, data, field_name, rule):
		 """Used for validating fields for a maximum integer value, returns a list of error messages"""

		 #retrieve the value for that max rule
		 max_value = int(rule.split(':')[1])

		 errs = []
		 try:
			 if data[field_name].isdigit():
				 if int(data[field_name]) > max_value:
					 errs.append(self.error_message_templates['max'] + field_name+ " can be " + str(max_value))
			 else:
				 if len(data[field_name]) > max_value:
					 errs.append("The maximum number of characters in the value of the " + field_name + " can be " + str(max_value)+" characters")
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)

		 return errs

	def __validate_min_fields(self, data, field_name, rule):
		 """Used for validating fields for a minimum integer value, returns a list of error messages"""

		 #retrieve the value for that min rule
		 min_value = int(rule.split(':')[1])

		 errs = []
		 try:
			if data[field_name].isdigit():
				if int(data[field_name]) < min_value:
					errs.append("The minimum value of the " + field_name + " can be " + str(min_value))
			else:
				if len(data[field_name]) < min_value:
					errs.append(self.error_message_templates['min'] +" for field "+ field_name + " must be atleast " + str(min_value)+" characters")
		 except KeyError:
			errs.append(self.error_message_templates['no_field'] + field_name)

		 return errs

	def __validate_confirmed_fields(self, data, field_name):
		 """if the field under validation is password, a matching password_confirmation field must be present in the data, returns a list of error messages"""

		 errs = []
		 confirmation_field = field_name+"_confirmation"

		 try:
			 if confirmation_field not in data.keys():
				 errs.append(field_name + self.error_message_templates['confirmed'] + confirmation_field)
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 return errs

	def __validate_size_fields(self, data, field_name, rule):
		 """Used for validating fields for a maximum number of characters in a string value, returns a list of error messages"""

		 #retrieve the value for that size rule
		 size_value = int(rule.split(':')[1])

		 errs = []
		 try:
			 if len(data[field_name]) >= size_value:
				 errs.append(self.error_message_templates['size'] + field_name + " can be " + str(size_value))
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)

		 return errs

	def __validate_not_in_fields(self, data, field_name, rule):
		 """Used for validating fields for some number of values to avoid, returns a list of error messages"""

		 #retrieve the value for that not_in rule
		 ls = rule.split(':')[1].split(',')
		 errs = []

		 try:
			 if data[field_name] in ls:
				 errs.append(field_name + self.error_message_templates['not_in'] + str(ls))
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)

		 return errs

	def __validate_in_fields(self, data, field_name, rule):
		 """Used for validating fields for some number of values to allow, returns a list of error messages"""

		 #retrieve the value for that in rule
		 ls = rule.split(':')[1].split(',')
		 errs = []

		 try:
			 if data[field_name] not in ls:
				 errs.append(field_name + self.error_message_templates['in'] + str(ls))
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 return errs


	def __validate_different_fields(self, data, field_name, rule):
		 """Used for validating fields whose value should be different than the value of some other field, returns a list of error messages"""

		 #retrieve the value for the different rule
		 ls = rule.split(':')[1].split(',')
		 errs = []

		 try:
			 if data[field_name] == data[ls[0]]:
				 errs.append(field_name+ self.error_message_templates['different'] + str(ls[0]))
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 except Exception:
			 errs.append("Error Occured",sys.exc_info())
 		 
		 return errs

	def __validate_same_fields(self, data, field_name, rule):
		 """Used for validating fields whose value should be the same as some other field value, returns a list of error messages"""

		 #retrieve the value for the same rule
		 ls = rule.split(':')[1].split(',')
		 errs = []

		 try:
			 if data[field_name] != data[ls[0]]:
				 errs.append(field_name+ self.error_message_templates['same'] + str(ls[0]))
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 return errs


	def __validate_between_fields(self, data, field_name, rule):
		 """Used for validating fields for a number between two digits to allow, returns a list of error messages"""

		 #retrieve the value for the between rule
		 ls = rule.split(':')[1].split(',')
		 errs = []

		 try:
			 if int(data[field_name]) < int(ls[0]) or int(data[field_name]) > int(ls[1]):
				 errs.append(field_name+ self.error_message_templates['between'] + ls[0] +" and "+ls[1])
		 except KeyError:
			 errs.append(self.error_message_templates['no_field'] + field_name)
		 except ValueError:
			 errs.append(field_name + " can not be empty")
		 return errs

	def is_valid(self, data, rules):
		"""Validates the data according to the rules, returns True if the data is valid, and False if the data is invalid"""

		errors = self.validate(data,rules)
		self.errors = errors

		return not len(errors) > 0
			