import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import yfinance as yf 
from pyowm import OWM

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city using pyowm.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    owm = OWM('e71c4faf46f390cfc2ada82a9a8e0d91')  # Ganti 'your_api_key'
    mgr = owm.weather_manager()

    try:
        print(f"Retrieving weather for {city}...")
        # Get the weather observation for the specified city
        observation = mgr.weather_at_place(city)
        weather = observation.weather
        temperature = weather.temperature('celsius')["temp"]
        status = weather.detailed_status
        report = (
            f"The weather in {city} is {status} with a temperature of {temperature}°C."
        )
        return {"status": "success", "report": report}
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while retrieving weather information: {str(e)}",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "jakarta":
        tz_identifier = "Asia/Jakarta"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


def get_stock_info(stock_symbol: str) -> dict:
    """Retrieves stock information for a given stock symbol using yfinance.

    Args:
        stock_symbol (str): The stock symbol for which to retrieve information.

    Returns:
        dict: status and result or error msg.
    """
    try:
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.info
        if "regularMarketPrice" in stock_info:
            price = stock_info["regularMarketPrice"]
            currency = stock_info.get("currency", "N/A")
            name = stock_info.get("shortName", stock_symbol)
            return {
                "status": "success",
                "report": f"Stock info for {stock_symbol} ({name}): {price} {currency}",
            }
        else:
            return {
                "status": "error",
                "error_message": f"Stock information for '{stock_symbol}' is not available.",
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while retrieving stock information: {str(e)}",
        }


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time, weather, and stock information in Indonesia."
    ),
    instruction=(
        "I can answer your questions about the time, weather, and stock information in Indonesia."
    ),
    tools=[get_weather, get_current_time, get_stock_info],
)