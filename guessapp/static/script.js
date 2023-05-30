const socket = io();

const messageInput = document.getElementById("message")
messageInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageBtn").click();
    }
})

const sendMessage = () => {
    socket.emit("message", {data : messageInput.value});
}

const messageBody = document.getElementById("messages")
const createMessage = (name, msg) => {
     const message = `
                <div class="text">
                    <span>
                        <strong> ${name} <strong>: ${msg}
                    </span>
                <div>
            `;
            messageBody.innerHTML += message;
}

socket.on("connect", () => {
    console.log("COnnected");
});

socket.on("message", (data) => {
    createMessage(data.name, data.body)
    console.log(data.name, data.body);
});