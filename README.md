
# AI 기반 프라이버시 보호 실시간 화면 공유 서비스


## ✨ 포스터

<img src="https://github.com/iyeaaa/Secure_ScreenShare/blob/main/photos/%5B%ED%8F%AC%EC%8A%A4%ED%84%B0%5DCTR_%EC%9D%B4%EC%98%88%EC%9D%B8.jpg" width="650">


## 🎯 핵심 기능 (Core Features)

### 1\. AI 기반 자동 민감 정보 마스킹

단순한 화면 공유를 넘어, AI가 실시간으로 화면을 분석하여 민감 정보가 노출될 위험을 스스로 감지하고 차단합니다.

  * **실시간 객체 탐지**: 학습된 **YOLO 모델**을 활용하여, 화면 공유 중 갑자기 나타나는 카카오톡, 줌(Zoom) 알림 등 사전에 정의된 민감 객체를 실시간으로 탐지합니다.
  * **자동 마스킹**: 탐지된 객체는 즉시 검은색 사각형으로 가려져, 상대방에게는 해당 정보가 전혀 노출되지 않습니다.

| 원본 화면 (공유자) | 전송 화면 (시청자) |
| :--- | :--- |
|  |  |
| *(카카오톡 알림이 떠 있는 화면 예시 이미지)* | *(알림이 검은색으로 가려진 화면 예시 이미지)* |

### 2\. 화면 영역 세밀 지정

기존의 '전체 화면', '프로그램 창', '브라우저 탭' 단위 공유 방식의 한계를 극복했습니다. 사용자는 마치 이미지를 자르듯, 공유하고 싶은 화면 영역을 마우스로 자유롭게 지정할 수 있습니다.

  * **정교한 스트림 제어**: 브라우저의 **Insertable Streams API**를 활용하여 WebRTC로 전송되는 원본 비디오 프레임을 직접 제어합니다.
  * **직관적인 UX**: 사용자가 선택한 영역의 좌표값(x, y, width, height)을 기준으로 매 프레임을 잘라내어(crop) 상대방에게 전송함으로써, 원하는 부분만 정확하게 공유하고 나머지 영역의 프라이버시는 완벽하게 보호합니다.


## 🛠️ 시스템 아키텍처 및 기술 스택

이 프로젝트는 최신 웹 기술과 AI 모델을 결합한 풀스택 애플리케이션입니다.

  * **Frontend**: `HTML`, `CSS`, `JavaScript`
  * **Backend**: `Node.js`, `Express`, `Socket.IO`
  * **Real-time Communication**: `WebRTC` (영상/음성/데이터 채널)
  * **AI Module**: `Python`, `YOLO`, `OpenCV`
  * **System Integration**: Node.js의 `child_process`를 통한 Python 모듈 API화

<!-- end list -->

```
[ 사용자 A (공유자) ]                  [      Node.js 서버      ]                  [ 사용자 B (시청자) ]
  - WebRTC 화면 캡처  <---------------->  - 시그널링 (Socket.IO)  <---------------->  - WebRTC 스트림 수신
  - 캡처 프레임 전송     
        |
        V
  [ Python AI 모듈 ]
  - YOLO 객체 탐지
  - 마스킹 좌표 반환
```


## 🏆 수상 경력

- **2025 CNU SW/AI Project Fair 창의작품경진대회 우수상 (2위/85팀)**.  

| 상장 | 판넬 |
| :--- | :--- |
| <img src="https://github.com/iyeaaa/Secure_ScreenShare/blob/main/photos/%EC%83%81%EC%9E%A5.jpeg" width="300"> | <img src="https://github.com/iyeaaa/Secure_ScreenShare/blob/main/photos/%ED%8C%90%EB%84%AC.jpeg" width="300"> |






## 발전과정

