
/* 로그아웃 버튼 */

const logoutBtn = document.getElementById("logout")

function logout() {
    fetch("/logout", {
        method: "POST"
    }).then(() => {
        window.location.href = "/";
    });
}
logoutBtn.addEventListener("click", (event) => {
    logout()
})

/* 유저 데이터 불러오기 */

const chatList = document.querySelector(".chat-list")

fetch(`/user`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // JSON 데이터를 반환
    })
    .then(users => {
        users.forEach((value, key) => {
            const email = value.email
            const room = value.room
            createChatRoom(
                'profile1.jpg',
                email,
                room,
            )
        })
    })
    .catch(error => {
        console.error('Fetch error:', error); // 에러 처리
    });

function controllButtonEvent(roomname) {
    window.location.href = `/controller?room=${roomname}`
}

function receiveButtonEvent(roomname) {
    window.location.href = `/receiver?room=${roomname}`
}

// 새 채팅 방 정보를 생성하는 함수
function createChatRoom(profilePicSrc, username, room) {
    // chat-room div 생성
    const chatRoomDiv = document.createElement('div');
    chatRoomDiv.classList.add('chat-room');

    // chat-info div 생성
    const chatInfoDiv = document.createElement('div');
    chatInfoDiv.classList.add('chat-info');

    // 사용자 이름
    const usernameElement = document.createElement('h3');
    usernameElement.textContent = username;

    // 최근 메시지
    const lastMessageElement = document.createElement('p');
    lastMessageElement.textContent = `마지막 연결 : 2024.12.24`;

    // 원격 제어(하는 쪽) 버튼
    const remoteControlBtn = document.createElement('button');
    remoteControlBtn.classList.add('remote-control-btn');
    remoteControlBtn.textContent = '원격 제어하기';
    remoteControlBtn.addEventListener('click', () => controllButtonEvent(room));


    // 원격 제어(받는 쪽) 버튼
    const remoteControlledBtn = document.createElement('button');
    remoteControlledBtn.classList.add('remote-controlled-btn');
    remoteControlledBtn.textContent = '원격 제어 받기';
    remoteControlledBtn.addEventListener('click', () => receiveButtonEvent(room))

    // chat-info div에 사용자 이름과 메시지 추가
    chatInfoDiv.appendChild(usernameElement);
    chatInfoDiv.appendChild(lastMessageElement);

    // chat-room div에 요소들 추가
    chatRoomDiv.appendChild(chatInfoDiv);
    chatRoomDiv.appendChild(remoteControlBtn);
    chatRoomDiv.appendChild(remoteControlledBtn);

    // 원하는 부모 요소에 chat-room 추가 (예: chatList)
    chatList.appendChild(chatRoomDiv);
}