import requests
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
import time
import uvicorn

from logs.logging_logic import logger

API_KEY = "12b787a589d34a61b3460947242303"
BASE_URL = "https://api.weatherapi.com/v1/current.json"
RATE_LIMIT = 5 
RATE_TIME = 10 
request_counts = {}
app = FastAPI()

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    ip = request.client.host
    current_time = time.time()
    if ip not in request_counts:
        request_counts[ip] = []
    request_counts[ip] = [ts for ts in request_counts[ip] if current_time - ts < RATE_TIME]
    if len(request_counts[ip]) >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for IP: {ip}")
        return JSONResponse(
            {"detail": "Rate limit exceeded."},
            status_code=429
        )
    
    request_counts[ip].append(current_time)
    response = await call_next(request) 
    return response
    

@app.get("/weather/{city}")
def get_weather(city: str):
    try:
        logger.info(f"Received request for weather in {city}")
        response = requests.get(BASE_URL, params={"key": API_KEY, "q": city})
        response.raise_for_status()
        data = response.json()
        data = {
            "city": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "Humidity": data["current"]["humidity"],
            "Wind": data["current"]["wind_kph"]
        }
        if not data:
            logger.warning(f"City {city} not found")
            return JSONResponse(status_code=404, content={"message": "City not found"})
        logger.info(f"Weather data for {city} retrieved successfully")
        return JSONResponse(status_code=200, content=data)
    
    except Exception as e:
        logger.warning(f"City {city} not found")
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)