from utils.GlobalVaribles import GlobalVariables as GV
from utils.LoggingUtil import logging

from utils.PositionCalcUtil import *

from communication.BaseListener import BaseListener
from communication.CommunicationManager import CommunicationManager as CM


class LocationQuerier(BaseListener):
    def __init__(self, cm: CM, topic_in=None, topic_out=None):
        super(BaseListener, self).__init__(cm)
        self.topic_in = topic_in
        self.topic_out = topic_out
        self.state = "Available"
        self.result = None
        self.subscribe_to(self.topic_in)

    def query(self, cid: str, timestamp: int, pixel: Point2D):
        self.state = "Querying"
        self.cm.send(self.topic_out, f"{timestamp};{pixel.x};{pixel.y}")
        while self.state != "Pending":
            pass
        self.state = "Available"
        return self.result

    def on_message(self, headers, msg):
        # TODO: add support for more cameras
        timestamp, x, y, z = msg.split(';')
        # transform to centimeters.
        self.result = Point3D(
            float(x),
            float(y),
            float(z)
        ) * 10
        self.state = "Pending"
