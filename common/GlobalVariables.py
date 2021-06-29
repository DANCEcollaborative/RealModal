from common.Camera import *
from common.Geometry import Point3D


# TODO: use argparse to parse parameters in command line.
class GlobalVariables():
    """
    This is a global class which uses static variables to store hyperparameters and share temporary information between
    other classes
    """
    mapping = {
        "messenger_name_mapping": {},
        "listener_name_mapping": {},
        "processor_name_mapping": {},
        "running_value_mapping": {}
    }

    @classmethod
    def register_listener(cls, name):
        def wrap(listener_cls):
            cls.mapping["listener_name_mapping"][name] = listener_cls
            return listener_cls

        return wrap

    @classmethod
    def register_messenger(cls, name):
        def wrap(messenger_cls):
            cls.mapping["messenger_name_mapping"][name] = messenger_cls
            return messenger_cls

        return wrap

    @classmethod
    def register_processor(cls, name):
        def wrap(processor_cls):
            cls.mapping["processor_name_mapping"][name] = processor_cls
            return processor_cls

        return wrap

    @classmethod
    def get_listener_class(cls, name):
        return cls.mapping["listener_name_mapping"].get(name, None)

    @classmethod
    def get_messenger_class(cls, name):
        return cls.mapping["messenger_name_mapping"].get(name, None)

    @classmethod
    def get_processor_class(cls, name):
        return cls.mapping["processor_name_mapping"].get(name, None)

    @classmethod
    def register(cls, name, value):
        path = name.split(".")
        current = cls.mapping["running_value_mapping"]

        for part in path[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        current["__" + path[-1]] = value

    @classmethod
    def unregister(cls, name, default=None):
        path = name.split(".")
        current = cls.mapping["running_value_mapping"]

        for part in path[:-1]:
            if part not in current:
                return default
            current = current[part]
        return current.pop("__" + path[-1], default)

    @classmethod
    def get(cls, name, default=None):
        path = name.split(".")
        current = cls.mapping["running_value_mapping"]

        for part in path[:-1]:
            if part not in current:
                return default
            current = current[part]
        return current.get("__" + path[-1], default)


GV = GlobalVariables()

# Runtime variables

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

frame_process_time = {}

