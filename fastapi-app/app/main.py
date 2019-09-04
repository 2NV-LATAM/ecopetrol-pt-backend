from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

WEATHER_URL = (
    "http://api.openweathermap.org/data/2.5/weather"
    "?appid=8581e5f4667acea0a6eefd7b19547122"
)

BRENT_URL = "https://api.oilpriceapi.com/v1/prices/"
BRENT_ENPOINTS = ["latest", "past_day", "past_week", "past_month", "past_year"]


@app.get("/weather/")
def get_weather(lat: float, lon: float):
    weather_url_request = f"{WEATHER_URL}&lat={lat}&lon={lon}"

    weather_api_response = requests.get(weather_url_request)
    if weather_api_response.status_code != 200:
        if weather_api_response.status_code == 400:
            return weather_api_response.json()
        else:
            raiseException(status_code=weather_api_response.status_code)

    return weather_api_response.json()


@app.get("/brent/{endpoint}")
def get_brent(endpoint: str):
    if endpoint not in BRENT_ENPOINTS:
        raiseException(status_code=400)

    brent_url_request = f"{BRENT_URL}{endpoint}"
    brent_api_headers = {
        "content-type": "application/json",
        "Authorization": "Token 0f5a96ed1f1c9312b89e587c9cf4d20a"
    }

    brent_api_response = requests.get(
        brent_url_request,
        headers=brent_api_headers
    )

    if brent_api_response.status_code != 200:
        raiseException(status_code=brent_api_response.status_code)

    return brent_api_response.json()


def raiseException(status_code):
    raise HTTPException(
        status_code=status_code,
        detail="Error. Por favor reportar a contacto@2nv.co"
    )
