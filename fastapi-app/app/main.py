from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

WEATHER_URL = (
    "http://api.openweathermap.org/data/2.5/weather"
    "?appid=8581e5f4667acea0a6eefd7b19547122"
)


@app.get("/weather/")
def read_item(lat: float, lon: float):
    weather_url_request = f"{WEATHER_URL}&lat={lat}&lon={lon}"

    weather_api_response = requests.get(weather_url_request)
    if weather_api_response.status_code != 200:
        if weather_api_response.status_code == 400:
            return weather_api_response.json()
        else:
            raise HTTPException(
                status_code=400,
                detail="Error. Por favor reportar a contacto@2nv.co"
            )

    return weather_api_response.json()
