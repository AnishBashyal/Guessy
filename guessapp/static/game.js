const gameSocket = io("/game");
let turn = false
let Timer
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

const wordInput = document.getElementById("wordInput")
wordInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("wordInputBtn").click();
    }
})

const setWord = () => {
    if (wordInput.value && turn ) {
        turn=false
        gameSocket.emit("wordSet",{data:wordInput.value});
        document.getElementById("wordInputArea").style.display="none"
        wordInput.value = ""
    }
}

const clearTimer = () => {
    clearInterval(Timer);
    document.getElementById("countdown").innerHTML = "Time Remain : &infin; ";
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
    console.log(data.message)
    alert(data.message)
});

gameSocket.on("turnDecided", (data)=>{
    console.log(turn)
    document.getElementById("currentturn").innerText = "Current Turn : " + (turn ? "You" : data.name)
});

gameSocket.on("turn", () => {
    console.log("Your turn boy!")
    document.getElementById("wordInputArea").style.display="block"
    turn = true

});

gameSocket.on("wordSet", (data)=>{
    console.log("Time starts")
    let timeleft = 10;
    Timer = setInterval(function(){
        if(timeleft <= 0){
            clearTimer()
            alert (`Winner is nobody..  ${data.name} choice of word was ${data.message}`);
            gameSocket.emit("wordNotGuessed")
        } else  {
            document.getElementById("countdown").innerText =  "Time Remain : " + timeleft;
        }
        timeleft -= 1;
    }, 1000);

})

gameSocket.on("wordGuessed", (data)=>{
    clearTimer()
    alert (`Winner is ${data.name} and correct word was ${data.message}`);
})

