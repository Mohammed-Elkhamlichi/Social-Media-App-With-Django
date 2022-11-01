let alertContainer = document.getElementById("alerts_container") || null;
let closeAlert = document.getElementById("close_alert") || null;
if (alertContainer !== null) {
    setTimeout(function () {
        alertContainer.setAttribute("class", "transition  duration-1000 ease-in-out  -translate-x-full");
        closeAlert.setAttribute("class", "transition  duration-1000 ease-in-out  -translate-x-full");
    }, 5000);
} else {
    console.log("container not found");
}
console.log({ closeAlert });
if (closeAlert !== null) {
    closeAlert.addEventListener("click", (e) => {
        e.preventDefault();
        closeAlert.setAttribute("class", "transition  duration-1000 ease-in-out  translate-x-full");
        alertContainer.setAttribute("class", "transition  duration-400 ease-in-out  -translate-x-full");
    });
}
