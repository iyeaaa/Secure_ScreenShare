# # 1. 필요 라이브러리 설치 (터미널에서 한 번만 실행)
# # pip install ultralytics opencv-python

# # 2. 코드 시작
# from ultralytics import YOLO
# import cv2

# # 모델 로드 (로컬에 yolov8n.pt 파일이 없으면 자동 다운로드됩니다)
# model = YOLO('yolov8n.pt')

# # 처리할 이미지 경로 지정
# img_path = 'kakaoicon.png'  # ← 사용자 환경에 맞게 경로 설정

# # YOLOv8n으로 추론 수행
# results = model(img_path)[0]  # 단일 이미지이므로 인덱스 0 사용

# # 원본 이미지 불러오기 (OpenCV BGR 포맷)
# img = cv2.imread(img_path)

# # 결과 출력 및 시각화
# for box in results.boxes:
#     # 바운딩 박스 좌표 추출
#     x1, y1, x2, y2 = map(int, box.xyxy[0])
#     cls_id = int(box.cls[0])            # 클래스 ID
#     conf  = float(box.conf[0])          # 신뢰도

#     # 클래스명 조회
#     class_name = model.names[cls_id]

#     # 콘솔에 정보 출력
#     print(f"클래스: {class_name}  |  신뢰도: {conf:.2f}  |  좌표: ({x1}, {y1}), ({x2}, {y2})")

#     # 이미지에 박스 및 레이블 그리기
#     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     label = f"{class_name} {conf:.2f}"
#     cv2.putText(img, label, (x1, y1 - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # 결과 이미지 저장
# output_path = 'result.jpg'
# cv2.imwrite(output_path, img)
# print(f"시각화 결과가 '{output_path}'에 저장되었습니다.")

# # (선택) 윈도우에 결과 표시
# cv2.imshow('YOLOv8n Detection', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# from ultralytics import YOLO

# model = YOLO('yolov8n.pt')
# print(model.names)
from ultralytics import YOLO
import os

# 1) 작업 디렉터리 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_YAML = os.path.join(BASE_DIR, 'kakaoicon.yaml')

# 2) 사전 학습된 nano 모델 불러오기
model = YOLO('yolov8n.pt')

# 3) 훈련 실행
#    epochs: 원하는 에폭 수로 조정
#    imgsz: 학습/추론 시 사용되는 이미지 해상도
#    name: runs/train/ 폴더 하위에 결과가 저장되는 experiment 이름
model.train(
    data=DATA_YAML,
    epochs=50,
    imgsz=640,
    batch=16,
    name='kakaoicon_detector'
)
