import pika
import pyperclip
import Queue
from libs.Producer import Producer
from libs.Consumer import Consumer


def callback(ch, method, properties, body):
	global producer
	if producer._current_value != body:
		print ' [r] ' + body
	pyperclip.copy(body)
	producer._current_value = pyperclip.paste()


try:
	parameters = pika.URLParameters('amqp://clipman:clipman123@linoman.net/ClipboardMQ')
	connection = pika.BlockingConnection(parameters)

	exchangeId = 'cmq.exchange.topic.transient'
	exchangeType = 'topic'
	producerRoutingKey = 'cmq.linoman'

	channel = connection.channel()
	channel.exchange_declare(exchange=exchangeId, type=exchangeType)
	result = channel.queue_declare(exclusive=True, auto_delete=True)
	queue_name = result.method.queue

	channel.queue_bind(exchange=exchangeId, queue=queue_name, routing_key=producerRoutingKey)

	print ' [*] ClipboardMQ is ready'
	channel.basic_consume(callback, queue=queue_name, no_ack=True)
	queue = Queue.Queue()

	producer = Producer(queue, pyperclip.paste())
	producer.start()

	consumer = Consumer(queue, channel, exchangeId, exchangeType, producerRoutingKey)
	consumer.start()

	channel.start_consuming()

except KeyboardInterrupt:
	connection.close()
	producer.stop()
	consumer.stop()
	print ' [*] ClipboardMQ is done'
