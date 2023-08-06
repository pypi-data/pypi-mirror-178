from datetime import datetime, timedelta


class D:

	def __init__(self):
		self.now = datetime.now()
		self.utc_now = datetime.utcnow()
		self.timedelta = 0

	@classmethod
	def get_now(cls, format: str = '%Y-%m-%d %H:%M:%S') -> str:
		return cls().now.strftime(format)

	@classmethod
	def get_year(cls, diff: int = 0) -> int:
		return int((cls().now + timedelta(days=diff)).strftime('%Y'))

	@classmethod
	def get_month(cls, diff: int = 0) -> int:
		return int((cls().now + timedelta(days=diff)).strftime('%m'))

	@classmethod
	def get_day(cls, diff: int = 0) -> int:
		return int((cls().now + timedelta(days=diff)).strftime('%d'))

	@classmethod
	def to_string(cls, target: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
		return datetime.strftime(target, format)

	@classmethod
	def to_date(cls, target: str, format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
		return datetime.strptime(target, format)

	@classmethod
	def calc_date(cls, diff: int, format: str = "%Y-%m-%d %H:%M:%S") -> str:
		return (cls().now + timedelta(days=diff)).strftime(format)

	# 초를 시간으로 환산하는 기능
	@staticmethod
	def conv_sec_to_datetime(sec: int) -> str:
		t1 = timedelta(seconds=sec)
		days = t1.days
		_sec = t1.seconds
		(hours, minutes, seconds) = str(timedelta(seconds=_sec)).split(':')
		hours = int(hours)
		minutes = int(minutes)
		seconds = int(seconds)

		result = []
		if days >= 1:
			result.append(str(days) + '일')
		if hours >= 1:
			result.append(str(hours) + '시간')
		if minutes >= 1:
			result.append(str(minutes) + '분')
		if seconds >= 1:
			result.append(str(seconds) + '초')
		return ' '.join(result)