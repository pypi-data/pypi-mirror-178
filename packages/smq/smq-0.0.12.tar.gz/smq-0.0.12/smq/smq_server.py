import sys
from multiprocessing.managers import BaseManager
from .brokers.simple_topic_agent import SimpleTopicAgent
from .brokers.unique_key_topic_agent import UniqueKeyTopicAgent
from flask import Flask
from flask import jsonify
from flask import redirect
from .common.protocol import DEFAULT_SIMPLE_AGENT_NAME
from .common.protocol import DEFAULT_UNIQUE_KEY_AGENT_NAME
from loguru import logger
import threading
import psutil

logger.remove()
# logger.add(sys.stderr, level='DEBUG')

app = Flask(__name__)

unique_key_agent = UniqueKeyTopicAgent()
simple_agent = SimpleTopicAgent()

@app.route('/')
def index():
    cpu_usage = psutil.cpu_percent()
    mem_used_percent = psutil.virtual_memory()[2]
    mem_used_gb = psutil.virtual_memory()[3]/1000000000
    resp = {
        'Info': {
            'The CPU usage is: ': f'{cpu_usage}%',
            'RAM memory used: ': f'{mem_used_percent}%',
            'RAM Used (GB): ': f'{round(mem_used_gb, 2)}'
        },
        'Topics': {
            'UniqueKeyAgent': unique_key_agent.info(),
            'SimpleAgent': simple_agent.info(),
        }
    }
    return jsonify(resp)

@app.route('/clear')
def clear():
    unique_key_agent.clear()
    simple_agent.clear()
    return redirect('/')


class QueueManager(BaseManager):
    pass


QueueManager.register(DEFAULT_SIMPLE_AGENT_NAME, SimpleTopicAgent)
QueueManager.register(DEFAULT_UNIQUE_KEY_AGENT_NAME, UniqueKeyTopicAgent)


class SmqServer():


    def __init__(self, api_port, queue_port, auth_key, log_level='INFO'):
        self._api_port = api_port
        self._queue_port = queue_port
        self._auth_key = auth_key
        logger.add(sys.stderr, level=log_level)

    def run(self):
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=self._api_port, debug=True, use_reloader=False), daemon=True).start()
        m = QueueManager(address=('0.0.0.0', self._queue_port), authkey=self._auth_key)
        s = m.get_server()
        s.serve_forever()


if __name__ == '__main__':
    smq_server = SmqServer(55555, 44444, b'abr')
    smq_server.run()
