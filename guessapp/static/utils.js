const messageBody = document.getElementById("messages")

export const createMessage = (name, msg) => {
    const message = `
               <div class="text">
                   <span>
                       <strong> ${name} <strong>: ${msg}
                   </span>
               <div>
           `;
           messageBody.innerHTML += message;
}
