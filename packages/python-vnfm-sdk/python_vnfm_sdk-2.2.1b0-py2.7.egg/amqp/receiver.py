# Copyright (c) 2015 Fraunhofer FOKUS. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import ConfigParser
import logging
import threading

from utils.Utilities import get_map

import os
import pika

__author__ = 'lto'

log = logging.getLogger(__name__)


def on_request(ch, method, props, body):
    n = body
    response = on_message(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                         props.correlation_id, content_type='text/plain'),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.info("Answer sent")


def thread_function(ch, method, properties, body):
    threading.Thread(target=on_request, args=(ch, method, properties, body)).start()


def main(vnfManager):
    config_file_name = "/etc/openbaton/%s/conf.ini" % vnfManager.get('type')  # understand if it works
    log.debug(config_file_name)
    config = ConfigParser.ConfigParser()
    config.read(config_file_name)  # read config file
    _map = get_map(section='vnfm', config=config)  # get the data from map
    logging_dir = _map.get('log_path')

    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)

        logging.basicConfig(filename=logging_dir + '/%s-vnfm.log' % _map.get('type'), level=logging.INFO)

    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)

    logging.basicConfig(filename=logging_dir + '/ems-receiver.log', level=logging.INFO)
    queue_type = _map.get("type")  # get type of the queue
    hostname = _map.get("hostname")
    username = _map.get("username")
    password = _map.get("password")
    autodel = _map.get("autodelete")
    heartbeat = _map.get("heartbeat")
    exchange_name = _map.get("exchange")
    queuedel = True
    if autodel == 'false':
        queuedel = False
    if not heartbeat:
        heartbeat = '60'
    if not exchange_name:
        exchange_name = 'openbaton-exchange'

    rabbit_credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=_map.get("orch_ip"), credentials=rabbit_credentials,
                                  heartbeat_interval=int(heartbeat)))

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, type="topic", durable=True)
    # channel.queue_declare(queue='ems.%s.register'%queue_type, auto_delete=queuedel)
    channel.queue_declare(queue='vnfm.%s.actions' % hostname, auto_delete=queuedel)
    channel.queue_bind(exchange=exchange_name, queue='ems.%s.register' % queue_type)
    channel.queue_bind(exchange=exchange_name, queue='vnfm.%s.actions' % hostname)
    channel.basic_publish(exchange='', routing_key='ems.generic.register',
                          properties=pika.BasicProperties(content_type='text/plain'),
                          body='{"hostname":"%s"}' % hostname)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(thread_function, queue='vnfm.%s.actions' % hostname)
    print "Waiting for actions"
    channel.start_consuming()


if __name__ == '__main__':
    main()
