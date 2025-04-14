let rt, rl, rr, rb;
importScripts('https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js');


async function transform(frame, controller) {
    // Crop 설정 및 캔버스 처리 생략 (기존 코드 유지)
    const bitmap = await createImageBitmap(frame);
    const canvas = new OffscreenCanvas(frame.displayWidth, frame.displayHeight);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0);

    // OCR 실행
    const { data: { words } } = await Tesseract.recognize(canvas, 'eng');

    // "Hello"만 블러 처리
    for (const word of words) {
        if (word.text !== "Hello") continue;  // ✅ 이 조건 추가

        const { x0, y0, x1, y1 } = word.bbox;
        const w = Math.max(x1 - x0, 1);
        const h = Math.max(y1 - y0, 1);
        const region = ctx.getImageData(x0, y0, w, h);
        const size = 5;

        for (let yy = 0; yy < h; yy += size) {
            for (let xx = 0; xx < w; xx += size) {
                const i = (yy * w + xx) * 4;
                const r = region.data[i];
                const g = region.data[i + 1];
                const b = region.data[i + 2];

                for (let dy = 0; dy < size; dy++) {
                    for (let dx = 0; dx < size; dx++) {
                        const xi = ((yy + dy) * w + (xx + dx)) * 4;
                        if (xi < region.data.length - 4) {
                            region.data[xi] = r;
                            region.data[xi + 1] = g;
                            region.data[xi + 2] = b;
                        }
                    }
                }
            }
        }

        ctx.putImageData(region, x0, y0);
    }

    const newFrame = new VideoFrame(canvas, {
        timestamp: frame.timestamp
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
