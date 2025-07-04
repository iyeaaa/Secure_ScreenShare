import cv2
import numpy as np
import os
import random

# 데이터셋 폴더 설정
DATASET_DIR = './dataset'
IMG_DIR = os.path.join(DATASET_DIR, 'images', 'val')
LABEL_DIR = os.path.join(DATASET_DIR, 'labels', 'val')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(LABEL_DIR, exist_ok=True)

# 원본 카카오톡 아이콘 경로 (알파 채널 포함 PNG)
ICON_PATH = 'kakao.png'

# 데이터 생성 개수
NUM_IMAGES = 50

def random_position(img_width, img_height, icon_width, icon_height):
    x = random.uniform(icon_width / 2, img_width - icon_width / 2)
    y = random.uniform(icon_height / 2, img_height - icon_height / 2)
    return x, y

def overlay_image_alpha(bg, fg, x, y):
    # 배경과 전경의 크기 가져오기
    h, w = fg.shape[:2]
    # 배경의 ROI 가져오기
    roi = bg[y:y+h, x:x+w]

    # 알파 채널 분리
    fg_rgb = fg[:, :, :3]
    alpha = fg[:, :, 3] / 255.0

    # 전경과 배경 합성
    for c in range(3):  # BGR 채널
        roi[:, :, c] = (alpha * fg_rgb[:, :, c] + (1 - alpha) * roi[:, :, c])

    bg[y:y+h, x:x+w] = roi
    return bg

def save_image_with_label(background, icon, icon_name, idx):
    h, w, _ = background.shape
    icon_h, icon_w, _ = icon.shape

    # 랜덤 위치와 크기 조정
    scale = random.uniform(0.1, 0.5)
    new_w, new_h = int(icon_w * scale), int(icon_h * scale)
    icon_resized = cv2.resize(icon, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # 랜덤 위치 계산
    center_x, center_y = random_position(w, h, new_w, new_h)
    x1 = int(center_x - new_w / 2)
    y1 = int(center_y - new_h / 2)

    # 이미지 합성 (알파 채널 고려)
    combined = overlay_image_alpha(background, icon_resized, x1, y1)

    # 이미지 저장
    img_name = f'kakaoicon_{idx}.png'
    img_path = os.path.join(IMG_DIR, img_name)
    cv2.imwrite(img_path, combined)

    # 라벨 파일 생성 (상대 좌표)
    label_name = f'kakaoicon_{idx}.txt'
    label_path = os.path.join(LABEL_DIR, label_name)
    with open(label_path, 'w') as f:
        rel_x = center_x / w
        rel_y = center_y / h
        rel_w = new_w / w
        rel_h = new_h / h
        f.write(f'0 {rel_x:.6f} {rel_y:.6f} {rel_w:.6f} {rel_h:.6f}\n')

# 카카오톡 아이콘 불러오기 (알파 채널 포함)
icon = cv2.imread(ICON_PATH, cv2.IMREAD_UNCHANGED)

# 데이터셋 생성
for i in range(NUM_IMAGES):
    # 흰색 배경 이미지 생성 (투명도 포함)
    background = np.ones((640, 640, 3), dtype=np.uint8) * 255
    background = cv2.cvtColor(background, cv2.COLOR_RGB2RGBA)
    save_image_with_label(background, icon, 'kakaoicon', i)

print(f"[완료] {NUM_IMAGES}개의 데이터셋이 생성되었습니다.")
