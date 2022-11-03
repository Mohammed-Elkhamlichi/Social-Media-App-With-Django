let deleteMessageBtn = document.getElementsByName("delete_message_btn");
// console.log(deleteMessageBtn);
async function deleMessage() {
    deleteMessageBtn.forEach((link) => {
        // console.log({ link: link.id });
        let messageID = link.id;
        let apiUrl = `http://localhost:8000/delete-message/${messageID}/`;
        link.addEventListener("click", (e) => {
            // console.log({ apiUrl });
            e.preventDefault();
            let confirm = window.confirm("are you sure you want to delete this message");
            if (confirm) {
                fetch(apiUrl)
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.success) {
                            let deleteMessageParent = link.parentElement.parentElement.parentElement;
                            deleteMessageParent.remove();
                        }
                    })
                    .catch((error) => console.log({ error }));
            }
        });
    });
}

deleMessage();
