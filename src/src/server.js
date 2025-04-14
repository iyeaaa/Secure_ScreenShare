import http from "http";
import { Server } from "socket.io";
import { instrument } from "@socket.io/admin-ui";
import express from "express";
import session from "express-session";
import path from "path";

const app = express();

/* Session 설정 */
const sessionMiddleware = session({
    secret: "your_secret_key", // 강력한 비밀 키 사용 요망
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false } // HTTPS 쓰면 secure: true
});

app.use(sessionMiddleware);
app.use(express.static(path.join(__dirname, "public")));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* Database 예시 */
const users = {
    "iyeaaa@naver.com": [
        { email: "cyh1443@gmail.com", room: "a" },
        { email: "sjj2305@naver.com", room: "b" }
    ],
    "cyh1443@gmail.com": [
        { email: "iyeaaa@naver.com", room: "a" },
        { email: "sjj2305@naver.com", room: "c" }
    ],
    "sjj2305@naver.com": [
        { email: "cyh1443@gmail.com", room: "c" },
        { email: "iyeaaa@naver.com", room: "b" }
    ],
};

const login_info = {
    "iyeaaa@naver.com": "123456",
    "cyh1443@gmail.com": "123456",
    "sjj2305@naver.com": "123456"
};

function ifNotLogin(req, res) {
    if (!req.session.user) {
        return res.redirect("/login.html");
    }
}

app.get("/", (req, res) => {
    ifNotLogin(req, res);
    res.sendFile(path.join(__dirname, "public", "main.html"));
});

app.get("/user", (req, res) => {
    ifNotLogin(req, res);
    res.send(JSON.stringify(users[req.session.user.email]));
});

app.get("/controller", (req, res) => {
    ifNotLogin(req, res);
    res.sendFile(path.join(__dirname, "public", "controller.html"));
});

app.get("/receiver", (req, res) => {
    ifNotLogin(req, res);
    res.sendFile(path.join(__dirname, "public", "receiver.html"));
});

app.post("/login", (req, res) => {
    const { email, password } = req.body;
    if (login_info[email] && login_info[email] === password) {
        req.session.user = { email };
        res.status(200).json({ message: "success", sid: req.sessionID });
    } else {
        res.status(401).json({ message: "fail" });
    }
});

app.post("/logout", (req, res) => {
    req.session.destroy(() => {
        res.redirect("/");
    });
});

const httpServer = http.createServer(app);

/* Socket.io 서버 설정 */
const wsServer = new Server(httpServer, {
    cors: {
        origin: ["https://admin.socket.io"],
        credentials: true
    }
});

instrument(wsServer, {
    auth: false
});

// 세션을 Socket.IO에 통합
wsServer.use((socket, next) =>
    sessionMiddleware(socket.request, socket.request.res || {}, next)
);

wsServer.on("connection", socket => {
    const session = socket.request.session;
    if (!session?.user) {
        console.log("Unauthorized access to Socket");
        return socket.disconnect();
    }

    console.log(`${session.user.email} connected`);
    socket.onAny(event => console.log(`Socket Event: ${event}`));

    socket.on("join", (roomName) => {
        socket.join(roomName);
    });

    socket.on("start", (roomName) => {
        // start 이벤트 발생 시 같은 룸의 상대에게 알림
        socket.to(roomName).emit("start");
    });

    socket.on("offer", (offer, roomName) => {
        console.log("offer received");
        socket.to(roomName).emit("offer", offer);
    });

    socket.on("answer", (answer, roomName) => {
        console.log("answer received");
        socket.to(roomName).emit("answer", answer);
    });

    socket.on("ice", (ice, roomName) => {
        console.log("ice candidate received");
        socket.to(roomName).emit("ice", ice);
    });

    socket.on("new_message", (msg, time, roomName) => {
        socket.to(roomName).emit("new_message", msg, time);
    });

    socket.on("size", (dx, dy, width, height, roomName) => {
        socket.to(roomName).emit("size", dx, dy, width, height);
    });

    socket.on("disconnecting", () => {
        socket.rooms.forEach(room => {
            socket.to(room).emit("bye", session.user.email);
        });
    });

    socket.on("disconnect", () => {
        wsServer.emit("update_rooms", getPublicRooms());
    });
});

const handleListen = () => console.log("Listening on http://localhost:3000");
httpServer.listen(3000, handleListen);

/* Helper function */
function getPublicRooms() {
    const { rooms, sids } = wsServer.sockets.adapter;
    return [...rooms.keys()].filter(room => !sids.has(room));
}
