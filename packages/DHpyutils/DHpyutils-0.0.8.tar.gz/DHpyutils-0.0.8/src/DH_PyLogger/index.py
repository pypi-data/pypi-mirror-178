from datetime import datetime


class Log:

	def __init__(self, *args):
		self.now = datetime.now()

	@classmethod
	def d(cls, *message: any):
		print("\n")
		print("-" * 50, "DEBUG START", "-" * 47)
		print(f"DateTime : {cls().now} \n")
		for msg in message:
			print(msg)
		print("-" * 50, " DEBUG END", "-" * 48)
		print("\n")

