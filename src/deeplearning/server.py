from flask import Flask, request, Response
from ultralytics import YOLO
import cv2
import os
import numpy as np
from PIL import Image # PIL은 다양한 이미지 포맷 처리에 유용
import io

app = Flask(__name__)

# --- 이전 Python 코드의 함수들 ---
MODEL_PATH = 'best.pt'  # 학습된 모델 파일 경로 (실제 경로로 수정)
yolo_model = None # 전역 변수로 모델 로드

def load_yolo_model_global():
    global yolo_model
    if not os.path.exists(MODEL_PATH):
        print(f"[오류] 모델 파일을 찾을 수 없습니다: {MODEL_PATH}")
        yolo_model = None
        return
    try:
        yolo_model = YOLO(MODEL_PATH)
        print(f"[정보] 모델 로드 완료: {MODEL_PATH}")
    except Exception as e:
        print(f"[오류] 모델 로드 중 문제 발생: {e}")
        yolo_model = None

def detect_and_mask_objects(model, image_bitmap):
    """
    이미지 비트맵에서 객체를 탐지하고, 검은색으로 마스킹 처리합니다.
    처리된 이미지 비트맵(NumPy 배열)을 반환합니다.
    """
    if model is None:
        print("[오류] detect_and_mask_objects: 모델이 유효하지 않습니다.")
        return image_bitmap # 원본 반환 또는 오류 처리
    if not isinstance(image_bitmap, np.ndarray):
        print("[오류] detect_and_mask_objects: 입력 이미지가 유효한 NumPy 배열이 아닙니다.")
        return image_bitmap # 원본 반환 또는 오류 처리

    # 객체 탐지를 위해 BGR 형식으로 가정 (OpenCV 기본)
    # 클라이언트에서 RGBA로 보냈다면 변환 필요
    # 예: image_bgr = cv2.cvtColor(image_bitmap, cv2.COLOR_RGBA2BGR)

    # 복사본에서 작업
    masked_image = image_bitmap.copy()
    detected_objects_list = []

    try:
        results = model(image_bitmap, verbose=False)[0] # verbose=False로 로그 줄이기
    except Exception as e:
        print(f"[오류] 모델 추론 중 문제 발생: {e}")
        return image_bitmap # 원본 반환

    if len(results.boxes) > 0:
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0].item())
            class_id = int(box.cls[0].item())
            class_name = model.names[class_id]

            if confidence > 0.5: # 신뢰도 임계값
                # 감지된 객체 영역을 검은색으로 채우기
                cv2.rectangle(masked_image, (x1, y1), (x2, y2), (0, 0, 0), cv2.FILLED)
                print(f"[Python 감지 및 마스킹] 클래스: {class_name}, 신뢰도: {confidence:.2f}")
    else:
        print("[Python 정보] 감지된 객체가 없습니다.")

    return masked_image


@app.route('/process_image_python', methods=['POST'])
def process_image_endpoint():
    global yolo_model
    if yolo_model is None:
        return Response("Model not loaded", status=500, mimetype='text/plain')

    if not request.data:
        return Response("No image data received", status=400, mimetype='text/plain')

    try:
        # 클라이언트(JavaScript)에서 보낸 이미지 크기 정보 가져오기
        width = int(request.headers.get('X-Image-Width'))
        height = int(request.headers.get('X-Image-Height'))

        # 요청 본문(raw bytes)을 NumPy 배열로 변환
        # 클라이언트에서 RGBA 순서의 ArrayBuffer를 보냈다고 가정
        image_rgba_flat = np.frombuffer(request.data, dtype=np.uint8)
        image_rgba = image_rgba_flat.reshape((height, width, 4)) # RGBA는 채널 4개

        # OpenCV는 BGR 순서를 사용하므로 변환
        image_bgr = cv2.cvtColor(image_rgba, cv2.COLOR_RGBA2BGR)

        # 객체 탐지 및 마스킹 처리
        processed_bgr_image = detect_and_mask_objects(yolo_model, image_bgr)

        # 처리된 이미지를 클라이언트가 받을 수 있는 형식으로 변환 (예: RGBA raw bytes)
        processed_rgba_image = cv2.cvtColor(processed_bgr_image, cv2.COLOR_BGR2RGBA)

        # NumPy 배열을 raw bytes로 변환
        img_bytes = processed_rgba_image.tobytes()

        return Response(img_bytes, mimetype='application/octet-stream')

    except Exception as e:
        print(f"Error processing image in Python: {e}")
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

if __name__ == '__main__':
    load_yolo_model_global() # Flask 앱 시작 시 모델 로드
    app.run(host='0.0.0.0', port=8080) # 개발용 서버 실행