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

let messageChild = `
<div
    class="flex flex-col w-80   my-4 border py-2 px-4   rounded-md {% if room.host == message.user %} border-green-600 bg-gray-600  {% else %} border-green-600 bg-slate-700  ml-auto mr-10 justify-center   {% endif %}">
    <div class="flex flex-row  items-center ">
        <img src="{{message.user.profile_pic.url}}" alt="room host" class=" h-8 w-8  rounded-full">
        <a href="{% url 'accounts:profile' message.user.username %}"
            class="text-xs mx-1 text-slate-300">
            @{{message.user}}
        </a>
        <span class="text-xs text-slate-400">
            {{message.created|time:'H:i'}}
        </span>
        {% if message.user != request.user %}
        {% if message.user in request.user.following.all %}
        <a href="{% url 'accounts:follow_unfollow_user' message.user.username 'unfollow' %}"
            class="mx-2 text-green-500 border-2 rounded-full py-1 px-2 text-xs transition duration-200 ease-in-out hover:border-green-500 hover:text-white cursor-pointer">
            unfollow
        </a>
        {% else %}
        <a href="{% url 'accounts:follow_unfollow_user' message.user.username 'follow'  %}"
            class="mx-2 text-green-500 border-2 rounded-full py-1 px-2 text-xs transition duration-200 ease-in-out hover:border-green-500 hover:text-white cursor-pointer">
            follow
        </a>
        {% endif %}
        {% endif %}
    </div>
    <div class="text-xs text-gray-300 px-2 py-0 ml-1 whitespace-normal indent-4  leading-1 break-all">
        {{message.body}}
    </div>
</div>
`;

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
        body: JSON.stringify({ body }),
    })
        .then((res) => res.json())
        .then((data) => {
            console.log({ data });
            messagesListContainer.append(messageChild);
        })
        .catch((err) => console.log({ err }));
}

handleSendMessagesForm();
