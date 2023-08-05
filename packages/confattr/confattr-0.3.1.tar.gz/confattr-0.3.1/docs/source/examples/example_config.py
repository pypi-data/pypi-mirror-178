from confattr import Config

class Car:

	speed_limit = Config('traffic-law.speed-limit', 50, unit='km/h')

	def __init__(self) -> None:
		self.speed = 0

	def accelerate(self, value: int) -> None:
		new_speed = self.speed + value
		if new_speed > self.speed_limit:
			raise ValueError('you are going too fast')

		self.speed = new_speed
# ------- 01 -------
	def print_config(self) -> None:
		print('{key}: {val}'.format(key=type(self).speed_limit.key, val=self.speed_limit))
# ------- 02 -------
if __name__ == '__main__':
	from confattr import ConfigFile
	ConfigFile(lambda lvl, msg: print(msg), appname=__package__).load()

	c1 = Car()
	print('speed_limit: %s' % c1.speed_limit)
