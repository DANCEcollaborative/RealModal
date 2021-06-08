from utils.Camera import *
from utils.PositionCalcUtil import Point3D, Point2D, Line3D


# TODO: use argparse to parse parameters in command line.
class GlobalVariables():
    """
    This is a global class which uses static variables to store hyperparameters and share temporary information between
    other classes
    """

    """
    Debugging mode will output more log.
    Using logging() instead of print() to get debugging time log.
    """
    debug = False

    """
    Runtime variables
    """
    # The flag of whether the program has come to an end.
    ended = False

    # Threading locks of different components.
    locks = dict()

    # Utilities that need to be pre-initialized.
    fru = None  # face recognition utility
    opu = None  # Openpose utility

    # Processors
    Processor = []  # store the instances used for processing images
    ProcessorState = []  # store the states of the instances.
                         # values can be "Available", "Processing:{ip}" and "Pending:{ip}"
    ProcessorLock = []  # store possible locks used in processors

    # Recent results from different components.
    OpenPoseResult = dict()
    FaceRecognitionResult = dict()

    # The server to send results back to client.
    send_server = None

    # The communication manager used by client to communicate with Psi.
    manager = None

    # The listener used to query the mapping between color image and depth image.
    LocationQuerier = None

    # The utility used to get next idiom for the solitaire.
    IdiomUtil = None

    """
    Configurations:
    """
    PSIImageFormat = "jpg"

    UseOpenpose = True
    UseFaceRecognition = False
    UsePosition = True

    # Which backend is used to calculate position information
    PositionBackend = "OpenPose"

    # Whether to use data from depth camera to get people location.
    UseDepthCamera = False

    # Which Dialog Agent is used to response
    DialogAgentInfo = {
        "agent_type": "Solitaire",
        "url": "https://misty.lti.cs.cmu.edu/bazaar/login?roomName=diamondkatapsi&roomId=10010&id=1&username=yansen",
        "GUI": True,
    }

    # The ip address to establish sockets between clients and server.
    server_addr_in = ("128.2.204.127", 5416)
    server_addr_out = ("128.2.204.127", 5417)
    client_addr_in = ("brandy.lti.cs.cmu.edu", 5417)
    client_addr_out = ("brandy.lti.cs.cmu.edu", 5416)

    # The frequency that the server processes a frame.
    process_freq = 0.4

    """
    Camera information:
    """
    # TODO: load camera information from files rather than directly modifying here.
    #    CameraPosition = {
    #        "webcam": Point3D(0, 0, 0)
    #    }
    #    CameraCenterDirection = {
    #        "webcam": Point3D(0, 0, 1)
    #    }

    CameraList = {
        "webcam": WebCamera(
            pos_camera=Point3D(29.2, 12.7, 125.7),
            dir_camera=Point3D(357.1, 319.2, 19.08),
            dir_x=Point3D(-17.27, 19.26, 1.01284),
            theta=0.684644277715545,
            whratio=16. / 9
        )
    }

    # When using one camera only, the default distance to the camera
    SingleCameraDistance = 55.

    # Which cameras are visualized in client end.
    CameraToDisplay = ["webcam"]

    """
    Room information:
    """
    #CornerPosition = [
    #    (-50, -50, 55),
    #    (-50, 50, 55),
    #    (50, 50, 55),
    #    (50, -50, 55),
    #]

    CornerPosition = [
        (0, 0, 0),
        (378.2, 0, 0),
        (378.2, 416.7, 0),
        (0, 284.5, 0)
    ]

    """
    Display size: define the position display size.
    """
    display_size = (500, 500)
    display_margin = 50

    frame_process_time = {}