from ultralytics import YOLO

model = YOLO("yolov11l-face.pt")
def detect_face(img_path, output_file):
  results = model.predict(img_path, device=0, conf=0.3)
  for result in results:
      result.save_crop("crops", output_file)
      print(result.verbose())
