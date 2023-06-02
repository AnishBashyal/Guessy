const chatSocket = io("/chat");

const messageChatInput = document.getElementById("messageChat")
messageChatInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageChatBtn").click();
    }
})

const sendChatMessage = () => {
    if (messageChatInput.value) {
        console.log("Chat button pressed")
        chatSocket.emit("message", {data : messageChatInput.value});
        messageChatInput.value = ""
    }

}

const messageChatBody = document.getElementById("messagesChat")
const createChatMessage = (name, msg) => {
    div = document.createElement("div");
    div.classList = "text";
    span = document.createElement("span");
    strong = document.createElement("strong");
    strong.innerText = name;
    text = document.createTextNode(` : ${msg}`);

    span.appendChild(strong);
    span.appendChild(text);
    div.appendChild(span);
    messageChatBody.appendChild(div);
    messageChatBody.scrollTop = messageChatBody.scrollHeight;

}

chatSocket.on("connect", () => {
    console.log("COnnected");
});

chatSocket.on("message", (data) => {
    createChatMessage(data.name, data.message)
    console.log(data.name, data.message);
});

