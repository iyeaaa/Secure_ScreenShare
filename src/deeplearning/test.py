from ultralytics import YOLO
import cv2
import os
import numpy as np

# 모델 경로 설정
MODEL_PATH = 'best.pt'  # 학습된 모델 파일 경로 (사용자 환경에 맞게 수정)

# 1. 모델 로드 함수
def load_yolo_model(model_path):
    """
    지정된 경로에서 YOLO 모델을 로드합니다.

    Args:
        model_path (str): YOLO 모델 파일(.pt)의 경로.

    Returns:
        ultralytics.YOLO or None: 성공적으로 로드된 모델 객체 또는 실패 시 None.
    """
    if not os.path.exists(model_path):
        print(f"[오류] 모델 파일을 찾을 수 없습니다: {model_path}")
        return None
    try:
        model = YOLO(model_path)
        print(f"[정보] 모델 로드 완료: {model_path}")
        return model
    except Exception as e:
        print(f"[오류] 모델 로드 중 문제 발생: {e}")
        return None

# 2. 이미지 비트맵에서 객체 탐지 및 좌표 반환 함수
def detect_objects_from_bitmap(model, image_bitmap):
    """
    이미지 비트맵(NumPy 배열)에서 객체를 탐지하고,
    각 객체의 클래스명, 신뢰도, 좌표를 반환합니다.

    Args:
        model (ultralytics.YOLO): 로드된 YOLO 모델 객체.
        image_bitmap (np.ndarray): OpenCV 등으로 읽은 이미지 데이터 (BGR 형식).

    Returns:
        list: 감지된 객체들의 정보(딕셔너리)를 담은 리스트.
              각 딕셔너리는 'class_name', 'confidence', 'coordinates' 키를 가집니다.
              탐지된 객체가 없으면 빈 리스트를 반환합니다.
    """
    if model is None:
        print("[오류] detect_objects_from_bitmap: 모델이 유효하지 않습니다.")
        return []
    if not isinstance(image_bitmap, np.ndarray):
        print("[오류] detect_objects_from_bitmap: 입력 이미지가 유효한 NumPy 배열이 아닙니다.")
        return []

    detected_objects_list = []
    try:
        print(image_bitmap)
        # YOLO 모델로 추론 수행
        results = model(image_bitmap)[0]  # 첫 번째 결과 사용
    except Exception as e:
        print(f"[오류] 모델 추론 중 문제 발생: {e}")
        return []

    # 감지된 객체 정보 추출
    if len(results.boxes) > 0:
        print(f"[정보] 감지된 객체 수: {len(results.boxes)}")
        for box in results.boxes:
            # 바운딩 박스 좌표 (xyxy 포맷)
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            confidence = float(box.conf[0].item())  # 신뢰도
            class_id = int(box.cls[0].item())      # 클래스 ID
            class_name = model.names[class_id]     # 클래스명

            # 설정된 신뢰도 임계값 이상인 객체만 처리
            if confidence > 0.5:  # 임계값 (0.0 ~ 1.0, 필요에 따라 조절)
                object_info = {
                    'class_name': class_name,
                    'confidence': confidence,
                    'coordinates': (x1, y1, x2, y2)
                }
                detected_objects_list.append(object_info)
                # 콘솔에 감지 정보 출력
                print(f"[감지] 클래스: {class_name} | 신뢰도: {confidence:.2f} | 좌표: ({x1}, {y1})-({x2}, {y2})")
    else:
        print("[정보] 감지된 객체가 없습니다.")

    return detected_objects_list

# --- 메인 실행 부분 ---
if __name__ == "__main__":
    # 모델 로드
    yolo_model = load_yolo_model(MODEL_PATH)

    if yolo_model:
        # 테스트할 이미지 경로 설정
        IMG_NAME = 'test2.png'  # 테스트할 이미지 파일명 (사용자 환경에 맞게 수정)
        IMG_PATH = os.path.join(os.getcwd(), IMG_NAME) # 현재 작업 디렉토리 기준

        if not os.path.exists(IMG_PATH):
            print(f"[오류] 이미지 파일을 찾을 수 없습니다: {IMG_PATH}")
        else:
            # OpenCV를 사용하여 이미지 파일을 비트맵(NumPy 배열)으로 로드
            original_image_bitmap = cv2.imread(IMG_PATH)

            if original_image_bitmap is None:
                print(f"[오류] 이미지를 로드할 수 없습니다: {IMG_PATH}")
            else:
                # 가리기 효과를 적용할 이미지 복사본 생성
                image_to_display_masked = original_image_bitmap.copy()

                # 이미지 비트맵으로 객체 탐지 수행
                # 추론은 원본 이미지로 수행해야 정확합니다.
                detected_objects = detect_objects_from_bitmap(yolo_model, original_image_bitmap)

                if detected_objects:
                    print("\n--- 최종 감지 결과 및 객체 가리기 ---")
                    for obj in detected_objects:
                        print(f"가려질 객체: 클래스: {obj['class_name']}, 신뢰도: {obj['confidence']:.2f}, 좌표: {obj['coordinates']}")

                        # 감지된 객체 영역을 검은색 사각형으로 완전히 가리기
                        x1, y1, x2, y2 = obj['coordinates']
                        cv2.rectangle(image_to_display_masked, (x1, y1), (x2+300, y2), (0, 0, 0), cv2.FILLED) # 검은색(BGR), 채우기

                    # 결과 이미지 (가려진 객체 포함) 보여주기
                    cv2.imshow("Masked Objects in Image", image_to_display_masked)
                    print("\n[정보] 가려진 객체가 표시된 이미지를 확인하세요. 아무 키나 누르면 창이 닫힙니다.")
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                else:
                    print("\n--- 최종 감지 결과 ---")
                    print("감지된 객체가 없어 가릴 내용이 없습니다.")
                    # 객체가 없을 경우 원본 이미지를 보여줄 수 있습니다.
                    # cv2.imshow("Original Image (No Detections)", original_image_bitmap)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
    else:
        print("[오류] YOLO 모델 로드에 실패하여 프로그램을 종료합니다.")