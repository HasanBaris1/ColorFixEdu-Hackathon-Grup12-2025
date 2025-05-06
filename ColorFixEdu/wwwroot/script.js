const messages = [
    "Her gün bir adım daha ileri!",
    "Bugün en güçlü halinle başla!",
    "Kendine güven, başarabilirsin!",
    "Gelişim sabırla gelir.",
    "Zorluklar seni güçlendirir.",
    "Küçük adımlar büyük farklar yaratır.",
    "Bugün için bir şey yap!",
    "Sen yeter ki iste!",
    "Başlamak bitirmenin yarısıdır.",
    "Yola devam, pes etme!"
];

const gradients = [
    "linear-gradient(to right, #6a11cb, #2575fc)",
    "linear-gradient(to right, #ff512f, #dd2476)",
    "linear-gradient(to right, #00b09b, #96c93d)",
    "linear-gradient(to right, #f7971e, #ffd200)",
    "linear-gradient(to right, #fc5c7d, #6a82fb)",
    "linear-gradient(to right, #a18cd1, #fbc2eb)",
    "linear-gradient(to right, #4facfe, #00f2fe)",
    "linear-gradient(to right, #43cea2, #185a9d)"
];

let currentIndex = 0;
const popup = document.createElement("div");
popup.classList.add("popup");
document.body.appendChild(popup);

function showPopup() {
    popup.textContent = messages[currentIndex];
    popup.classList.add("show");

    const randomGradient = gradients[Math.floor(Math.random() * gradients.length)];
    popup.style.background = randomGradient;

    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    const popupWidth = 300;
    const popupHeight = 80;
    const side = Math.random() < 0.5 ? "left" : "right";

    const horizontalPadding = 20;
    const verticalPadding = 40;

    const left = side === "left"
        ? horizontalPadding
        : windowWidth - popupWidth - horizontalPadding;

    const top = Math.floor(Math.random() * (windowHeight - popupHeight - verticalPadding * 2)) + verticalPadding;

    popup.style.left = `${left}px`;
    popup.style.top = `${top}px`;

    setTimeout(() => {
        popup.classList.remove("show");
    }, 3500);

    currentIndex = (currentIndex + 1) % messages.length;
}

setInterval(showPopup, 4000);

const firebaseConfig = {
    apiKey: "AIzaSyA8ht2vwuc15a8cqQJxpiLCqxRUPYRoCGQ",
    authDomain: "colorfixedu.firebaseapp.com",
    projectId: "colorfixedu",
    storageBucket: "colorfixedu.appspot.com",
    messagingSenderId: "700457303779",
    appId: "1:700457303779:web:fe22964b328816de7a0fd6"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();

            db.collection("users").add({
                username: username,
                password: password
            }).then(() => {
                alert("Kayıt başarılı!");
                window.location.href = "login.html";
            }).catch(error => {
                alert("Hata: " + error.message);
            });
        });
    }
});
