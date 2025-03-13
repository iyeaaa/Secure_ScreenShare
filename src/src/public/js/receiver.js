const socket = io();
const configuration = {
    iceServers: [
        {
            urls: "stun:stun.relay.metered.ca:80",
        },
        {
            urls: "turn:seoul.relay.metered.ca:80",
            username: "e0c6e9df29d16b37783c32a5",
            credential: "mU8NxnuLYXuEXzRr",
        },
        {
            urls: "turn:seoul.relay.metered.ca:80?transport=tcp",
            username: "e0c6e9df29d16b37783c32a5",
            credential: "mU8NxnuLYXuEXzRr",
        },
        {
            urls: "turn:seoul.relay.metered.ca:443",
            username: "e0c6e9df29d16b37783c32a5",
            credential: "mU8NxnuLYXuEXzRr",
        },
        {
            urls: "turns:seoul.relay.metered.ca:443?transport=tcp",
            username: "e0c6e9df29d16b37783c32a5",
            credential: "mU8NxnuLYXuEXzRr",
        },
    ],
};

const input = document.getElementById("text-input");
const sendMessageButton = document.getElementById("sendbtn");

const url = new URL(window.location.href);
const params = url.searchParams;
const room = params.get("room");
const myVideo = document.querySelector(".video-overlay video");
const screenVideo = document.querySelector(".screen-share video");

let screenStream;
let peerConnection;
let sendChannel;
let receiveChannel;

const startShareButton = document.querySelector(".screen-share-controls #startShareBtn");
const stopShareButton = document.querySelector(".screen-share-controls #stopShareBtn");
const screenCropBtn = document.querySelector(".screen-share-controls #screenCropBtn");

let slider = [0, 0, 0, 0, 0];

const worker = new Worker("./js/cropworker.js", { name: 'Crop worker' });
let readable, writable;

if (room == null) {
    alert("Room is Null");
}

socket.emit("join", room);

function init() {
    getScreen()
        .then(() => {
            makeConnection();
            socket.emit("start", room);
        });
}

document.querySelector('.slider-container').style.display = 'none';

function updateValue(sliderNumber, value) {
    document.getElementById("value" + sliderNumber).innerText = value;
    slider[sliderNumber] = value;
}

screenCropBtn.addEventListener('click', function () {
    const sliderContainer = document.querySelector('.slider-container');
    sliderContainer.style.display = (sliderContainer.style.display === 'none' || sliderContainer.style.display === '')
        ? 'flex'
        : 'none';
});

function applySliderValues() {
    const top = slider[1] || 0;
    const bottom = slider[2] || 0;
    const left = slider[3] || 0;
    const right = slider[4] || 0;
    console.log("적용 버튼 클릭:", top, bottom, left, right);
    croppingScreen(top, bottom, left, right);
}

function close() {
    screenStream.getTracks().forEach(track => track.stop());
    screenVideo.srcObject = null;
    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }
    startShareButton.disabled = false;
    stopShareButton.disabled = true;
    screenCropBtn.disabled = true;
}

startShareButton.disabled = false;
stopShareButton.disabled = true;
screenCropBtn.disabled = true;

startShareButton.addEventListener("click", init);
stopShareButton.addEventListener("click", close);

async function getScreen() {
    try {
        screenStream = await navigator.mediaDevices.getDisplayMedia({
            video: { displaySurface: "window" },
            audio: { suppressLocalAudioPlayback: false },
            preferCurrentTab: false,
            selfBrowserSurface: "exclude",
            systemAudio: "include",
            surfaceSwitching: "include",
            monitorTypeSurfaces: "include",
        });
        startShareButton.disabled = true;
        stopShareButton.disabled = false;
        screenCropBtn.disabled = false;
        screenVideo.srcObject = screenStream;
    } catch (err) {
        console.error("Error during screen capture", err);
    }
}

function croppingScreen(top, bottom, left, right) {
    if (typeof MediaStreamTrackProcessor === 'undefined' ||
        typeof MediaStreamTrackGenerator === 'undefined') {
        alert(
            'Your browser does not support the experimental MediaStreamTrack API for Insertable Streams of Media.'
        );
        return;
    }

    // 기존 화면 스트림에서 첫번째 트랙 추출
    const [track] = screenStream.getTracks();

    // 매번 새로운 Processor/Generator 생성
    const processor = new MediaStreamTrackProcessor({ track });
    const readable = processor.readable;

    const generator = new MediaStreamTrackGenerator({ kind: 'video' });
    const writable = generator.writable;

    // 새 생성된 generator의 트랙으로 화면 업데이트
    screenVideo.srcObject = new MediaStream([generator]);

    // cropworker에 새로운 스트림과 crop 파라미터 전달 (스트림은 transfer 됨)
    worker.postMessage({
        operation: 'crop',
        readable,
        writable,
        top, bottom, left, right
    }, [readable, writable]);

    // 만약 이미 RTCPeerConnection이 존재한다면, 기존 트랙을 새 generator의 트랙으로 교체!
    if (peerConnection) {
        const senders = peerConnection.getSenders();
        const videoSender = senders.find(sender => sender.track && sender.track.kind === 'video');
        if (videoSender) {
            videoSender.replaceTrack(generator).then(r => console.log('비디오 트랙을 교체했습니다.'));
        } else {
            // 없다면 새로 추가
            peerConnection.addTrack(generator, screenVideo.srcObject);
            console.log('비디오 트랙을 추가했습니다.');
        }
    } else {
        // 연결이 없다면 새 연결 생성 (기존 로직 유지)
        makeConnection();
        socket.emit("start", room);
    }
}


