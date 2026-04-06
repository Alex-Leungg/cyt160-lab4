import paho.mqtt.client as mqtt
import ssl, time, json

BROKER = '<AWS_VM_IP>' # replace with current session IP
PORT = 8883 # TLS port
TOPIC = 'iot/lab/topic'
CA = '/home/alexleung/mqtt-certs/ca.crt'
CERT = '/home/alexleung/mqtt-certs/client.crt'
KEY = '/home/alexleung/mqtt-certs/client.key'

client = mqtt.Client(client_id='rpi-tls-client')

# Configure TLS — provide the CA to verify the broker, and our
# client certificate so the broker can verify us (mutual TLS)
client.tls_set(
	ca_certs=CA,
	certfile=CERT,
	keyfile=KEY,
	tls_version=ssl.PROTOCOL_TLSv1_2
)

client.tls_insecure_set(True)

print('[*] Connecting to broker with TLS...')
client.connect(BROKER, PORT, 60)
print('[*] Connected.')

for i in range(10):
	payload = json.dumps({"device": "rpi-tls-client", "temp": 20 + i * 0.5, "unit": "C"})
	client.publish(TOPIC, payload)
	print(f' Sent: {payload}')
	time.sleep(1)

client.disconnect()
print('[*] Done.')
