# import cv2
# import torch
# import numpy as np
# from ultralytics import YOLO
# import mss

# def detect_and_mask_right_screen(model_path='best.pt', confidence_threshold=0.6, region_size=(800, 600)):
#     # 모델 로드
#     model = YOLO(model_path)
    
#     # 화면 캡처 설정
#     with mss.mss() as sct:
#         # 모니터 해상도 가져오기 (첫 번째 모니터 사용)
#         monitor = sct.monitors[1]
#         screen_width = monitor['width']
#         screen_height = monitor['height']

#         # 우상단 영역 계산
#         region = {
#             "top": 0,  # 상단 시작
#             "left": screen_width - region_size[0],  # 우측에서 시작
#             "width": region_size[0],
#             "height": region_size[1]
#         }

#         print(f"실시간 우상단 화면 탐지 및 우측 전체 마스킹 시작... (종료하려면 'q' 키를 누르세요)")

#         while True:
#             # 우상단 화면 캡처
#             screenshot = sct.grab(region)
#             frame = np.array(screenshot)

#             # BGR 형식으로 변환 (mss는 기본적으로 BGRA로 캡처)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

#             # 모델을 이용하여 탐지 수행
#             results = model(frame)

#             # 객체 탐지 여부 플래그
#             object_detected = False

#             # 탐지 결과를 프레임에 그리기
#             for result in results:
#                 boxes = result.boxes
#                 for box in boxes:
#                     confidence = float(box.conf[0])  # 신뢰도
#                     if confidence >= confidence_threshold:
#                         object_detected = True
#                         break
#                 if object_detected:
#                     break

#             # 객체가 탐지되면 우측 전체를 검은색으로 마스킹 처리
#             if object_detected:
#                 frame[:, region_size[0]//2:] = (0, 0, 0)

#             # 결과 화면 표시
#             cv2.imshow("YOLOv8n 실시간 우측 전체 마스킹 (신뢰도 90% 이상)", frame)

#             # 'q' 키를 누르면 종료
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         # 자원 해제
#         cv2.destroyAllWindows()

# # 실행 (우상단 부분: 너비 800, 높이 600)
# detect_and_mask_right_screen(model_path='best.pt', confidence_threshold=0.6, region_size=(800, 600))
# import cv2
# import torch
# import time
# import numpy as np
# from ultralytics import YOLO
# import mss

# def detect_screen(model_path='best.pt', confidence_threshold=0.9):
#     # 모델 로드
#     model = YOLO(model_path)
    
#     # 화면 캡처 설정
#     with mss.mss() as sct:
#         monitor = sct.monitors[1]  # 첫 번째 모니터 전체 영역

#         print("실시간 화면 탐지 시작... (종료하려면 'q' 키를 누르세요)")

#         while True:
#             # 화면 캡처
#             screenshot = sct.grab(monitor)
#             frame = np.array(screenshot)
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

#             # YOLO 탐지 수행
#             results = model(frame)

#             # 탐지 결과 처리
#             for result in results:
#                 boxes = result.boxes
#                 for box in boxes:
#                     conf = float(box.conf[0])
#                     if conf >= confidence_threshold:
#                         x1, y1, x2, y2 = map(int, box.xyxy[0])
#                         class_id = int(box.cls[0])
#                         label = model.model.names[class_id]

#                         # 사각형(경계 상자) 그리기
#                         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

#                         # 라벨 및 신뢰도 표시
#                         cv2.putText(frame, f'{label} {conf:.2f}', (x1, max(y1 - 10, 0)),
#                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            
#             # 화면 출력
#             cv2.imshow("YOLOv8 실시간 화면 탐지 (신뢰도 ≥ 90%)", frame)

#             # 종료 키
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cv2.destroyAllWindows()

# # 실행
# detect_screen(model_path='best.pt', confidence_threshold=0.9)

# import cv2
# import torch
# from ultralytics import YOLO

# def detect_realtime(model_path='best.pt', source=0, confidence_threshold=0.9):
#     # 모델 로드
#     model = YOLO(model_path)
    
#     # 비디오 캡처 객체 생성 (웹캠 기본: 0)
#     cap = cv2.VideoCapture(source)
    
#     if not cap.isOpened():
#         print("Error: 비디오 캡처를 열 수 없습니다.")
#         return

#     print("실시간 탐지 시작... (종료하려면 'q' 키를 누르세요)")

#     while True:
#         # 프레임 읽기
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: 프레임을 읽을 수 없습니다.")
#             break

#         # 모델을 이용하여 탐지 수행
#         results = model(frame)

#         # 탐지 결과를 프레임에 그리기
#         for result in results:
#             boxes = result.boxes
#             for box in boxes:
#                 confidence = float(box.conf[0])  # 신뢰도
#                 if confidence < confidence_threshold:
#                     continue  # 기준 미달은 무시

#                 x1, y1, x2, y2 = map(int, box.xyxy[0])  # 좌표 추출
#                 label = result.names[int(box.cls[0])]  # 클래스 이름
                
#                 # 탐지 결과 표시
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # 결과 화면 표시
#         cv2.imshow("YOLOv8n 실시간 탐지", frame)

#         # 'q' 키를 누르면 종료
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # 자원 해제
#     cap.release()
#     cv2.destroyAllWindows()

# # 실행
# detect_realtime(model_path='last.pt', source=0, confidence_threshold=0.9)

import cv2
import numpy as np
from ultralytics import YOLO
import mss

def detect_screen_top_right(model_path='best.pt', confidence_threshold=0.9):
    # 모델 로드
    model = YOLO(model_path)

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # 모든 모니터의 전체 화면

        print("실시간 화면 탐지 시작... (종료하려면 'q' 키를 누르세요)")

        while True:
            # 화면 캡처
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            height, width = frame.shape[:2]

            # ROI: 우측 상단 1000x300 영역만 추출
            roi_width, roi_height = 1500, 500
            x_roi = width - roi_width
            y_roi = 0
            roi = frame[y_roi:y_roi + roi_height, x_roi:x_roi + roi_width]

            # 탐지 수행 (우측 상단 영역만)
            results = model(roi)

            should_mask = False

            # 탐지 결과 처리
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    confidence = float(box.conf[0])
                    if confidence < confidence_threshold:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # 객체 중심이 ROI 내부에 있으면 마스킹 조건 만족
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    if center_x >= 0 and center_x <= roi_width and center_y >= 0 and center_y <= roi_height:
                        should_mask = True

            # 마스킹 조건 만족 시, 우측 상단 762x202 영역 마스킹
            if should_mask:
                mask_x = width - 800
                mask_y = 0
                frame[mask_y:mask_y + 300, mask_x:mask_x + 800] = 0

            # 전체 화면 표시
            cv2.imshow("YOLOv8 화면 탐지 (우측 상단만 분석)", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

# 실행
detect_screen_top_right(model_path='last.pt', confidence_threshold=0.9)
