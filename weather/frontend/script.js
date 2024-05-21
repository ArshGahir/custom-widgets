document.addEventListener('DOMContentLoaded', function() {
    const defaultLatitude = 43.7001;  // Example latitude for Toronto
    const defaultLongitude = -79.4163; // Example longitude for Toronto
    const defaultDays = 3;

    // Fetch weather data for default location
    fetchWeather(defaultLatitude, defaultLongitude, defaultDays);

    document.getElementById('customize-button').addEventListener('click', function() {
        window.open('customizer/index.html', 'Customizer', 'width=400,height=600');
    });
});

function fetchWeather(latitude, longitude, days) {
    fetch(`/weather?latitude=${latitude}&longitude=${longitude}&days=${days}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            const current = data.current;
            const daily = data.daily;
            const hourly = data.hourly;

            // Update current weather
            if (document.getElementById('city').style.display !== 'none') {
                document.getElementById('city').innerText = `Latitude: ${latitude}, Longitude: ${longitude}`;
            }
            if (document.getElementById('icon').style.display !== 'none') {
                document.getElementById('icon').src = `https://openweathermap.org/img/w/${current.weather_code}.png`;
            }
            if (document.getElementById('description').style.display !== 'none') {
                document.getElementById('description').innerText = current.weather_code; // Map to proper description
            }
            if (document.getElementById('temperature').style.display !== 'none') {
                document.getElementById('temperature').innerText = `${current.temperature_2m} K`;
            }

            // Update daily forecast
            const dailyForecastElem = document.getElementById('daily-forecast');
            if (dailyForecastElem.style.display !== 'none') {
                dailyForecastElem.innerHTML = '';
                daily.date.forEach((date, index) => {
                    dailyForecastElem.innerHTML += `
                        <div>${date}: Max ${daily.temperature_2m_max[index]} K, Min ${daily.temperature_2m_min[index]} K</div>
                    `;
                });
            }

            // Update hourly forecast
            const hourlyForecastElem = document.getElementById('hourly-forecast');
            if (hourlyForecastElem.style.display !== 'none') {
                hourlyForecastElem.innerHTML = '';
                hourly.date.forEach((date, index) => {
                    hourlyForecastElem.innerHTML += `
                        <div>${date}: Temp ${hourly.temperature_2m[index]} K</div>
                    `;
                });
            }

            // Update sun/moon info
            const sunMoonElem = document.getElementById('sun-moon');
            if (sunMoonElem.style.display !== 'none') {
                sunMoonElem.innerHTML = `
                    <div>Sunrise: ${daily.sunrise[0]}</div>
                    <div>Sunset: ${daily.sunset[0]}</div>
                `;
            }
        })
        .catch(error => console.error('Error fetching weather data:', error));
}
