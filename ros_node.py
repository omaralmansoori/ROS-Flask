from time import sleep
import rospy
import requests
from turtlesim.msg import Pose

TURTLE_NAME = "turtle1"
NODE_NAME = "Coord_Transmit"
SERVER_ADDRESS = ""
API_DELAY = 1

class Transmitter(object):
    def __init__(self):
        rospy.init_node(NODE_NAME, anonymous=True)
        self.sub = rospy.Subscriber(f'/{TURTLE_NAME}/pose', Pose, self.update, queue_size=10)
        self.rate = API_DELAY      
        self.pose = None

    def update(self, msg):
        self.pose = msg

    def transmit(self):
        r = rospy.Rate(self.rate)
        while self.pose == None:
            r.sleep()
        while not rospy.is_shutdown():
            self.publish(self.pose)
            r.sleep()

    def publish(self, pose):
        requests.post(f'{SERVER_ADDRESS}/{TURTLE_NAME}/{pose.x}/{pose.y}')

if __name__ == "__main__":
    TR = Transmitter()
    TR.transmit()