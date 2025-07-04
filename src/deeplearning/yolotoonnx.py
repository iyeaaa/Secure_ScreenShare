from ultralytics import YOLO

# 모델 로드
model = YOLO('best.pt')  # 또는 yolov8n.pt 등

# 전체 클래스 목록과 개수 출력
class_names = model.model.names  # {클래스ID: 클래스이름} 딕셔너리
print(f"모델이 학습한 전체 클래스 수: {len(class_names)}")
print("클래스 목록:")
for i, name in class_names.items():
    print(f"  {i}: {name}")
