from common.Geometry import *
from common.GlobalVariables import GV
from components.stomp.BaseMessenger import BaseMessenger


@GV.register_messenger("location_querier")
class LocationQuerier(BaseMessenger):
    def __init__(self, config):
        """
        :param config:
            Configuration Dictionary.
            Topic from and to ActiveMQ should be included under "topic_in" and "topic_out" domains.
        """
        super(LocationQuerier, self).__init__(config)
        self.topic_in = self.config.topic_in
        self.topic_out = self.config.topic_out
        self.state = "Available"
        self.result = None
        self.subscribe_to(self.topic_in)

    def query(self, cid: str, timestamp: int, pixel: Point2D):
        self.state = "Querying"
        print("Send to topic: ", self.topic_out)
        print(f"Content: {timestamp};{pixel.x};{pixel.y}")
        self.cm.send(self.topic_out, f"{timestamp};{pixel.x};{pixel.y}")
        while self.state != "Pending":
            pass
        self.state = "Available"
        return self.result

    def on_message(self, headers, msg):
        # TODO: add support for more cameras
        print("Get location message from PSI:", msg)
        msg_split = msg.split(";")
        if msg_split[1] == "null":
            # Cannot get the location information from depth camera
            self.result = p_zero()
        else:
            timestamp, x, y, z = msg.split(';')
            # transform to centimeters.
            self.result = Point3D(
                float(x),
                float(y),
                float(z)
            )
        self.state = "Pending"
