let rt, rl, rr, rb;

function transform(frame, controller) {
    const top = frame.displayHeight * (rt / 100);
    const left = frame.displayWidth * (rl / 100);
    const right = frame.displayWidth * (rr / 100);
    const bottom = frame.displayHeight * (rb / 100);

    function alignTo(value, alignment) {
        return value - (value % alignment);
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
