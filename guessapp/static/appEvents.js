const messageInput = document.getElementById("message")
messageInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageBtn").click();
    }
})

