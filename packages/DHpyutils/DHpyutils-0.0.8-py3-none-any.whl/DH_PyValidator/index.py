import re


class Validator:

	# 비밀번호 검증기능
	@staticmethod
	def validate_password(password: str):
		if re.search("[a-z]+", password) is None:
			return False
		elif re.search("[A-Z]+", password) is None:
			return False
		elif re.search("[`~!@#$%^&*(),<>/?]", password) is None:
			return False

		return True