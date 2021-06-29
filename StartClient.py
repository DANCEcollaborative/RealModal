from common.Configuration import load_yaml
from components.stomp import *
from components.client import *
import _thread
import time

if __name__ == "__main__":
    # Get configurations
    # TODO: add support for argparse
    config_path = "config/config.yaml"
    config = load_yaml(config_path)

    if "client" in config:
        # Initialize communication manager to receive massage from ActiveMQ.
        GV.register("stomp_manager", CM())

        # Initialize messengers
        for key in config["client"]:
            messenger_cls = GV.get_messenger_class(key)
            assert messenger_cls is not None, f"Messenger name {key} not defined. Please register it before using."
            messenger = messenger_cls(config["client"][key])
            GV.register(f"stomp.{key}", messenger)
        # Start messengers
        for key in config["client"]:
            _thread.start_new_thread(GV.get(f"stomp.{key}").start, ())

    while not GV.get("ended"):
        time.sleep(2)


    """
    # Add components and start the listener.
    visualizer = ForwardVisualizer(GV.client_addr_in, GV.client_addr_out, "PSI_Python_Image")
    if GV.UseFaceRecognition:
        RFR = FaceRecognitionListener("FaceRecognition")
        visualizer.add(RFR)
    if GV.UseOpenpose:
        ROP = OpenPoseListener("OpenPose")
        visualizer.add(ROP)
    if GV.UsePosition:
        RPD = PositionDisplayListener("Position")
        visualizer.add(RPD)

    if GV.UseDepthCamera:
        LQ = LocationQuerier("PSI_Python_AnswerKinect", "Python_PSI_QueryKinect")
        GV.LocationQuerier = LQ

    visualizer.start()

    DL = DialogMessenger("PSI_Bazaar_Text", "Python_PSI_Text", **GV.DialogAgentInfo)

    # Block the main process.
    while not GV.ended:
        s = input()
        if s == "end":
            GV.ended = True
            break
        DL.process_text(s)
        # time.sleep(2)
        # pass
    """
    exit(0)
