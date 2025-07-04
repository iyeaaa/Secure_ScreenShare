# from ultralytics import YOLO
# import cv2
# import os

# # 0. 학습된 모델 경로 설정
# MODEL_PATH = 'best.pt'  # 모델 파일 경로

# # 1. 모델 로드 (학습된 best.pt 파일 사용)
# if not os.path.exists(MODEL_PATH):
#     print(f"모델 파일을 찾을 수 없습니다: {MODEL_PATH}")
#     exit()

# model = YOLO(MODEL_PATH)

# # 2. 처리할 이미지 경로 지정
# IMG_NAME = 'test2.png'  # 테스트용 이미지 파일 이름
# IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)

# if not os.path.exists(IMG_PATH):
#     print(f"이미지 파일을 찾을 수 없습니다: {IMG_PATH}")
#     exit()

# # 3. YOLO 모델로 추론 수행
# results = model(IMG_PATH)[0]  # 단일 이미지이므로 인덱스 0 사용

# # 4. 원본 이미지 불러오기 (OpenCV BGR 포맷)
# img = cv2.imread(IMG_PATH)

# # 5. 결과 출력 및 시각화
# if len(results.boxes) > 0:
#     for box in results.boxes:
#         # 바운딩 박스 좌표 추출 (xyxy 포맷)
#         x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
#         cls_id = int(box.cls[0].item())    # 클래스 ID
#         conf = float(box.conf[0].item())   # 신뢰도

#         # 클래스명 조회
#         class_name = model.names[cls_id]

#         # 콘솔에 정보 출력
#         print(f"클래스: {class_name} | 신뢰도: {conf:.2f} | 좌표: ({x1}, {y1}), ({x2}, {y2})")

#         # 이미지에 박스 및 레이블 그리기
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 초록색 박스
#         label = f"{class_name} {conf:.2f}"
#         cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
# else:
#     print("감지된 카카오톡 아이콘이 없습니다.")

# # 6. 결과 이미지 저장
# output_path = os.path.join(os.getcwd(), 'result_kakaoicon.jpg')
# cv2.imwrite(output_path, img)
# print(f"시각화 결과가 '{output_path}'에 저장되었습니다.")

# # 7. (선택) 윈도우에 결과 표시
# cv2.imshow('YOLO KakaoIcon Detection', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
from ultralytics import YOLO
import cv2
import os

# 모델 경로 설정
MODEL_PATH = 'best.pt'  # 학습된 모델 파일 경로

# 모델 로드
if not os.path.exists(MODEL_PATH):
    print(f"[오류] 모델 파일을 찾을 수 없습니다: {MODEL_PATH}")
    exit()

model = YOLO(MODEL_PATH)

# 이미지 경로 설정
IMG_NAME = 'test1.png'  # 테스트할 이미지 이름
IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)

if not os.path.exists(IMG_PATH):
    print(f"[오류] 이미지 파일을 찾을 수 없습니다: {IMG_PATH}")
    exit()

# 라벨 파일 확인
LABEL_PATH = os.path.join(os.getcwd(), 'kakaoicon.txt')
if not os.path.exists(LABEL_PATH):
    print(f"[경고] 라벨 파일이 없습니다: {LABEL_PATH}")
else:
    with open(LABEL_PATH, 'r') as f:
        label_content = f.read().strip()
        print(f"[라벨 확인] {label_content}")

# YOLO 모델로 추론 수행
try:
    results = model(IMG_PATH)[0]
except Exception as e:
    print(f"[오류] 모델 추론 중 문제 발생: {e}")
    exit()

# 원본 이미지 불러오기
img = cv2.imread(IMG_PATH)

# 감지 여부 확인
if len(results.boxes) > 0:
    print("[정보] 감지된 객체 수:", len(results.boxes))
    for box in results.boxes:
        # 바운딩 박스 좌표 추출 (xyxy 포맷)
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cls_id = int(box.cls[0].item())    # 클래스 ID
        conf = float(box.conf[0].item())   # 신뢰도

        # 클래스명 조회
        class_name = model.names[cls_id]

        # 콘솔에 정보 출력
        print(f"[감지] 클래스: {class_name} | 신뢰도: {conf:.2f} | 좌표: ({x1}, {y1}), ({x2}, {y2})")

        if conf > 0.5:
            # 이미지에 박스 및 레이블 그리기
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 초록색 박스
            label = f"{class_name} {conf:.2f}"
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
else:
    print("[정보] 감지된 카카오톡 아이콘이 없습니다.")

# 결과 이미지 저장
output_path = os.path.join(os.getcwd(), 'result_kakaoicon.jpg')
cv2.imwrite(output_path, img)
print(f"[완료] 시각화 결과가 '{output_path}'에 저장되었습니다.")

# 윈도우에 결과 표시 (선택 사항)
cv2.imshow('YOLO KakaoIcon Detection', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
