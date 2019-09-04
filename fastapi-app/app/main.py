from fastapi import FastAPI, HTTPException
import json
import requests
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


ECOPETROL_SHARES_URL = (
    "https://www.google.com/async/finance_wholepage_price_updates?ei="
    f"aQ9vXczCHYq45gLJzZPYDA&yv=3&async=mids:%2Fg%2F11dx9gnmzd,currencies:,"
    "_fmt:jspb"
)

BRENT_ENPOINTS = ["latest", "past_day", "past_week", "past_month", "past_year"]
BRENT_URL = "https://api.oilpriceapi.com/v1/prices/"

WEATHER_URL = (
    "http://api.openweathermap.org/data/2.5/weather"
    "?appid=8581e5f4667acea0a6eefd7b19547122"
)


@app.get("/ecopetrol_shares/")
def get_ecopetrol_shares():
    ecopetrol_shares_api_response = requests.get(
        ECOPETROL_SHARES_URL
    )

    if ecopetrol_shares_api_response.status_code != 200:
        raiseException(
            status_code=ecopetrol_shares_api_response.status_code
        )

    ecopetrol_shares_api_response = ecopetrol_shares_api_response.text.replace(
        ')]}\'',
        ''
    )
    ecopetrol_shares_api_response = json.loads(ecopetrol_shares_api_response)

    root_json_response = ecopetrol_shares_api_response[
        "PriceUpdate"
    ][0][0][0]

    closed_date = root_json_response[15][4]
    price = root_json_response[17][3]
    price_after_closing = root_json_response[15][0]
    variation = root_json_response[17][5]
    variation_after_closing = root_json_response[15][1]
    variation_percent = root_json_response[17][6]
    variation_percent_after_closing = root_json_response[15][2]

    return {
        "closed_date": closed_date,
        "price": price,
        "price_after_closing": price_after_closing,
        "variation": variation,
        "variation_after_closing": variation_after_closing,
        "variation_percent": variation_percent,
        "variation_percent_after_closing": variation_percent_after_closing
    }


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


def raiseException(status_code):
    raise HTTPException(
        status_code=status_code,
        detail="Error. Por favor reportar a contacto@2nv.co"
    )
