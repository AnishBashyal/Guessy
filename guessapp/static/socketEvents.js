import {createMessage} from './utils.js';

const socket = io({autoConnect : false});



const sendMessage = () => {
    socket.emit("message", {data : document.getElementById("message").value});
}

const createRoom = () => {  
    console.log("Beofre")
    socket.connect();
    console.log("After")

    socket.emit("create_room", {data : document.getElementById("username").value})
}

const createRoomBtn = document.getElementById("create_room")
if(createRoomBtn) createRoomBtn.addEventListener('click', createRoom)

socket.on("connect", () => {
    console.log("COnnected");
});

socket.on("message", (data) => {
    // createMessage(data.name, data.body)
    console.log(data.name, data.body);
});
