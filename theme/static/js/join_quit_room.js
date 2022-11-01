function handleQuitJoinRoomBtn() {
    // handle quit join room button
    const btn = document.getElementById("join_quit_room") || null;
    if(btn !== null){
        btn.addEventListener("click", async function (e) {
            e.preventDefault();
            console.log(btn.innerHTML);
            let room_id = parseInt(btn.value);
            if (btn.innerHTML === "Quit") {
                btn.innerHTML = "Join";
                quitJoinRoomFetch(room_id, "quit");
                btn.setAttribute(
                    "class",
                    "py-2 px-4 bg-green-600 border text-xs mx-1 rounded-lg text-gray-300   hover:font-bold"
                );
                window.location.reload();
            } else if (btn.innerHTML === "Join") {
                btn.setAttribute(
                    "class",
                    "py-2 px-4 bg-slate-600 border text-xs mx-1 rounded-lg text-gray-300  hover:font-bold"
                );
                btn.innerHTML = "Quit";
                quitJoinRoomFetch(room_id, "join");
                window.location.reload();
            }
        });
    }
}
function quitJoinRoomFetch(roomID, state) {
    // http://127.0.0.1:8000/join-quit-room/120/join/
    let ApiUri = `http://localhost:8000/join-quit-room/${roomID}/${state}/`;
    console.log({ ApiUri });
    fetch(ApiUri)
        .then((response) => response.json())
        .then((data) => console.log({ data }))
        .catch((err) => console.error({ err }));
}
handleQuitJoinRoomBtn();
