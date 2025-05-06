// Firebase SDK bağlantıları zaten chatbot.html <head> kısmında eklenmiş olmalı:
// <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js"></script>
// <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-firestore-compat.js"></script>
// <script src="https://www.gstatic.com/firebasejs/9.6.10/firebase-storage-compat.js"></script>

const firebaseConfig = {
    apiKey: "AIzaSyA8ht2vwuc15a8cqQJxpiLCqxRUPYRoCGQ",
    authDomain: "colorfixedu.firebaseapp.com",
    projectId: "colorfixedu",
    storageBucket: "colorfixedu.appspot.com"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
const storage = firebase.storage();

const username = localStorage.getItem("username") || "anonymous";
const userId = localStorage.getItem("userId") || "unknown";

function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() !== "") {
        const chatBox = document.getElementById('chatBox');

        const userMessage = document.createElement('div');
        userMessage.classList.add('chat-message', 'user-message');
        userMessage.innerHTML = `<p><strong>Siz:</strong> ${userInput}</p>`;
        chatBox.appendChild(userMessage);

        db.collection("messages").add({
            user_id: userId,
            username: username,
            sender: "user",
            message: userInput,
            timestamp: new Date().toISOString()
        });

        const botReply = "Merhaba! Size nasıl yardımcı olabilirim?";
        const botMessage = document.createElement('div');
        botMessage.classList.add('chat-message', 'bot-message');
        botMessage.innerHTML = `<p><strong>Bot:</strong> ${botReply}</p>`;
        chatBox.appendChild(botMessage);

        db.collection("messages").add({
            user_id: userId,
            username: username,
            sender: "bot",
            message: botReply,
            timestamp: new Date().toISOString()
        });

        document.getElementById('userInput').value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function resetChat() {
    document.getElementById('chatBox').innerHTML =
        '<div class="chat-message bot-message"><p><strong>Bot:</strong> Merhaba! Size nasıl yardımcı olabilirim?</p></div>';
}

document.getElementById('fileInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const chatBox = document.getElementById('chatBox');
        const imgMessage = document.createElement('div');
        imgMessage.classList.add('chat-message', 'user-message');
        imgMessage.innerHTML = `<p><strong>Siz:</strong> Yüklenen resim:</p><img src="${URL.createObjectURL(file)}" style="max-width: 100%; border-radius: 10px;">`;
        chatBox.appendChild(imgMessage);
        chatBox.scrollTop = chatBox.scrollHeight;

        const imageRef = storage.ref().child(`uploads/${userId}_${Date.now()}_${file.name}`);
        imageRef.put(file).then(snapshot => {
            return snapshot.ref.getDownloadURL();
        }).then(downloadURL => {
            // Firestore'a kayıt
            db.collection("images").add({
                user_id: userId,
                username: username,
                image_url: downloadURL,
                uploaded_at: new Date().toISOString(),
                processed: false
            });

            const botMessage = document.createElement('div');
            botMessage.classList.add('chat-message', 'bot-message');
            botMessage.innerHTML = `<p><strong>Bot:</strong> Fotoğraf başarıyla yüklendi ve sisteme kaydedildi.</p>`;
            chatBox.appendChild(botMessage);
        }).catch(error => {
            alert("❌ Yükleme hatası: " + error.message);
        });
    }
});
