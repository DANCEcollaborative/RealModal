from common.GlobalVariables import GV
from components.server.ServerProcessor import BaseImageProcessor

from Socket.BaseSocket import BaseTCPSocket

from common.Geometry import *
from common.Color import get_color_name

import numpy as np


@GV.register_processor("position")
class PositionProcessor(BaseImageProcessor):
    def __init__(self, backend="Openpose", topic=None):
        super(PositionProcessor, self).__init__(topic)

        self.backendNotFound = False
        self.timestamp = None
        self.positions = []
        if backend.lower() not in ["openpose", "facerecognition"]:
            raise ValueError("Undefined backend.")
        self.backend = backend.lower()

    def process(self, info):
        self.timestamp = info["timestamp"]
        if self.backend == "openpose":
            self.process_openpose(info)
        elif self.backend == "facerecognition":
            self.process_face_rec(info)

    def process_face_rec(self, info):
        camera_ids = list(GV.CameraList.keys())
        # check whether face recognition is enabled
        if not GV.UseFaceRecognition:
            if not self.backendNotFound:
                self.backendNotFound = True
                raise RuntimeError("Face Recognition module not enabled.")
            return

        # check whether all cameras have updated results
        flag = False
        while not flag:
            flag = True
            for cid in camera_ids:
                flag = flag and (cid in GV.FaceRecognitionResult)
        GV.locks["FaceRecognition"].acquire()
        faces = GV.FaceRecognitionResult.copy()
        GV.locks["FaceRecognition"].release()

        if len(camera_ids) == 1:
            face_id, face_loc = faces[camera_ids[0]]
            self.positions = []
            for i, face in enumerate(face_loc):
                top, right, bottom, left = face
                x0, y0 = (right + left) / 2, (top + bottom) / 2
                h, w = info['img'].shape[:2]
                x0 = float(x0) / w
                y0 = float(y0) / h
                line_center = GV.CameraList[camera_ids[0]].image_mapping(Point2D(x0, y0))
                p_center = line_center.find_point_by_z(GV.SingleCameraDistance)
                self.positions.append((Point2D(x0, y0), p_center.to_vec()))
        else:
            # TODO: add position recognition when using several cameras.
            pass

    def process_openpose(self, info):
        # TODO: [URGENT!!] here, the info and GV.OpenPoseResult might not point to a same image.
        camera_ids = list(GV.CameraList.keys())
        # check whether face recognition is enabled
        if not GV.UseOpenpose:
            if not self.backendNotFound:
                self.backendNotFound = True
                raise RuntimeError("OpenPose module not enabled.")
            return

        # check whether all cameras have updated results
        flag = False
        while not flag:
            flag = True
            for cid in camera_ids:
                flag = flag and (cid in GV.OpenPoseResult)
        GV.locks["OpenPose"].acquire()
        keypoints = GV.OpenPoseResult.copy()
        GV.locks["OpenPose"].release()

        nose_index = 0
        neck_index = 1
        midhip_index = 8

        if len(camera_ids) == 1:
            self.positions = []
            cid = camera_ids[0]
            if len(keypoints[cid].shape) < 3:
                return
            for i, points in enumerate(keypoints[cid]):
                if not is_zero(points[neck_index]):
                    use_index = neck_index
                elif not is_zero(points[nose_index]):
                    use_index = nose_index
                elif not is_zero(points[midhip_index]):
                    use_index = midhip_index
                else:
                    continue
                x0, y0, _ = points[use_index]
                h, w = info['img'].shape[:2]

                # clothes color detection
                if is_zero(points[neck_index]):
                    cloth_color = "Unknown"
                else:
                    cropped_area = info['img'][int(y0)+5:int(y0)+15, int(x0)-5:int(x0)+5]
                    if sum(cropped_area.shape) > 0:
                        cropped_color = np.mean(cropped_area, (0, 1))
                        cloth_color = get_color_name(cropped_color)
                    else:
                        cloth_color = "Unknown"
                x0 = float(x0) / w
                y0 = float(y0) / h
                line_center = GV.CameraList[camera_ids[0]].image_mapping(Point2D(x0, y0))
                p_center = line_center.find_point_by_z(GV.SingleCameraDistance)
                self.positions.append(
                    (Point2D(x0, y0), GV.CameraList[cid].world_mapping(p_center).to_vec(), cloth_color)
                )
        else:
            # Determine which body key point is used to calculate positions
            num_nose = 0
            num_neck = 0
            num_midhip = 0
            for cid in camera_ids:
                for points in keypoints[cid]:
                    if not is_zero(points[nose_index]):
                        num_nose += 1
                    if not is_zero(points[neck_index]):
                        num_neck += 1
                    if not is_zero(points[midhip_index]):
                        num_midhip += 1
            use_index = 1
            if num_neck >= num_nose and num_neck >= num_midhip:
                use_index = neck_index
            elif num_nose >= num_midhip:
                use_index = nose_index
            else:
                use_index = midhip_index

            # Gather the line information
            start_point = []
            direction = []
            for cid in camera_ids:
                start_point.append(GV.CameraList[cid].pos_camera)
                direction.append([])
                for points in keypoints[cid]:
                    keypoint = points[use_index]
                    if not is_zero(keypoint):
                        direction[-1].append(GV.CameraList[cid].image_mapping(Point2D(keypoint[0], keypoint[1])))

            # Calculate position
            self.positions = calc_position(start_point, direction)

    def send(self, soc: BaseTCPSocket):
        soc.send_str(f"timestamp:int:{self.timestamp}")
        soc.send_str("END")
        l = len(self.positions)
        print(f"sending message for timestamp: {self.timestamp}")
        print("find %d person(s) in the space" % l)
        soc.send_int(l)
        for i, (p, (x, y, z), c) in enumerate(self.positions):
            print("sending person %d" % i)
            soc.send_float(p.x)
            soc.send_float(p.y)
            soc.send_float(x)
            soc.send_float(y)
            soc.send_float(z)
            soc.send_str(c)
