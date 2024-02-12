if (document.cookie) {
    window.location.replace("home.html");
}

const form = document.getElementById('form');

function createCookie(name,value,minutes) {
    if (minutes) {
        var date = new Date();
        date.setTime(date.getTime()+(minutes*60*1000));
        var expires = "; expires="+date.toGMTString();
    } else {
        var expires = "";
    }
    document.cookie = name+"="+value+expires+"; path=/";
}

let backend = "https://unity-johnson-rapidly-sale.trycloudflare.com/";

form.addEventListener('submit', async event => {
    event.preventDefault();

    const data = new FormData(form);

    try {
        const res = await fetch(
        backend + "auth/login/",
        {
            method: 'POST',
            body: data,
        },
        );

        const resData = await res.json();
        createCookie("username", resData.username, 30);

    } catch (err) {
        console.log(err.message);
    }
});
