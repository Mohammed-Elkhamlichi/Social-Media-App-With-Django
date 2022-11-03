// follow unfollow user from his profile send request
async function followUnfollowUserProfileFetch(username, state) {
    // http://127.0.0.1:8000/auth/najim/follow-unfollow/unfollow
    let ApiUri = `http://localhost:8000/auth/${username}/follow-unfollow/${state}/`;
    fetch(ApiUri)
        .then((response) => response.json())
        .then((data) => console.log({ data }))
        .catch((err) => console.error({ err }));
}

// change the number of following and followers of the user after follow or unfollow people
// this script is to handle the follow and unfollow btn from the user profile
async function handleFollowUnfollowUserProfile() {
    let userFollowersLink = document.getElementById("user_followers_link");
    let container = document.getElementById("profile_follow_unfollow");
    if(userFollowersLink !== null && container  !== null){
        let btn = container.children[0]
        btn.addEventListener("click", async function (e) {
            e.preventDefault();
            let username = btn.id;
            let followers = parseInt(userFollowersLink.innerText.split(" ")[0]);
            if (btn.innerText === "unfollow") {
                await followUnfollowUserProfileFetch(username, "unfollow");
                userFollowersLink.innerText = `${(followers -= 1)} followers`;
                btn.innerText = "follow";
            } else if (btn.innerText === "follow") {
                await followUnfollowUserProfileFetch(username, "follow");
                userFollowersLink.innerText = `${(followers += 1)} followers`;
                btn.innerText = "unfollow";
            }
        });
    }
}

handleFollowUnfollowUserProfile();
