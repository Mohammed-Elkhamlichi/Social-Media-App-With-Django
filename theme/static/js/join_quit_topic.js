// handle quit join topic form
const quitJoinTopicBtn = document.getElementsByName("topic_join_form") || null;
function handleQuitJoinTopicForm() {
    if(quitJoinTopicBtn !== null){
        quitJoinTopicBtn.forEach(async function (item) {
            item.addEventListener("submit", async function (e) {
                e.preventDefault();
                let input = item.childNodes[5];
                const topicID = parseInt(input.id);
                console.log({ input: input.value, topicID });
                if (input.value === "Quit") {
                    input.value = "Join";
                    input.setAttribute("class", "opacity-100 cursor-pointer");
                    quitJoinTopicFetch(topicID, "quit");
                } else if (input.value === "Join") {
                    input.value = "Quit";
                    input.setAttribute("class", "opacity-50 group-hover:opacity-100 cursor-pointer");
                    quitJoinTopicFetch(topicID, "join");
                }
            });
        });
    }
}
function quitJoinTopicFetch(topicID, state) {
    // http://127.0.0.1:8000/join-quit-topic/100/join/
    let ApiUri = `http://localhost:8000/join-quit-topic/${topicID}/${state}/`;
    console.log({ ApiUri });
    fetch(ApiUri)
        .then((response) => response.json())
        .then((data) => console.log({ data }))
        .catch((err) => console.error({ err }));
}

handleQuitJoinTopicForm();
