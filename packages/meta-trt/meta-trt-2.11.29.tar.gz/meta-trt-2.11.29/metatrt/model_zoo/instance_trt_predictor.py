import cv2
import numpy as np
from ..utils import preproc, multiclass_nms, sigmoid
from ..utils import BaseEngine


class InstanceTrtPredictor(BaseEngine):
    def __init__(self, trt_file, image_size=(640, 640)):
        super(InstanceTrtPredictor, self).__init__(trt_file)
        self.image_size = image_size  # (h, w)
        self.mean = None
        self.std = None

    @staticmethod
    def get_rect(mask):
        h, w = mask.shape[:2]
        _, pred = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
        pred = 255 - pred
        contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) < 1:
            return [[0, 0], [0, w - 1], [h - 1, w - 1], [h - 1, 0]]

        area = [cv2.contourArea(c) for c in contours]
        max_idx = np.argmax(area)
        min_rect = cv2.minAreaRect(contours[max_idx])
        min_rect = cv2.boxPoints(min_rect)

        return min_rect

    def predict(self, origin_img, class_names, use_preprocess, conf, iou, end2end=False):
        img, ratio = preproc(origin_img, self.image_size, self.mean, self.std) if use_preprocess else (origin_img, 1.0)
        data = self.infer(img)
        # 处理box
        pred = np.reshape(data[-1], (1, -1, 38))[0]
        boxes = self.postprocess(pred, ratio=1., score_thr=conf, nms_thr=iou)
        # 处理mask
        proto = np.reshape(data[0], (1, 32, -1))[0]
        masks = np.reshape(sigmoid(np.dot(boxes[:, 6:], proto)), (-1, 160, 160))

        dets = []
        ih, iw = 160 / self.image_size[0], 160 / self.image_size[1]
        for mask, box, score, label in zip(masks, boxes[:, :4], boxes[:, 4], boxes[:, 5]):
            x1, y1, x2, y2 = box[0] * iw, box[1] * ih, box[2] * iw, box[3] * ih
            crop = mask[int(y1):int(y2) + 1, int(x1):int(x2) + 1] * 255
            min_rect = self.get_rect(crop.astype(np.uint8))
            rect = [[(r[0] + x1) / ih / ratio, (r[1] + y1) / iw / ratio] for r in min_rect]
            dets.append([int(rect[0][0]), int(rect[0][1]),
                         int(rect[1][0]), int(rect[1][1]),
                         int(rect[2][0]), int(rect[2][1]),
                         int(rect[3][0]), int(rect[3][1]),
                         float(score), int(label)])
        return dets

    @staticmethod
    def postprocess(predictions, ratio, score_thr, nms_thr):
        boxes = predictions[:, :4]
        scores = predictions[:, 4:5] * predictions[:, 5:6]
        masks = predictions[:, 6:]
        boxes_xyxy = np.ones_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
        boxes_xyxy /= ratio
        dets = multiclass_nms(boxes_xyxy, scores, nms_thr=nms_thr, score_thr=score_thr, masks=masks)
        return dets
