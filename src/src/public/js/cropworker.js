let rt, rl, rr, rb;

function transform(frame, controller) {
    const top = frame.displayHeight * (rt / 100);
    const left = frame.displayWidth * (rl / 100);
    const right = frame.displayWidth * (rr / 100);
    const bottom = frame.displayHeight * (rb / 100);

<<<<<<< Updated upstream
    function alignTo(value, alignment) {
        return value - (value % alignment);
=======
async function transform(frame, controller) {
    // 1. 캔버스 준비
    const bitmap = await createImageBitmap(frame);
    const canvas = new OffscreenCanvas(frame.displayWidth, frame.displayHeight);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0);

    // 2. OCR 실행 (이전과 동일)
    const { data: { words } } = await Tesseract.recognize(canvas, 'eng');

    // 3. "Hello" 단어 찾아 검은색 사각형으로 덮기 ✨
    for (const word of words) {
        if (word.text !== "YIYEIN") continue; // "Hello"가 아니면 건너뛰기

        // "Hello" 단어의 경계 상자(bounding box) 정보 가져오기
        const { x0, y0, x1, y1 } = word.bbox;
        const w = x1 - x0; // 사각형의 너비 계산
        const h = y1 - y0; // 사각형의 높이 계산

        // === 블러 처리 코드 대신 아래 코드로 변경 ===
        // 그리기 색상을 검은색으로 설정
        ctx.fillStyle = 'black';
        // 해당 위치에 채워진 사각형 그리기
        ctx.fillRect(x0, y0, w, h);
        // ========================================
>>>>>>> Stashed changes
    }

    const alignedLeft = alignTo(Math.round(left), 2);
    const alignedTop = alignTo(Math.round(top), 2);

    const newFrame = new VideoFrame(frame, {
        visibleRect: {
            x: alignedLeft,
            width: Math.round(frame.displayWidth - (left + right)),
            y: alignedTop,
            height: Math.round(frame.displayHeight - (top + bottom)),
        }
    });

    controller.enqueue(newFrame);
    frame.close();
}

onmessage = async (event) => {
    const { operation } = event.data;
    if (operation === 'crop') {
        const { readable, writable, top, bottom, left, right } = event.data;

        // 새 AbortController를 로컬로 생성
        const abortController = new AbortController();

        // crop 파라미터 저장
        rt = top;
        rb = bottom;
        rl = left;
        rr = right;

        try {
            await readable
                .pipeThrough(new TransformStream({ transform }))
                .pipeTo(writable, { signal: abortController.signal });
        } catch (err) {
            if (err.name === 'AbortError') {
                console.log('이전 작업이 취소되었습니다.');
            } else {
                console.error(err);
            }
        }
    } else {
        console.error('Unknown operation', operation);
    }
};
