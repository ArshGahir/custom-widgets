document.getElementById('update-widget').addEventListener('click', function() {
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const days = document.getElementById('days').value;

    const showCity = document.getElementById('show-city').checked;
    const showTemperature = document.getElementById('show-temperature').checked;
    const showDailyForecast = document.getElementById('show-daily-forecast').checked;
    const showHourlyForecast = document.getElementById('show-hourly-forecast').checked;
    const showCurrentWeather = document.getElementById('show-current-weather').checked;
    const showSunMoon = document.getElementById('show-sun-moon').checked;

    const color = document.getElementById('color').value;

    if (!latitude || !longitude || !days) {
        alert('Please enter latitude, longitude, and number of days');
        return;
    }

    const widgetWindow = window.opener;
    widgetWindow.fetchWeather(latitude, longitude, days);

    // Update visibility of elements
    widgetWindow.document.getElementById('city').style.display = showCity ? 'block' : 'none';
    widgetWindow.document.getElementById('icon').style.display = showCurrentWeather ? 'block' : 'none';
    widgetWindow.document.getElementById('description').style.display = showCurrentWeather ? 'block' : 'none';
    widgetWindow.document.getElementById('temperature').style.display = showTemperature ? 'block' : 'none';
    widgetWindow.document.getElementById('daily-forecast').style.display = showDailyForecast ? 'block' : 'none';
    widgetWindow.document.getElementById('hourly-forecast').style.display = showHourlyForecast ? 'block' : 'none';
    widgetWindow.document.getElementById('sun-moon').style.display = showSunMoon ? 'block' : 'none';

    // Update color of elements
    widgetWindow.document.getElementById('city').style.color = color;
    widgetWindow.document.getElementById('temperature').style.color = color;
    widgetWindow.document.getElementById('description').style.color = color;
    widgetWindow.document.getElementById('daily-forecast').style.color = color;
    widgetWindow.document.getElementById('hourly-forecast').style.color = color;
    widgetWindow.document.getElementById('sun-moon').style.color = color;

    window.close();
});
