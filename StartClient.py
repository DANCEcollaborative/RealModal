from common.Configuration import load_yaml
from components.messenger import *
from components.client import *
import _thread
import time

if __name__ == "__main__":
    # Get configurations
    # TODO: add support for argparse
    config_path = "config/config.yaml"
    config = load_yaml(config_path)

    if "room_corner" in config:
        corner_list = []
        for corner in config["room_corner"]:
            corner_list.append(Point3D(corner))
        GV.register("room.corner", corner_list)

    if "client" in config:
        # Initialize communication manager to receive massage from ActiveMQ.
        GV.register("stomp_manager", CM())

        # Initialize messengers
        for key in config["client"]:
            messenger_cls = GV.get_messenger_class(key)
            assert messenger_cls is not None, f"Messenger name {key} not defined. Please register it before using."
            messenger = messenger_cls(config["client"][key])
            GV.register(f"messenger.{key}", messenger)
        # Start messengers
        for key in config["client"]:
            _thread.start_new_thread(GV.get(f"messenger.{key}").start, ())

    while not GV.get("ended", True):
        time.sleep(2)
