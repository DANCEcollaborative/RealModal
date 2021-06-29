from components.server.FaceRocognition import *
from components.server.Openpose import *
from components.server.Position import *


# TODO: change the add_processor logic
def add_processor(processor):
    GV.Processor.append(processor)
    GV.ProcessorState.append("Available")
    GV.ProcessorLock.append(threading.Lock())
