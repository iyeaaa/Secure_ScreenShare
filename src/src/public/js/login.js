

const loginForm = document.querySelector("form");

console.log(loginForm)

// 로그인 요청
function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message === "success") {
                window.location.href = "/"; // 로그인 성공 후 메인 페이지로 이동
            } else {
                alert("로그인 실패");
            }
        });
}


loginForm.addEventListener("submit", event => {
    event.preventDefault()
    login()
})

