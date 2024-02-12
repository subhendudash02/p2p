if (!document.cookie) {
    window.location.replace("index.html");
}


let name = document.getElementById("name");

name.innerHTML = document.cookie;