import requests

API_KEY = "5ad943af4f2a3082fa3e42820d6da32f"

city = input("Enter city name or ZIP code: ").strip()

if not city:
    print("Please enter a city name or ZIP code.")
else:
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            city_name = data["name"]
            country = data["sys"]["country"]
            temperature_c = data["main"]["temp"]
            temperature_f = (temperature_c * 9 / 5) + 32
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]

            print("Weather Report")
            print("City:", city_name)
            print("Country:", country)
            print(f"Temperature: {temperature_c:.1f} °C")
            print(f"Temperature: {temperature_f:.1f} °F")
            print("Humidity:", humidity, "%")
            print("Condition:", condition.title())
            print("Wind Speed:", wind_speed, "m/s")

        elif response.status_code == 401:
            error_data = response.json()
            print("API Error:", error_data.get("message", "Invalid API key."))

        elif response.status_code == 404:
            print("City not found.")

        elif response.status_code == 429:
            print("API request limit exceeded.")

        else:
            print("Unable to get weather information.")

    except requests.exceptions.Timeout:
        print("Request timed out.")

    except requests.exceptions.ConnectionError:
        print("Network connection problem.")

    except requests.exceptions.RequestException:
        print("Something went wrong.")
