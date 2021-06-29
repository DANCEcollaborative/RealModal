from common.GlobalVariables import GV
from components.server.ServerProcessor import BaseImageProcessor
import threading

from Socket.BaseSocket import BaseTCPSocket
import base64


@GV.register_processor("openpose")
class OpenPoseProcessor(BaseImageProcessor):
    def __init__(self, topic=None):
        super(OpenPoseProcessor, self).__init__(topic)
        assert GV.opu is not None, "OpenPose should be initialized before using!"
        self.openpose = GV.opu
        self.poseKeypoints = None
        GV.locks["OpenPose"] = threading.Lock()

    def process(self, info):
        img = info['img']
        if img.shape[-1] == 4:
            img = img[:, :, :3]
        self.poseKeypoints, _ = self.openpose.find_pose(img)
        GV.locks["OpenPose"].acquire()
        GV.OpenPoseResult[info['camera_id']] = self.poseKeypoints.copy()
        GV.locks["OpenPose"].release()

    def send(self, soc: BaseTCPSocket):
        if len(self.poseKeypoints.shape) == 3:
            l = self.poseKeypoints.shape[0]
        else:
            l = 0
        print("find %d person(s) in the image" % l)
        soc.send_int(l)
        # Send poses only when there are at least one person detected.
        # This is because self.poseKeypoints will be a very weird value if no people is detected due to some features
        # or bugs in the  Openpose Library.
        if l > 0:
            soc.send_data(base64.b64encode(self.poseKeypoints.tostring()))
