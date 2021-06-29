from common.GlobalVariables import GV
from components.client.RemoteListener import BaseRemoteListener
import cv2

from Socket.Client import DataTransmissionClient as DTC
from utils.LoggingUtil import logging
from common.Geometry import *


@GV.register_listener("position")
class PositionDisplayListener(BaseRemoteListener):
    def __init__(self, config):
        super(PositionDisplayListener, self).__init__(config)

    def receive(self, socket: DTC):
        logging("In position display listener... receiving")
        prop_dict = self.receive_properties(socket)
        pos_num = socket.recv_int()
        print("%d position(s) to receive." % pos_num)
        to_send = str(pos_num) + ';' + str(prop_dict["timestamp"])
        time = GV.get("visualizer.sendtime", dict())
        print(len(GV.frame_process_time), GV.frame_process_time.keys())
        print(prop_dict['timestamp'])
        if prop_dict['timestame'] in time:
            print(f"For frame {prop_dict['timestamp']}, processing time: {time.time() - GV.frame_process_time[prop_dict['timestamp']]}")
            current_ts = prop_dict['timestamp']
            keys = GV.frame_process_time.keys()
            for key in list(keys):
                if key <= current_ts:
                    GV.frame_process_time.pop(key)
        raw_info = []
        person = []
        for i in range(pos_num):
            print("receiving person %d" % i)
            x0 = socket.recv_float()
            y0 = socket.recv_float()
            x = socket.recv_float()
            y = socket.recv_float()
            z = socket.recv_float()
            c = socket.recv_str()
            raw_info.append((x0, y0, x, y, z, c))
            print(f"received person {i}, location: ({x0}, {y0})")
        for i, (x0, y0, x, y, z, c) in enumerate(raw_info):
            if GV.UseDepthCamera:
                result = GV.LocationQuerier.query(None, prop_dict["timestamp"], Point2D(x0, y0))
                # result = camera[cid].camera_to_real
                if p_is_zero(result):
                    person.append((x, y, z))
                else:
                    person.append((result.x, result.y, result.z))
                to_send += f";person_{c}&{result.x}:{result.y}:{result.z}"
            else:
                person.append((x, y, z))
                to_send += f";person_{c}&{x}:{y}:{z}"
        logging(to_send)
        self.update_layout_image(GV.CornerPosition, person)
        GV.manager.send("Python_PSI_Location", to_send)
        return []

    def draw(self, img, buf):
        return img

    @staticmethod
    def draw_layout(corner, person):
        minx = min(map(lambda x: x[0], corner))
        miny = min(map(lambda x: x[1], corner))
        maxx = max(map(lambda x: x[0], corner))
        maxy = max(map(lambda x: x[1], corner))
        dis_x, dis_y = GV.display_size
        mar = GV.display_margin
        logging(person)

        def cov(x, y=None, z=None) -> (int, int):
            if type(x) == int:
                nx = int(mar + (x - minx) * (dis_x - 2 * mar) / (maxx - minx))
                ny = int(mar + (y - miny) * (dis_y - 2 * mar) / (maxy - miny))
            elif type(x) == Point3D:
                nx = int(mar + (x.x - minx) * (dis_x - 2 * mar) / (maxx - minx))
                ny = int(mar + (x.y - miny) * (dis_y - 2 * mar) / (maxy - miny))
            else:
                nx = int(mar + (x[0] - minx) * (dis_x - 2 * mar) / (maxx - minx))
                ny = int(mar + (x[1] - miny) * (dis_y - 2 * mar) / (maxy - miny))
            return ny, nx

        ret = np.ones((dis_x, dis_y, 3), dtype=np.uint8) * 240
        for i in range(len(corner)):
            cv2.line(ret, cov(corner[i]), cov(corner[(i + 1) % len(corner)]), (0, 0, 0), 2)
        for p in person:
            cv2.circle(ret, cov(p), 5, (0, 0, 255), cv2.FILLED)
        return ret

    def update_layout_image(self, corner, person):
        img = self.draw_layout(corner, person)
        cv2.imshow("Smart Room - Body Positions", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
