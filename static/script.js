const defaultMessage = `
<div class="bot-message">
    Hello 👋 Ask me any educational or general question.
</div>`;

async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();

    if(message === "") return;

    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerText = message;

    chatBox.appendChild(userDiv);

    input.value = "";

    const loadingDiv = document.createElement("div");
    loadingDiv.className = "bot-message";
    loadingDiv.innerText = "Thinking...";

    chatBox.appendChild(loadingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    try{

        const response = await fetch("/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                message:message
            })
        });

        const data = await response.json();

        loadingDiv.innerText = data.answer || "No response found.";

    }catch(error){
        loadingDiv.innerText = "Error fetching response.";
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

function clearChat(){
    document.getElementById("chat-box").innerHTML = "";
}

function newChat(){
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = defaultMessage;
    document.getElementById("user-input").value = "";
}

document.getElementById("user-input")
.addEventListener("keypress",function(e){
    if(e.key === "Enter"){
        sendMessage();
    }
});
