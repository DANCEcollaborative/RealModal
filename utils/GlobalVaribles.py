from utils.Camera import WebcamMapping
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
    debug = True

    """
    Runtime variables
    """
    # Threading locks of different components.
    locks = dict()

    # Utilities that need to be pre-initialized.
    fru = None  # face recognition utility
    opu = None  # Openpose utility

    # Recent results from different components.
    OpenPoseResult = dict()
    FaceRecognitionResult = dict()

    # The server to send results back to client.
    send_server = None

    # The communication manager used by client to communicate with Psi.
    manager = None

    """
    Configurations:
    """
    UseOpenpose = False
    UseFaceRecognition = True
    UsePosition = True

    # Which backend is used to calculate position information
    PositionBackend = "FaceRecognition"

    # The ip address to establish sockets between clients and server.
    server_addr_in = ("128.2.204.127", 6416)
    server_addr_out = ("128.2.204.127", 6417)
    client_addr_in = ("brandy.lti.cs.cmu.edu", 6417)
    client_addr_out = ("brandy.lti.cs.cmu.edu", 6416)

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

    # Pixel-World mapping function for every camera.
    CameraMapping = {
        "webcam": WebcamMapping(
            pos_camera=Point3D(0, 0, 0),
            dir_camera=Point3D(0, 0, 1),
            dir_x=Point3D(1, 0, 0),
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
    CornerPosition = [
        (-50, -50, 55),
        (-50, 50, 55),
        (50, 50, 55),
        (50, -50, 55),
    ]

    #    CornerPosition = [
    #        (0, 0, 0),
    #        (378.2, 0, 0),
    #        (378.2, 416.7, 0),
    #        (0, 284.5, 0)
    #    ]

    """
    Display size: define the position display size. 
    """
    display_size = (500, 500)
    display_margin = 50
