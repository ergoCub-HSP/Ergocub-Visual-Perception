import os
from logging import INFO
from action_rec.focus.gaze_estimation.focus import FocusDetector
from utils.concurrency.generic_node import GenericNode
from utils.concurrency.ipc_queue import IPCQueue
from utils.concurrency.py_queue import PyQueue
from utils.concurrency.yarp_queue import YarpQueue
from utils.confort import BaseConfig


class Logging(BaseConfig):
    class Logger:
        class Params:
            level = INFO  # Minimum logging level or list of logging levels
            recurring = False

    debug = True
    # options: rgb depth mask 'fps center hands partial scene reconstruction transform


class Network(BaseConfig):
    node = GenericNode

    class Args:
        in_queues = {
            'rgb': YarpQueue(remote_port_name='/depthCamera/rgbImage:r', local_port_name='/Focus/rgbImage:i',
                             data_type='rgb', read_format='rgb'),
        }

        out_queues = {
            'visualizer': PyQueue(ip="localhost", port=50000, queue_name='visualizer',
                                  write_format={'focus': None, 'face_bbox': None}),
            'rpc': IPCQueue(ipc_key=1234, write_format={'focus': False})
        }


class FOCUS(BaseConfig):
    model = FocusDetector

    class Args:
        area_thr = 0.03  # head bounding box must be over this value to be close
        close_thr = -0.95  # When close, z value over this thr is considered focus
        dist_thr = 0.3  # when distant, roll under this thr is considered focus
        foc_rot_thr = 0.7  # when close, roll above this thr is considered not focus
        patience = 3  # result is based on the majority of previous observations
        sample_params_path = os.path.join("action_rec", "focus", "gaze_estimation", "assets",
                                          "sample_params.yaml")
