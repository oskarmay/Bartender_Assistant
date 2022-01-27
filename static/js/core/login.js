const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());

let memo = sessionStorage.getItem("first_try")
if (params["login"] && params["password"] && memo === null) {
    document.querySelector("#id_username").value = params["login"]
    document.querySelector("#id_password").value = params["password"]
    document.querySelector(".btn").click()
    sessionStorage.setItem("first_try", "true")
}
