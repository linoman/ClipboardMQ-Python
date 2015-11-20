import time
import threading


class Consumer(threading.Thread):
	def __init__(self, queue, channel, exchangeId, exchangeType, routingKey):
		super(Consumer, self).__init__()
		self._pause = 5
		self._stopping = False
		self._queue = queue
		self._channel = channel
		self._exchangeId = exchangeId
		self._exchangeType = exchangeType
		self._routingKey = routingKey

	def run(self):
		while not self._stopping:
			# print 'Consumer'
			if not self._queue.empty():
				message = self._queue.get()
				self._channel.exchange_declare(exchange=self._exchangeId, type=self._exchangeType)
				self._channel.basic_publish(exchange=self._exchangeId, routing_key=self._routingKey, body=message)
				print ' [s] ' + message
			time.sleep(self._pause)

	def stop(self):
		self._stopping = True
