export function setAlert(success, message) {
    let alertsContainer = document.getElementById("alerts_container");
    // create the alert container
    let alertContainer = document.createElement("div");
    // create the message container
    let alertMessage = document.createElement("h1");
    if (success) {
        alertContainer.setAttribute("class", "my-2 bg-green-100 p-3 w-full rounded m-auto");
        alertMessage.setAttribute("class", "text-md text-green-700");
        alertMessage.textContent = message;
    }
    if (!success) {
        alertContainer.setAttribute("class", "my-2 bg-red-100  p-3 w-full rounded m-auto");
        alertMessage.setAttribute("class", "text-md  text-red-700");
        alertMessage.textContent = message;
    }

    alertContainer.appendChild(alertMessage);
    if (alertsContainer !== null) {
        alertsContainer.appendChild(alertContainer);
    }
    setTimeout(function () {
        alertContainer.setAttribute("class", "hidden");
    }, 5000);
}
