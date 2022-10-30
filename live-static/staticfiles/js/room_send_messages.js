let messageParent = document.getElementById("messages_parent");
let messagesListContainer = document.getElementById("messages_container");
async function handleSendMessagesForm() {
    // get the message body, user, room, form
    let sendMessageForm = document.getElementById("send_message_form");
    let messageBody = document.getElementById("message_body");
    let messageUser = document.getElementById("message_user");
    let messageRoom = document.getElementById("message_room");
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    messageBody.focus();

    // when the user submit the form
    sendMessageForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        let roomID = parseInt(messageRoom.value);
        let body = messageBody.value;
        let user = messageUser.value;
        console.log({ roomID, user, body, csrfToken });
        await messagesApi(roomID, user, body, csrfToken);
        messageBody.value = "";
    });
}
let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
// post and get data from the server
async function messagesApi(roomID, user, body, csrfToken) {
    // http://127.0.0.1:8000/12/detail/
    let apiUri = `http://127.0.0.1:8000/${roomID}/detail-js/`;
    fetch(apiUri, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        // mode: "cors",
        body: JSON.stringify({ body }),
        // credentials: "include",
    })
        .then((res) => res.json())
        .then((data) => {
            // {messages: Array(5), users: Array(8), room: {…}, room_participants: Array(2), authenticate_user: {…}}
            let { messages, users, room, authenticate_user, new_message } = data;
            console.log({ messages, users, room, authenticate_user, new_message });
            // for loop to all messages.
            user = users.find((user) => user.id === new_message.user);
            // create the message container and set to it some attributes
            let messageContainer = document.createElement("div");
            let x = "";
            room.id === user.id
                ? (x = "border-green-600 bg-gray-600")
                : (x = "border-green-600 bg-slate-700  ml-auto mr-10 justify-center");
            messageContainer.setAttribute("class", `flex flex-col w-80 my-4 border py-2 px-4 rounded-md ${x}`);
            // create the message user info  and set to it some attributes
            let messageUserInfoContainer = document.createElement("div");
            messageUserInfoContainer.setAttribute("class", "flex flex-row  items-center ");

            // create the message user image and set some attributes
            let messageUserImage = document.createElement("img");
            messageUserImage.setAttribute("src", `http://localhost:8000${user.profile_pic}`);
            messageUserImage.setAttribute("class", "h-8 w-8 rounded-full");
            messageUserImage.setAttribute("alt", "user logo");

            // create link to redirect to the user profile
            let messageUserProfileLink = document.createElement("a");
            messageUserProfileLink.setAttribute("class", "text-xs mx-1 text-slate-300");
            messageUserProfileLink.setAttribute("url", `http://localhost:8000/auth/${user.username}/profile/`);
            messageUserProfileLink.textContent = ` @${user.username}`;

            // create span to display the date of create message
            let messageDateTime = document.createElement("span");
            messageDateTime.setAttribute("class", "text-xs text-slate-400");
            messageDateTime.textContent = `20-10-2022`;

            // create div to display the message body
            let messageBody = document.createElement("div");
            messageBody.setAttribute(
                "class",
                "text-xs text-gray-300 px-2 py-0 ml-1 whitespace-normal indent-4  leading-1 break-all"
            );
            messageBody.textContent = `${new_message.body}`;

            // set the image,username,date
            messageUserInfoContainer.appendChild(messageUserImage);
            messageUserInfoContainer.appendChild(messageUserProfileLink);
            messageUserInfoContainer.appendChild(messageDateTime);

            // start append the children to the message container
            messageContainer.appendChild(messageUserInfoContainer);
            messageContainer.appendChild(messageBody);

            messagesListContainer.appendChild(messageContainer);

            // start append the children to the message list container
            messagesListContainer.scrollTop = messagesListContainer.scrollHeight;
        })
        .catch((err) => console.log({ err }));
}

handleSendMessagesForm();
