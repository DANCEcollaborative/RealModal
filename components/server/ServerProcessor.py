from common.GlobalVariables import GV

import time
import abc
import threading

from Socket.BaseSocket import BaseTCPSocket



@GV.register_processor("base")
class BaseImageProcessor(metaclass=abc.ABCMeta):
    def __init__(self, topic=None):
        # TODO: auto synchronize the topic(may not be possible)
        self.topic = topic
        self.current = None
        self.last_time = 0

    def base_send(self, soc: BaseTCPSocket):
        soc.send_str(f"type:{self.topic}:{self.current['camera_id']}")
        try:
            self.send(soc)
        except Exception as e:
            print(e)

    @abc.abstractmethod
    def send(self, soc: BaseTCPSocket):
        pass

    def base_process(self, info, pos, ip_addr):
        if time.time() - self.last_time < GV.process_freq:
            return
        print(f"Current state for {type(self)} at timestamp {info['timestamp']}: {GV.ProcessorState[pos]}")
        if GV.ProcessorLock[pos].acquire(blocking=False):
            GV.ProcessorState[pos] = f"Processing:{ip_addr}"
            self.current = info.copy()
            self.last_time = time.time()
            try:
                self.process(info)
                GV.ProcessorState[pos] = f"Pending:{ip_addr}"
            except Exception as e:
                print(e)
                GV.ProcessorState[pos] = "Available"
            finally:
                GV.ProcessorLock[pos].release()

    @abc.abstractmethod
    def process(self, info):
        pass






