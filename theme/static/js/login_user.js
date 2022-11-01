import { setAlert } from "./alerts.js";

let loginUserForm = document.getElementById("login_user_form");
let email = document.getElementById("login_user_email");
let password = document.getElementById("login_user_password");
let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

if (loginUserForm !== null && email !== null && password !== null && csrfToken !== null) {
    loginUserForm.addEventListener("submit", (e) => {
        e.preventDefault();
        let emailValue = email.value;
        let passwordValue = password.value;
        let apiUrl = "http://localhost:8000/auth/login-api/";
        fetch(apiUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email: emailValue, password: passwordValue }),
            credentials: "include",
        })
            .then((res) => res.json())
            .then((login_data) => {
                console.log({ login_data });
                // alerts_div container
                setAlert(login_data.success, login_data.message);
                if (login_data.success) {
                    let username = login_data.username;
                    setTimeout(() => {
                        window.location.replace(`/auth/${username}/profile/`);
                    }, 2000);
                }
            })
            .catch((login_error) => {
                console.log({ login_error });
                setAlert(false, "Internal Server Error");
            });
    });
}
