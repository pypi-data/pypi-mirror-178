import json
from datetime import datetime
import lxml
from kafka import KafkaProducer, KafkaConsumer

def Subscribe(ip: str, topic: str, duration: int, offset: str, callback: any):
    """
    Subscribe to a topic in the kafka server, and execute a callback function on each message read.

    :param ip: The IP of the Kafka server to subscribe
    :param topic: the kafka topic
    :param duration: the time duration (in seconds) for listening (-1 for infinite duration)
    :param offset: start reading from 'earliest' or 'latest' message recorded
    :param callback: function to execute on each message ( callback(result: dict) )
    """

    try:
        if (offset != 'earliest') and (offset != 'latest'):
            raise Exception("Offset must be 'earliest' or 'latest' only!")
        consumer = KafkaConsumer(topic, auto_offset_reset=offset,
                                     bootstrap_servers=[ip], consumer_timeout_ms=(duration * 1000))
        for msg in consumer:
            callback(json.loads(msg.value))
        if consumer is not None:
            consumer.close()
        else:
            raise Exception("Failed to create consumer!")
    except Exception as ex:
        print('Exception in subscribing to kafka. Reason: ' + str(ex) + "\n")

class MilabProducer:
    """
    A Kafka producer for Milab.
    Initialize with the Kafka server's ip, and Terminate when done.

    :param ip: The ip of the Kafka server.
    """
    def __init__(self, ip: str):
        self._producer = self.__initialize(ip)

    @staticmethod
    def __initialize(ip: str) -> KafkaProducer:
        """
        Initialize the kafka producer, Needed for the Publish method.

        IMPORTANT: After finished with the producer, call Producer.Terminate() to terminate the instance.

        :param ip: IP of the kafka server, depends on the computer the kafka runs from.

        :return: producer_instance object
        """

        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=[ip])
        except Exception as ex:
            print('Exception while connecting Kafka. Reason: ' + str(ex) + "\n")
        finally:
            return _producer

    def Publish(self, topic: str, data: dict):
        """
        Publish a message to the kafka server.
        Note: Automatically adds 'time' field to the dict with the publishing time.

        :param topic: the topic in the kafka server to publish to
        :param data: the message itself, as a dict
        """

        try:
            key = 'raw'
            data["time"] = datetime.now().strftime("%H:%M:%S")
            value = json.dumps(data)
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self._producer.send(topic, key=key_bytes, value=value_bytes)
            self._producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print('Exception in publishing message. Reason: ' + str(ex) + "\n")

    def Terminate(self):
        """
            Terminates the kafka producer.
        """

        if self._producer:
            self._producer.close()
            self._producer = None
