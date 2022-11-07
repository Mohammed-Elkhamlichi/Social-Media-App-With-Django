let deleteRoomBtn = document.getElementsByName("delete_room_btn");
function deleRoom() {
    Object.entries(deleteRoomBtn).map((element) => {
        let roomID = element[1].id;
        let apiUrl = `/${roomID}/delete/`;
        element[1].addEventListener("click", (e) => {
            e.preventDefault();
            let confirm = window.confirm("are you sure you want to delete this Room");
            if (confirm) {
                fetch(apiUrl)
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.success) {
                            let deleteRoomParent = element[1].parentElement.parentElement.parentElement;
                            deleteRoomParent.remove();
                        }
                    })
                    .catch((error) => console.log({ error }));
            }
        });
    });
}
deleRoom();
