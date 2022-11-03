export function setAlert(data) {
    let alertsContainer = document.getElementById("alerts_container");
    // create the alert container
    let alertContainer = document.createElement("div");
    // create the message container
    let alertMessage = document.createElement("h1");
    if (data.success) {
        alertContainer.setAttribute("class", "my-2 bg-green-500 p-3 w-full rounded m-auto");
        alertMessage.setAttribute("class", "text-md text-white");
    } else {
        alertContainer.setAttribute("class", "my-2  p-3 w-full rounded m-auto");
        alertContainer.style.background = "#ff9898";
        alertMessage.setAttribute("class", "text-md  text-white");
    }
    alertMessage.textContent = data.message;
    alertContainer.appendChild(alertMessage);

    if (alertsContainer !== null) {
        alertsContainer.appendChild(alertContainer);
    }
    setTimeout(function () {
        alertContainer.setAttribute("class", "hidden");
    }, 5000);
}
