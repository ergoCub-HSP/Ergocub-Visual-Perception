import sys
from pathlib import Path

import cv2
import numpy as np
from loguru import logger
sys.path.insert(0,  Path(__file__).parent.parent.as_posix())
from utils.logging import setup_logger
from configs.sink_config import Logging, Network
print("SI scripts/sink.py")
from grasping.utils.misc import draw_mask, project_pc, project_hands
print("NO scripts/sink.py")
setup_logger(level=Logging.level)
@logger.catch(reraise=True)
class Sink(Network.node):
    def __init__(self):
        self.img = np.zeros([480, 640, 3], dtype=np.uint8)
        self.mask = None
        self.center = None
        self.hands = None
        self.fps = None
        self.distance = None
        self.focus = None
        self.pose = None
        self.bbox = None
        self.face_bbox = None
        self.actions = None
        self.edges = None
        self.is_true = None
        self.requires_focus = None
        self.requires_os = None
        self.last_n_actions = []  # TODO TEST
        super().__init__(**Network.Args.to_dict())

    def startup(self):
        # logo = cv2.imread('assets/logo.jpg')
        # logo = cv2.resize(logo, (640, 480))
        # cv2.imshow('Ergocub-Visual-Perception', np.array(logo, dtype=np.uint8))
        # cv2.waitKey(1)
        pass

    def loop(self, data: dict) -> dict:

        if 'rgb' in data.keys():
            self.img = data['rgb']
        img = self.img

        # GRASPING #####################################################################################################
        if 'mask' in data.keys():
            self.mask = data['mask']
        img = draw_mask(img, self.mask)

        if 'center' in data.keys():
            self.center = data['center']
        if self.center is not None:
            img = cv2.circle(img, project_pc(self.center)[0], 5, (0, 255, 0)).astype(np.uint8)

        if 'hands' in data.keys():
            self.hands = data['hands']
        if self.hands is not None:
            img = project_hands(img, self.hands[..., 0], self.hands[..., 1])

        # HUMAN ########################################################################################################
        if 'fps' in data.keys():
            self.fps = data['fps']
        if self.fps is not None:
            img = cv2.putText(img, f'FPS: {int(self.fps)}', (10, 20), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 1,
                              cv2.LINE_AA)

        if 'human_distance' in data.keys():
            self.distance = data['human_distance']
        if self.distance is not None:
            img = cv2.putText(img, f'DIST: {int(self.distance)}', (200, 20), cv2.FONT_ITALIC, 0.7, (255, 0, 0), 1,
                              cv2.LINE_AA)

        if 'focus' in data.keys():
            self.focus = data['focus']
        if self.focus is not None:
            img = cv2.putText(img, "FOCUS" if self.focus else "NOT FOCUS", (400, 20), cv2.FONT_ITALIC, 0.7,
                              (0, 255, 0) if self.focus else (0, 0, 255), 1, cv2.LINE_AA)

        if 'pose' in data.keys():  # and self.hands is None:
            self.pose = data["pose"]
            self.edges = data["edges"]
        if self.pose is not None:  # and self.hands is None:
            img = cv2.rectangle(img, (0, 430), (50, 480), (255, 255, 255), cv2.FILLED)
            for edge in self.edges:
                p0 = [int((p*50)+50) for p in self.pose[edge[0]][:2]]
                p1 = [int((p*50)+50) for p in self.pose[edge[1]][:2]]
                p0[1] += 405
                p1[1] += 405
                p0[0] += -25
                p1[0] += -25
                img = cv2.line(img, p0, p1, (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

        if 'bbox' in data:
            self.bbox = data["bbox"]
        if self.bbox is not None:  # and self.hands is None:
            x1, x2, y1, y2 = self.bbox
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        if 'focus' in data.keys():
            self.focus = data["focus"]
        if self.focus is not None:
            focus = self.focus
        else:
            focus = False

        if 'face_bbox' in data.keys():
            self.face_bbox = data["face_bbox"]
        if self.face_bbox is not None:
            x1, y1, x2, y2 = self.face_bbox
            color = (255, 0, 0) if not focus else (0, 255, 0)
            img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

        if 'actions' in data.keys():
            self.actions = data["actions"]
        if 'is_true' in data.keys():
            self.is_true = data["is_true"]
        if 'requires_focus' in data.keys():
            self.requires_focus = data['requires_focus']
        if 'requires_os' in data.keys():
            self.requires_os = data['requires_os']
        if self.actions is not None and self.hands is None:
            if len(self.actions) > 1:
                best = max(self.actions, key=self.actions.get)
                best_index = list(self.actions.keys()).index(best)
                # Temporal consistency start
                if len(self.last_n_actions) > 16:
                    self.last_n_actions = self.last_n_actions[1:]
                self.last_n_actions.append(best)
                if all([elem == self.last_n_actions[-1] for elem in self.last_n_actions]):
                # Temporal consistency end
                    if self.is_true > 0.66 or not self.requires_os[best_index]:
                        textsize = cv2.getTextSize(best, cv2.FONT_ITALIC, 1, 2)[0]
                        textX = int((img.shape[1] - textsize[0]) / 2)
                        text_color = (0, 255, 0) if not self.requires_focus[best_index] or (self.requires_focus[best_index] and focus) else (230, 172, 37)
                        img = cv2.putText(img, best, (textX, 450), cv2.FONT_ITALIC, 1, text_color, 2, cv2.LINE_AA)

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        cv2.imshow('Ergocub-Visual-Perception', img)
        cv2.setWindowProperty('Ergocub-Visual-Perception', cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)
        return {}


if __name__ == '__main__':
    source = Sink()
    source.run()
