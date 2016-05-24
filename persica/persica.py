

import time
import connection

import queue
class Persica:
	def __init__(self):
		self.functions = {}
		self.queue = queue.Queue()
		self.conn = connection.Connection()
		self.conn.register_cmd_callbacks(self.parse_command)


	def register_function(self, handle, function):
		self.functions[handle] = function

	def execute_functions(self):
		while not self.queue.empty():
			fn = self.queue.get()
			fn()

	def parse_command(self, args):
		if args["cmd"] in self.functions:
			self.queue.put(self.functions[args["cmd"]])

def hello():
	print ("oh baby")
if __name__ == '__main__':
	app = Persica()
	app.register_function("red", hello)

	while (True):
		app.execute_functions()
		time.sleep(1)