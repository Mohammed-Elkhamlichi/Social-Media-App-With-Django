async function handleSendMessagesForm() {
    // get the message body, user, room, form
    let sendMessageForm = document.getElementById("send_message_form");
    let messageBody = document.getElementById("message_body");
    let messageUser = document.getElementById("message_user");
    let messageRoom = document.getElementById("message_room");
    let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    // when the user submit the form
    sendMessageForm.addEventListener("submit", async function (e) {
        e.preventDefault();
        let roomID = parseInt(messageRoom.value);
        let body = messageBody.value;
        let user = messageUser.value;
        console.log({ roomID, user, body, csrfToken });
        let data = await messagesApi(roomID, user, body, csrfToken);
    });
}

// post and get data from the server
async function messagesApi(roomID, user, body, csrfToken) {
    // http://127.0.0.1:8000/12/detail/
    let apiUri = `http://127.0.0.1:8000/${roomID}/detail-js/`;
    fetch(apiUri, {
        method: "POST",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ user, body }),
    })
        .then((res) => res.json())
        .then((data) => {
            console.log({ data });
        })
        .catch((err) => console.log({ err }));
}

handleSendMessagesForm();
