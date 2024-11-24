// Sohbet kutusunu açma ve kapama
function toggleChat() {
    var chatbox = document.getElementById('chatbox');
    if (chatbox.style.display === "none" || chatbox.style.display === "") {
        chatbox.style.display = "flex";  // Sohbet kutusunu göster
    } else {
        chatbox.style.display = "none";  // Sohbet kutusunu gizle
    }
}

// Mesajları ekle
function appendMessage(message, sender) {
    var messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender);
    messageDiv.innerHTML = message;
    document.getElementById('messages').appendChild(messageDiv);
    document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
}

// Mesaj gönderme
function sendMessage() {
    var message = document.getElementById('userMessage').value;
    if (message.trim() === "") return;  // Boş mesaj gönderme
    appendMessage(message, 'user');  // Kullanıcı mesajını ekle
    document.getElementById('userMessage').value = '';  // Mesaj kutusunu temizle

    // Botun cevabını al
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.response, 'bot');  // Bot cevabını ekle
    })
    .catch(error => {
        console.error('Hata:', error);
    });
}

// Enter tuşuna basıldığında mesaj gönder
document.getElementById('userMessage').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
