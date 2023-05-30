const chatSocket = io("/chat");

const messageChatInput = document.getElementById("messageChat")
messageChatInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageChatBtn").click();
    }
})

const sendChatMessage = () => {
    if (messageChatInput.value) {
        chatSocket.emit("message", {data : messageChatInput.value});
        messageChatInput.value = ""
    }

}

const messageChatBody = document.getElementById("messagesChat")
const createChatMessage = (name, msg) => {
     const message = `
                <div class="text">
                    <span>
                        <strong> ${name} </strong>: ${msg}
                    </span>
                </div>
            `;
            messageChatBody.innerHTML += message;
}

chatSocket.on("connect", () => {
    console.log("COnnected");
});

chatSocket.on("message", (data) => {
    createChatMessage(data.name, data.body)
    console.log(data.name, data.body);
});