async function handleAddStream(event) {
    const incomingStream = event.streams[0];
    console.log("Received remote stream:", incomingStream);
    myVideo.srcObject = incomingStream;
    console.log("Attaching screen share stream");
}

function makeConnection() {
    peerConnection = new RTCPeerConnection(configuration);

    // 데이터 채널 설정
    setDataChannel();

    // 로컬 스트림의 모든 트랙을 연결에 추가
    if (screenVideo.srcObject)
        screenVideo.srcObject.getTracks().forEach(track =>
            peerConnection.addTrack(track, screenVideo.srcObject)
        );

    // ICE candidate 이벤트 리스너 등록
    peerConnection.addEventListener("icecandidate", (event) => {
        if (event.candidate) {
            socket.emit("ice", event.candidate, room);
            console.log("sent ice candidate");
        }
    });

    // 원격 스트림 받을 때 처리
    peerConnection.addEventListener("track", handleAddStream);
}

function setDataChannel() {
    // 데이터 채널 생성 (메시지 전송용)
    sendChannel = peerConnection.createDataChannel("sendChannel");
    sendChannel.onopen = handleSendChannelStatusChange;
    sendChannel.onclose = handleSendChannelStatusChange;

    // 원격에서 데이터 채널이 열리면 받기
    peerConnection.ondatachannel = (event) => {
        receiveChannel = event.channel;
        receiveChannel.onmessage = handleReceiveMessage;
        receiveChannel.onopen = handleReceiveChannelStatusChange;
        receiveChannel.onclose = handleReceiveChannelStatusChange;
    };
}

function handleSendChannelStatusChange(event) {
    if (sendChannel) {
        const state = sendChannel.readyState;
        if (state === "open") {
            input.disabled = false;
            input.focus();
            sendMessageButton.disabled = false;
        } else {
            input.disabled = true;
            sendMessageButton.disabled = true;
        }
    }
}

function handleReceiveMessage(event) {
    let message = event.data;
    let time = event.timeStamp;
    appendMessageToChat(message, timestamp2date(new Date(time * 1000)), false);
}

function handleReceiveChannelStatusChange(event) {
    if (receiveChannel) {
        console.log("Receive channel's status has changed to " + receiveChannel.readyState);
    }
}

function timestamp2date(timestamp) {
    const hours = timestamp.getHours();
    const minutes = timestamp.getMinutes();
    return `${hours > 12 ? '오후' : '오전'} ${hours % 12 || 12}:${minutes.toString().padStart(2, '0')}`;
}

sendMessageButton.addEventListener("click", event => {
    const currenttime = timestamp2date(new Date());
    let message = input.value;
    sendChannel.send(message);
    appendMessageToChat(message, currenttime, true);
    input.value = "";
    input.focus();
});

function createMessageElement(content, timestamp, isMine = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', isMine ? 'mine' : 'other');

    const contentParagraph = document.createElement('p');
    contentParagraph.textContent = content;

    const timestampSpan = document.createElement('span');
    timestampSpan.classList.add('timestamp');
    timestampSpan.textContent = timestamp;

    messageDiv.appendChild(contentParagraph);
    messageDiv.appendChild(timestampSpan);

    return messageDiv;
}

function appendMessageToChat(content, timestamp, isMine = false) {
    const chatMessagesContainer = document.querySelector('.chat-messages');
    if (!chatMessagesContainer) {
        console.error('Chat messages container not found!');
        return;
    }
    const newMessage = createMessageElement(content, timestamp, isMine);
    chatMessagesContainer.appendChild(newMessage);
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}

// Socket 이벤트 처리

socket.on("start", async (nickname) => {
    console.log("received join");
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    console.log("sent the offer");
    socket.emit("offer", offer, room);
});

socket.on("offer", async (offer) => {
    console.log("receive the offer");
    await peerConnection.setRemoteDescription(offer);
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    socket.emit("answer", answer, room);
    console.log("sent the answer");
});

socket.on("answer", async (answer) => {
    console.log("receive the answer");
    await peerConnection.setRemoteDescription(answer);
});

socket.on("ice", async (ice) => {
    console.log("receive the ice from other client");
    await peerConnection.addIceCandidate(ice);
});
