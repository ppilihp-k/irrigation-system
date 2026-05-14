# ---------------------------------------------------------------------------------------------------------------------
from json import loads
# ---------------------------------------------------------------------------------------------------------------------
file = open('/control_unit/mqtt_config.txt', 'r')
data = loads(file.read())
file.close()
#
# MQTT
#
URL: str = data['host']
PORT: int = data['port']
USER_NAME: str = data['user_name']
PASSWORD: str = data['password']
BASE_TOPIC: str = data['topic']

CLIENT_ID: str = data['client_id']
MQTT_KEEP_ALIVE: int = 60

# ---------------------------------------------------------------------------------------------------------------------
