from common.GlobalVariables import GV
from components.server.ServerProcessor import BaseImageProcessor
import threading

from Socket.BaseSocket import BaseTCPSocket


@GV.register_processor("face_recognition")
class FaceRecognitionProcessor(BaseImageProcessor):
    def __init__(self, topic=None):
        super(FaceRecognitionProcessor, self).__init__(topic)
        assert GV.fru is not None, "Face Recognizer should be initialized before using!"
        self.recognizer = GV.fru
        self.face_id = []
        self.face_loc = []
        GV.locks["FaceRecognition"] = threading.Lock()

    def process(self, info):
        img = info['img']
        if img.shape[-1] == 4:
            img = img[:, :, :3]
        self.face_id, self.face_loc = self.recognizer.recognize(img)
        GV.locks["FaceRecognition"].acquire()
        GV.FaceRecognitionResult[info['camera_id']] = (self.face_id, self.face_loc)
        GV.locks["FaceRecognition"].release()

    def send(self, soc: BaseTCPSocket):
        l = len(self.face_id)
        print("find %d face(s) in the image" % l)
        soc.send_int(l)
        for i in range(l):
            print("sending face %d" % i)
            soc.send_int(self.face_id[i])
            soc.send_int(self.face_loc[i][0])
            soc.send_int(self.face_loc[i][1])
            soc.send_int(self.face_loc[i][2])
            soc.send_int(self.face_loc[i][3])
