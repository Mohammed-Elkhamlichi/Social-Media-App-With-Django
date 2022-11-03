// make the scrollbar of the messages container be in the bottom to display
// the latest messages.

let messagesContainer = document.getElementById("messages_container") || null;
if(messagesContainer !== null){
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
