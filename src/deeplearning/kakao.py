from ultralytics import YOLO

# 모델 로드 (YOLOv8n 사용)
model = YOLO('yolov8n.pt')

# 모델 학습
model.train(
    data='kakao.yaml',
    epochs=100,
    batch=16,
    imgsz=640,
    name='kakaoicon_detector'
)

print("[완료] 모델 학습이 완료되었습니다.")
