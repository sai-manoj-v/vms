import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

# Necessary for AWS Tracking
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import random
import json, subprocess, psutil
import time, datetime
import math



import csv

file = open('test2.csv', 'a', newline='')
writer = csv.writer(file)
index = ["Sec", "Nanosec", "Latitude (degrees)", "Longitude (degrees)", "Altitude (m)"]
writer.writerow(index)


class GNSS_Subscriber(Node):
	def __init__(self):
		super().__init__('GNSS_Subscriber')
		self.subscription = self.create_subscription(NavSatFix, '/oxts/fix', self.rosbag_to_gnss, 10)
		self.count = 0
		self.previous_timestamp = 0
		

	def rosbag_to_gnss(self, msg):
		gnss_data = []
		if(msg.header.stamp.sec == self.previous_timestamp):
			self.count = self.count+1	
			if(self.count<=10):
				gnss_data = [msg.header.stamp.sec, msg.header.stamp.nanosec, msg.latitude, msg.longitude, msg.altitude]
				self.get_logger().info("I heard: %s" %gnss_data)
				writer.writerow(gnss_data)
				self.previous_timestamp = msg.header.stamp.sec
				
		else:
			self.count = 1
			gnss_data = [msg.header.stamp.sec, msg.header.stamp.nanosec, msg.latitude, msg.longitude, msg.altitude]
			self.get_logger().info("I heard: %s" %gnss_data)
			writer.writerow(gnss_data)
			self.previous_timestamp = msg.header.stamp.sec

	def publish_location(self):
		host = 'a32jbwrpvrfs4f-ats.iot.us-west-2.amazonaws.com'
		rootCAPath = '../../Certificates/BELIV_AV_EDGE/AmazonRootCA1.pem'
		certificatePath = '../../Certificates/BELIV_AV_EDGE/certificate.pem.cert'
		privateKeyPath = '../../Certificates/BELIV_AV_EDGE/private.pem.key'
		clientId = 'BELIV_AV_GPS'
		port = 8883
		topic = 'beliv/gps/vehicle'

		# Configurations for IoT core Connection
		myMQTTClient = None
		myMQTTClient = AWSIoTMQTTClient(clientId)
		myMQTTClient.configureEndpoint(host, port)
		myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		myMQTTClient.configureDrainingFrequency(2)
		myMQTTClient.configureConnectDisconnectTimeout(10)
		myMQTTClient.configureMQTTOperationTimeout(15)



def main(args=None):
	rclpy.init(args=args)

	converter = GNSS_Subscriber()

	rclpy.spin(converter)

	converter.destroy_node()

	rclpy.shutdown()

	file.close()

if __name__=='__main__':
	main()
