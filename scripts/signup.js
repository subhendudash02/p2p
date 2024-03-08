const signup = document.getElementById('form_signup');
const username = document.getElementById("username");
const password = document.getElementById("password");
const email = document.getElementById("email");

let backend = "http://localhost:8000/";

signup.addEventListener('submit', async event => {
    const data = {
        username: username.value,
        password: password.value,
        email: email.value
    };
    console.log(data);
    event.preventDefault();
    try {
        const res = await fetch(
        backend + "auth/signup/",
        {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        },
        );

        const resData = await res.json();
        console.log(resData);
        alert("Account Made");
        window.Location.replace("index.html");

    } catch (err) {
        console.log(err.message);
        alert("Error!");
    }
});
