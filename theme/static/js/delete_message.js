let deleteMessageBtn = document.getElementsByName("delete_message_btn");
setInterval(deleMessage(), 500);
function deleMessage() {
    Object.entries(deleteMessageBtn).map((link) => {
        let messageID = link[1].id;
        let apiUrl = `http://localhost:8000/delete-message/${messageID}/`;
        link[1].addEventListener("click", (e) => {
            e.preventDefault();
            let confirm = window.confirm("are you sure you want to delete this message");
            if (confirm) {
                fetch(apiUrl)
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.success) {
                            let deleteMessageParent = link[1].parentElement.parentElement.parentElement;
                            deleteMessageParent.remove();
                        }
                    })
                    .catch((error) => console.log({ error }));
            }
        });
    });
}