| 주차  | 활동 | 보고서 | 발표자료 | 발표영상 | PR |
|------|------|--------|----------|----------|----|
| 1 주차 | 디자인 개요서 작성 | [보고서](https://docs.google.com/document/d/1Et6mASg1h8TvnPL3yr42QxF-E3m8FyGT/edit?usp=sharing&ouid=116586439470799169786&rtpof=true&sd=true)| [발표자료](https://drive.google.com/file/d/1Er5kh8nodRNm502V2xAwjBVlRuuh4th6/view?usp=sharing) | [발표영상](https://youtu.be/z570EzBaHbY?si=IamLZpoUD0n9iSxB) | [PR](https://github.com/iyeaaa/PrivRTC/pull/1) |
| 2 주차 | 문제점 목록 작성 | [보고서](https://docs.google.com/document/d/1EyKkXhdYSxklNGGQriLnpQpO-PLTwXCe/edit?usp=sharing&ouid=116586439470799169786&rtpof=true&sd=true) | [발표자료](https://drive.google.com/file/d/1EtfTJZxNmwpgwLKUmFc3RD0Z3oLn_0A6/view?usp=sharing) | [발표영상](https://youtu.be/bX-g0Ycl_NE) | [PR](https://github.com/iyeaaa/PrivRTC/pull/2) |
| 3 주차 | 프로젝트 브레인스토밍 결과 작성 | [보고서](https://drive.google.com/file/d/1UIE2ilqTdA2pJEPVAZCcgX7qy_hZoTeh/view?usp=sharing) | [발표자료](https://drive.google.com/file/d/1UeGg6eTVL-r8IHE9Akafhmzww5hqME_R/view?usp=sharing) | [발표영상](https://youtu.be/tU0xAXcUeFE) | [PR](https://github.com/iyeaaa/PrivRTC/pull/3) |
| 4 주차 | 문제정의서 작성 | [보고서](https://docs.google.com/document/d/14Z3h5PkqaI4eDuY_tky5x93FtNltqDEp/edit?usp=sharing&ouid=116586439470799169786&rtpof=true&sd=true) | [발표자료](https://drive.google.com/file/d/14Udo597ZiC3P2LbN8PdXhLQTjNRFX-zJ/view?usp=sharing) | [발표영상](https://youtu.be/trcVuJcsKjQ) | [PR](https://github.com/iyeaaa/PrivRTC/pull/5) |
| 5 ~ 6 주차 | 유스케이스 명세서 작성 | [보고서](https://drive.google.com/file/d/1m5nW38I_OwqjBsZ1IMW_TGx7shzQ9rqv/view?usp=sharing) | [발표자료](https://drive.google.com/file/d/1lkffA419TqV7ijY0K5gdlcU2Xrhv3IAT/view?usp=sharing) | [발표영상](https://youtu.be/O9QoudGL4VE) | [PR](https://github.com/iyeaaa/PrivRTC/pull/7) |
| 7 ~ 8 주차 | 시퀀스 다이어그램 작성 | [보고서](https://drive.google.com/file/d/1ox4fszU0RliugP12ZYEe4a0OLRPJSRko/view?usp=sharing) | [발표자료](https://drive.google.com/file/d/1ox6m0jLALT0ibqaVIwET4WEnrD1hCBR_/view?usp=sharing) | [발표영상](https://youtu.be/8jrYlrZgomo) | [PR](https://github.com/iyeaaa/PrivRTC/pull/8) |
| 11 주차 | 테스트 계획서 작성 | [보고서](https://drive.google.com/file/d/1-I7cvU2s28HZpoLvkL2rfvS7Cv0rGDSq/view?usp=sharing) | [발표자료](https://drive.google.com/file/d/1-IN-QDe8_OGq-yHafoBtkF3UDPERWpfv/view?usp=sharing) | [발표영상](https://youtu.be/r8z5Vyb6kII) | [PR](https://github.com/iyeaaa/PrivRTC/pull/10) |
| 13 주차 | 테스트 결과 보고서 작성 | [보고서](https://drive.google.com/file/d/17isrAYxoZbIhu5AWgEg17g41AmclLsRX/view?usp=sharing) | [발표자료](https://drive.google.com/file/d/17cBLenmV8LcW5CkrlhdNdkkUHiMFpBUt/view?usp=sharing) | [발표영상](https://youtu.be/xj7pctZ1FHM) | [PR](https://github.com/iyeaaa/PrivRTC/pull/12) |


