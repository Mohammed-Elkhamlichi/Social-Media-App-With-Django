let messageParent = document.getElementById("messages_parent");
let messagesListContainer = document.getElementById("messages_container");
let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
async function handleSendMessagesForm() {
    // get the message body, user, room, form
    let sendMessageForm = document.getElementById("send_message_form");
    let messageBody = document.getElementById("message_body");
    let messageUser = document.getElementById("message_user");
    let messageRoom = document.getElementById("message_room");
    if (sendMessageForm !== null && messageBody !== null && messageUser !== null && messageRoom !== null) {
        messageBody.focus();
        // when the user submit the form
        sendMessageForm.addEventListener("submit", async function (e) {
            e.preventDefault();
            let roomID = parseInt(messageRoom.value);
            let body = messageBody.value;
            let user = messageUser.value;
            // setInterval(async () => {
            await messagesApi(roomID, user, body, csrfToken);
            // }, 5000);
            messageBody.value = "";
        });
    }
}

// post and get data from the server
async function messagesApi(roomID, user, body, csrfToken) {
    let apiUri = `http://localhost:8000/${roomID}/detail-js/`;
    fetch(apiUri, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ body }),
    })
        .then((res) => res.json())
        .then((data) => {
            let { messages, users, room, authenticate_user, new_message } = data;
            console.log({ messages, users, room, authenticate_user, new_message });
            // for loop to all messages.
            let isMessage = messages.filter((item) => item.id !== new_message.id);
            console.log({ isMessage: isMessage.length });
            // if ((isMessage.length > 0)) {
            user = users.find((user) => user.id === new_message.user);
            // create the message container and set to it some attributes
            let messageContainer = document.createElement("div");
            let x = "";
            user.id === new_message.user
                ? (x = "flex flex-col w-auto max-w-xs md:max-w-sm my-3 border p-2  rounded-lg border-green-600 bg-slate-800")
                : (x = "flex flex-col w-auto max-w-xs md:max-w-sm my-3 border p-2  rounded-lg border-green-600 bg-slate-700");
            messageContainer.setAttribute("class", x);
            // create the message user info  and set to it some attributes
            let messageUserInfoContainer = document.createElement("div");
            messageUserInfoContainer.setAttribute("class", "flex flex-row  items-center");

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
            let splitMessageDate = new_message.created.toString();
            splitMessageDate = splitMessageDate.split("T")[1].split(".")[0].split(":");
            let [h, m, s] = splitMessageDate;
            messageDateTime.textContent = `${h}:${m}`;
            // crate btn to delete the message
            // container
            let deleteMessageContainer = document.createElement("div");
            deleteMessageContainer.setAttribute("class", "flex flex-row items-center justify-center mx-3");

            // button
            let deleteMessageBtn = document.createElement("button");
            deleteMessageBtn.setAttribute(
                "class",
                "bg-red-500 w-6 h-6 text-center text-sm  text-white rounded-full border-2 border-red-500 hover:border-white"
            );
            deleteMessageBtn.setAttribute("name", "delete_message_btn");
            deleteMessageBtn.setAttribute("id", new_message.id);
            // icon
            let deleteMessageIcon = document.createElement("i");
            deleteMessageIcon.setAttribute("class", "fa fa-trash");

            deleteMessageBtn.appendChild(deleteMessageIcon);
            deleteMessageContainer.appendChild(deleteMessageBtn);

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
            messageUserInfoContainer.appendChild(deleteMessageContainer);

            // start append the children to the message container
            messageContainer.appendChild(messageUserInfoContainer);
            messageContainer.appendChild(messageBody);

            messagesListContainer.appendChild(messageContainer);

            // start append the children to the message list container
            messagesListContainer.scrollTop = messagesListContainer.scrollHeight;
            // }
        })
        .catch((err) => console.log({ err }));
}

handleSendMessagesForm();
