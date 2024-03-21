import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

# Necessary for AWS Tracking
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json


class GNSS_Subscriber(Node):
	
	def __init__(self):
		super().__init__('GNSS_Subscriber')
		self.subscription = self.create_subscription(NavSatFix, '/oxts/fix', self.rosbag_to_gnss, 10)
		self.previous_timestamp = 0

		#AWS Creds
		host = 'a32jbwrpvrfs4f-ats.iot.us-west-2.amazonaws.com'
		rootCAPath = 'AmazonRootCA1.pem'
		certificatePath = 'certificate.pem.cert'
		privateKeyPath = 'private.pem.key'
		clientId = 'BELIV_AV_GPS'
		port = 8883
		self.topic = 'beliv/gps/simulator'

		self.myMQTTClient = None
		self.myMQTTClient = AWSIoTMQTTClient(clientId)
		self.myMQTTClient.configureEndpoint(host, port)
		self.myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		self.myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
		self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
		self.myMQTTClient.configureDrainingFrequency(2)
		self.myMQTTClient.configureConnectDisconnectTimeout(10)
		self.myMQTTClient.configureMQTTOperationTimeout(15)

		self.myMQTTClient.connect()
		

	def rosbag_to_gnss(self, msg):
		if(msg.header.stamp.sec != self.previous_timestamp):
			devicePayload = {
                'deviceId': 'BELIV_AV_GPS',
                'timestamp': msg.header.stamp.sec,
                'latitude': msg.latitude,
                'longitude': msg.longitude,
            }
			self.get_logger().info("I heard: %s" %devicePayload)
			self.myMQTTClient.publish(self.topic, json.dumps(devicePayload), 1)
			self.previous_timestamp = msg.header.stamp.sec



def main(args=None):
	rclpy.init(args=args)
	converter = GNSS_Subscriber()
	rclpy.spin(converter)
	converter.destroy_node()
	rclpy.shutdown()

if __name__=='__main__':
	main()
