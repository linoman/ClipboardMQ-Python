import pyperclip
import time
import threading


class Producer(threading.Thread):
	def __init__(self, queue, current_value):
		super(Producer, self).__init__()
		self._pause = 5
		self._stopping = False
		self._queue = queue
		self._current_value = current_value

	def run(self):
		while not self._stopping:
			# print 'Producer'
			if self._current_value != pyperclip.paste():
				self._current_value = pyperclip.paste()
				self._queue.put(pyperclip.paste())
				print ' [q] ' + pyperclip.paste()
			time.sleep(self._pause)

	def stop(self):
		self._stopping = True
