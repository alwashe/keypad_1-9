import appdaemon.plugins.hass.hassapi as hass
import paho.mqtt.client as mqtt
import time

pin = []                                                # List to save the pin
s = ''                                                  # seperator for the join command 1,2,3,4 -> 1234
first=True                                              # first run            
second=False                                            # folowing runs
domainTopic = "esp22"                               # name for the first topic              domainTopic/####
keypadTopic = "keypad/ScanCode"                                  # topicname for every keypress          domainTopic/keypadTopic
pinTopic = "pin"                                        # topicname for every pin               domainTopic/pinTopic
maxElapsedTime = 10

mqttHost = "192.168.178.204"
mqttUsername="xxxx"
mqttPassword="xxxx"




class PinConverter(hass.Hass):
    def initialize(self):
        self.log("Hello from AppDaemon")
        self.log("### PinConverter ###")
        client = mqtt.Client()                                                              # instance
        client.on_connect = self.on_connect                                                      # 
        client.on_message = self.on_message                                                      #
        client.username_pw_set(mqttUsername,mqttPassword)
        client.connect(mqttHost, 1883, 60)                                      # connect to server
        client.loop_forever()                                                               # loop

    def on_connect(self, client, userdata, flags, rc):            # callback for mqtt connection
        client.subscribe(domainTopic +"/" +keypadTopic)     # mqtt topic subscribe for keypad press

    def on_message(self, client, userdata, msg):                  # callback when receiving message
        global first                                        # var is eddited in module
        global second                                       # var is eddited in module
        global start_time                                   # var is eddited in module
        if first:                                           # first run, to save time for first keypress
            start_time = time.time()                        # save start time for elapsed time calculation between the keypresses
            first = False                                   # disable first run
            second = True                                   # enable second if for all following runs
        elif second:                                        # second and following keypress
            end_time = time.time()                          # save end time for elapsed time calculation between the keypresses
            elapsed_time = end_time - start_time            # elapsed time calculation
            elapsed_time = int(elapsed_time)                # convert elapsed time calculation to int
            start_time = time.time()                        # restart timer
        if elapsed_time >= maxElapsedTime:                  # reset pin after the definded elapsed time
            pin.clear()                                     # clear pin list
            start_time = time.time()                        # restart timer after pin reset
        msg.payload = msg.payload.decode("utf-8")                                       # convert 8-Byte format
        if msg.payload in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:                # accept only numbers between 1-9 (because 0 is send after every press)
            pin.append(msg.payload)                                                     # add number to pin list
            if int(s.join((pin)))  > 999:                                               # if when number has 4 digits
                client.publish(domainTopic +"/" +pinTopic, s.join(map(str, pin)))       # send pin to pin topic
                del pin[0]                                                              # del first entry of list to end new last digit in next run
