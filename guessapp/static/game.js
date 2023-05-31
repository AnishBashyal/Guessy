const gameSocket = io("/game");

const messageGameInput = document.getElementById("messageGame")
messageGameInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageGameBtn").click();
    }
})

const sendGameMessage = () => {
    if (messageGameInput.value) {
        console.log("Game button pressed")
        gameSocket.emit("message", {data : messageGameInput.value});
        messageGameInput.value = ""
    }

}

const messageGameBody = document.getElementById("messagesGame")
const createGameMessage = (name, msg) => {
     const message = `
                <div class="text">
                    <span>
                        <strong> ${name} </strong>: ${msg}
                    </span>
                </div>
            `;
            messageGameBody.innerHTML += message;
}

gameSocket.on("connect", () => {
    console.log("COnnected 2");
});

gameSocket.on("message", (data) => {
    console.log("Message from Game")
    createGameMessage(data.name, data.message)
    console.log(data.name, data.message);
});

gameSocket.on("alert", (data) => {
    console.log("Not your turn")
    alert("Not your turn")
});