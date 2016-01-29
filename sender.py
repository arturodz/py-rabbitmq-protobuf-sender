import pika
import proto.log_pb2
import sys

def Main():
    log = proto.log_pb2.Log()
    log.service = "Python"
    log.instance = "ins1.entropy.tech"
    log.message = "Testing logs"
    log.trace = "Very long trace :O"
    return log

msg = Main().SerializeToString()

parameters = pika.URLParameters('amqp://guest:guest@172.17.0.3:5672/')
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.3',
                                                                5672,
                                                                '/',
                                                                credentials))
channel = connection.channel()
channel.queue_declare(queue='logger')
channel.basic_publish(exchange='',
                      routing_key='logger',
                      body=msg)
print(" [x] Sent 'Hello World!'")
connection.close()
