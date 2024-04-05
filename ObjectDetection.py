import cv2
import numpy as np

from pycoral.adapters.detect import get_objects
from pycoral.utils.edgetpu import run_inference


def detect (interpreter, img, labels, inference_sz, thres, k) :
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rgb_img = cv2.resize(rgb_img, inference_sz)
    
    run_inference(interpreter, rgb_img.tobytes())
    
    results = get_objects(interpreter, thres)[:k]
    
    return results


def append_results (img, inference_sz, results, labels) :
    h, w, c = img.shape
    s_x, s_y = w / inference_sz[0], h / inference_sz[1]
    
    for result in results :
        if result.id in [0, 2, 9, 12] :
            '''
            0 : person
            1 : bicycle
            2 : car
            3 : motorcycle
            9 : traffic light
            12 : stop sign
            14 : parking meter
            '''
            bbox = result.bbox.scale(s_x, s_y)
            
            x0, y0 = int(bbox.xmin), int(bbox.ymin)
            x1, y1 = int(bbox.xmax), int(bbox.ymax)
            
            score = int(100 * result.score)
            
            label = '{}% {}'.format(score, labels.get(result.id, result.id))
            
            img = cv2.rectangle(img, (x0,y0), (x1,y1), (255,255,255), 2)
            img = cv2.putText(img, label, (x0,y0 + 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,0), 2)
            
    return img