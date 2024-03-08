if (!document.cookie) {
    window.location.replace("index.html");
}

let backend = "http://localhost:8000/";
let energy_units = document.getElementById("energy_units");
let energy_forecast = document.getElementById("energy_forecast");
let profit_pref = document.getElementById("profit_pref");

let name = document.getElementById("name");

form.addEventListener('submit', async event => {
    event.preventDefault();

    const data = {
        storageUnits: energy_units.value,
        loadForecast: energy_forecast.value,
        profitPref: profit_pref.value / 100
    };

    try {
        const res = await fetch(
        backend + "energy/x",
        {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        },
        );

        const resData = await res.json();
        console.log(resData);

    } catch (err) {
        console.log(err.message);
    }
});

name.innerHTML = document.cookie;