import argparse
import time
import os
import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.adapters.common import input_size

from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

import ObjectDetection
import laneDetection
import ultraSonic

import backWheel
import frontWheel


def main():
  default_path = "/home/pi/adeept_picar-b/coral/pycoral/test_data"
  model_path = "ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
  label_path = "coco_labels.txt"
  thres = 0.53
  top_k = 3

  # argument parsing
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  
  parser.add_argument('--model', type=str,
                      help='File path of .tflite file',
                      default=os.path.join(default_path, model_path))
  parser.add_argument('--labels', help='File path of labels file', type=str,
                      default=os.path.join(default_path, label_path))
  parser.add_argument('--threshold', type=float, default=thres,
                      help='Score threshold for detected objects')
  parser.add_argument('--top_k', type=int, default=top_k,
                      help='Score threshold for detected objects')
  # parser.add_argument('-c', '--count', type=int, default=5,
  #                     help='Number of times to run inference')

  args = parser.parse_args()
  

  # model init
  labels = read_label_file(args.labels) if args.labels else {}
  
  interpreter = make_interpreter(args.model)
  interpreter.allocate_tensors()
  inference_sz = input_size(interpreter)
  
  thres = args.threshold
  
  k = args.top_k

  # camera init
  camera = PiCamera()
  camera.resolution = (640, 480)
  camera.framerate = 60
  rawCapture = PiRGBArray(camera, size=(640, 480))
  
  time.sleep(0.1)
  
  # ultrasonic init
  ultraSonic.init()
  
  # motor init
  
  # servo motor init
  SPEED = 90
  ANGLE = 110
  curr_steering_angle = 110
  backWheel.setup()
  frontWheel.servo_angle(0, ANGLE)
  backWheel.move(SPEED)

  print('----INFERENCE----')
  print('Note: The first inference is slow because it includes',
        'loading the model into Edge TPU memory.')
  try :
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True) :
      
      # img = frame.array.copy()
      img = frame.array
      
      # OD
      detected_results = ObjectDetection.detect(interpreter, img, labels, inference_sz, thres, k)
      
      # result_lst = ObjectDetection.append_results(img, inference_sz, detected_results, labels)
      # cv2.imshow('detected', result_lst), cv2.waitKey(1)
      
      # # LD
      lane_detected_results = laneDetection.get_lane_lines(img)
      if laneDetection.is_corner(lane_detected_results) and len(lane_detected_results) == 1 :
        print("CORNER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

      blended_img = laneDetection.show_image(img, detected_results, lane_detected_results, inference_sz, labels)
      cv2.imshow('detected', blended_img), cv2.waitKey(1)
      
      #steering
      #blend_frame, lane_lines = laneDetection.color_frame_pipeline(frames=frame, solid_lines=True, temporal_smoothing=True)
      blend_frame, steering_angle, no_lines = laneDetection.compute_steering_angle(blended_img, lane_detected_results)
      curr_steering_angle = laneDetection.stabilize_steering_angle(curr_steering_angle, steering_angle, no_lines)
      ANGLE = curr_steering_angle
      frontWheel.servo_angle(0, ANGLE)

      # UltraSonic
      dist = ultraSonic.checkdist() * 100
      print('%.2f' % dist)
      # dist max:96, min:13

      print('-------RESULTS--------')
      # if not lane_detected_results:
      #   print('No objects detected')

      # for obj in lane_detected_results:
      #   print(labels.get(obj.id, obj.id))
      #   print('  id:    ', obj.id)
      #   print('  score: ', obj.score)
      #   print('  bbox:  ', obj.bbox)
      rawCapture.truncate(0)
  finally :
    cv2.destroyAllWindows()
    camera.close()
    
    ultraSonic.cleanup()
    

if __name__ == '__main__':
  main()
