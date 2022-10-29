// make the scrollbar of the messages container be in the bottom to display
// the latest messages.

const messagesContainer = document.getElementById("messages_container");
messagesContainer.scrollTop = messagesContainer.scrollHeight;
