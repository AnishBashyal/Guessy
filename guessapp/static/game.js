const gameSocket = io("/game");
let turn = false
let gameStarted = false
let sid = ""
let Timer
const messageGameInput = document.getElementById("messageGame")
messageGameInput.addEventListener("keypress", function(event) {
    if (event.key == "Enter") {
        document.getElementById("messageGameBtn").click();
    }
})

const sendGameMessage = () => {
    if (messageGameInput.value && gameStarted) {
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
    gameStarted = false
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

gameSocket.on("setSid", (data) =>{
    sid = data.sid
})
gameSocket.on("alert", (data) => {
    console.log(data.message)
    const alerts = document.getElementById("alerts")

    const div = document.createElement("div");
    div.className = `alert alert-${data.category} alert-dismissible fade show`;
    div.setAttribute("role", "alert");

    const strong = document.createElement("strong");
    strong.textContent = data.message;
    div.appendChild(strong);

  
    // Create the button for closing the alert
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn-close";
    button.setAttribute("data-bs-dismiss", "alert");
    button.setAttribute("aria-label", "Close");
    div.appendChild(button);

    // Add the alert div to the document body or any desired parent element
    alerts.appendChild(div);
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
    gameStarted = true
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

gameSocket.on("displayTable", (data) => {
    console.log(data[0])
    let index = 0
    table = document.getElementById("leaderboardtable")
    table.innerHTML=""
    for (const item of data[1]) {
        index++
        const u_sid = Object.keys(item)[0];
        const u_name = Object.values(item)[0];
        
        const tr = document.createElement("tr");
        
        const th = document.createElement("th");
        th.scope = "row";
        th.textContent = index
        tr.appendChild(th)

        const td1 = document.createElement("td");
        td1.textContent =  u_name;
        if (u_sid == sid) {
            td1.textContent+= " (You)"
            tr.classList.add("table-active")
        }
        tr.appendChild(td1);

        const td2 = document.createElement("td");
        td2.textContent = data[0][u_sid];
        tr.appendChild(td2);

 

        table.appendChild(tr)
      }
    
})