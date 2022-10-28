function handleFollowUnfollowUserSidebar() {
    let container = document.getElementsByName("follow_unfollow_container");
    container.forEach((element) => {
        // if the user click on the button follow or unfollow
        let btn = element.children[1].children[0];
        btn.addEventListener("click", async function (e) {
            e.preventDefault();
            // select the button inner text (follow or unfollow)
            item = element.children[1].children[0];
            // get the username from the button id
            username = item.id;
            console.log({ username });
            if (item.innerText === "unfollow") {
                item.innerText = "follow";
                followUnfollowUserSidebarFetch(username, "unfollow");
            } else if (item.innerText === "follow") {
                item.innerText = "unfollow";
                followUnfollowUserSidebarFetch(username, "follow");
            }
        });
    });
}

function followUnfollowUserSidebarFetch(username, state) {
    // http://127.0.0.1:8000/auth/najim/follow-unfollow/unfollow
    let ApiUri = `http://127.0.0.1:8000/auth/${username}/follow-unfollow/${state}/`;
    console.log({ ApiUri });
    fetch(ApiUri)
        .then((response) => response.json())
        .then((data) => console.log({ data }))
        .catch((err) => console.error({ err }));
}
handleFollowUnfollowUserSidebar();
