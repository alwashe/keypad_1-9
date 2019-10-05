import paho.mqtt.client as mqtt
import time

pin = []
s = ''
first=True
second=False

def on_connect(client, userdata, flags, rc):
    client.subscribe("test12367/keypad")

def on_message(client, userdata, msg):
    global first
    global second
    global start_time
    if first:
        start_time = time.time()
        first = False
        second = True
    elif second:
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time = int(elapsed_time)
        start_time = time.time()
    if elapsed_time >= 10:
        start_time = time.time()
        pin.clear()
    msg.payload = msg.payload.decode("utf-8")
    if msg.payload in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        pin.append(msg.payload)
        if int(s.join((pin)))  > 999:
            client.publish("test12367/pin", s.join(map(str, pin)))
            del pin[0]
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()
