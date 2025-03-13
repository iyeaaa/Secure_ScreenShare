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

if (room == null) {
    alert("Room is Null");
}

socket.emit("join", room);

getMedia().then(() => {
    makeConnection();
});

function close(event) {
    screenStream = null;
    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }
    // 필요한 경우 UI 업데이트
    startShareButton.disabled = false;
    stopShareButton.disabled = true;
}

async function getMedia() {
    try {
        screenStream = await navigator.mediaDevices.getUserMedia({
            audio: true,
            video: true,
        });
        myVideo.srcObject = screenStream;
    } catch (err) {
        console.error(`${err.name}: ${err.message}`);
        alert(err);
    }
}

/* RTC 연결 */
function makeConnection() {
    peerConnection = new RTCPeerConnection(configuration);

    // 데이터 채널 설정 (채팅용)
    setDataChannel();

    // 로컬 스트림의 모든 트랙을 연결에 추가 (화면 및 음성)
    if (screenStream) {
        screenStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, screenStream);
        });
    }

    // ICE 후보 이벤트 처리
    peerConnection.addEventListener("icecandidate", (event) => {
        if (event.candidate) {
            socket.emit("ice", event.candidate, room);
            console.log("sent ice candidate");
        }
    });

    // 원격 스트림 수신 처리
    peerConnection.addEventListener("track", handleAddStream);
}

async function handleAddStream(event) {
    const incomingStream = event.streams[0];
    console.log("Received remote stream:", incomingStream);
    screenVideo.srcObject = incomingStream;
}

/* Data Channel 설정 */
function setDataChannel() {
    // sendChannel 생성 (메시지 전송용)
    sendChannel = peerConnection.createDataChannel("sendChannel");
    sendChannel.onopen = handleSendChannelStatusChange;
    sendChannel.onclose = handleSendChannelStatusChange;

    // 원격 데이터 채널 수신
    peerConnection.ondatachannel = (event) => {
        receiveChannel = event.channel;
        receiveChannel.onmessage = handleReceiveMessage;
        receiveChannel.onopen = handleReceiveChannelStatusChange;
        receiveChannel.onclose = handleReceiveChannelStatusChange;
    };
}

function handleSendChannelStatusChange(event) {
    console.log("sendChannel: " + sendChannel.readyState)
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

function handleReceiveChannelStatusChange(event) {
    if (receiveChannel) {
        console.log("Receive channel's status has changed to " + receiveChannel.readyState);
    }
}

/* 채팅 관련 함수 */
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

function handleReceiveMessage(event) {
    let message = event.data;
    let time = event.timeStamp;
    console.log(time);
    appendMessageToChat(message, timestamp2date(new Date(time * 1000)), false);
}

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

/* Socket 이벤트 처리 */
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
