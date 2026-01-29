import re
import sys
import os
import logging
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from dotenv import load_dotenv
from pypdf import PdfReader

# from utils.auth import create_auth0_verifier

# Load environment variables from .env file
load_dotenv()

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    stream=sys.stderr,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ricky-mcp")

# Get Auth0 configuration from environment
# auth0_domain = os.getenv("AUTH0_DOMAIN")
# resource_server_url = os.getenv("RESOURCE_SERVER_URL")

# if not auth0_domain:
#     raise ValueError("AUTH0_DOMAIN environment variable is required")
# if not resource_server_url:
#     raise ValueError("RESOURCE_SERVER_URL environment variable is required")

# Load server instructions
# with open("prompts/server_instructions.md", "r") as file:
#     server_instructions = file.read()

# Initialize Auth0 token verifier
# token_verifier = create_auth0_verifier()

# Create an MCP server with OAuth authentication
mcp = FastMCP("ricky-mcp")
    # "ricky-mcp",
    # instructions=server_instructions,
    # host="0.0.0.0",
    # OAuth Configuration
    # token_verifier=token_verifier,
    # auth=AuthSettings(
    #     issuer_url=AnyHttpUrl(f"https://{auth0_domain}/"),
    #     resource_server_url=AnyHttpUrl(resource_server_url),
    #     required_scopes=["openid", "profile", "email", "address", "phone"],
    # ),
# )

# --- HELPER FUNCTIONS --- #
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
            Event: {props.get("event", "Unknown")}
            Area: {props.get("areaDesc", "Unknown")}
            Severity: {props.get("severity", "Unknown")}
            Description: {props.get("description", "No description available")}
            Instructions: {props.get("instruction", "No specific instructions provided")}
            """
#

@mcp.tool()
def fetch_ricky_martin_data() -> str:
    """Retrieves the resume of an individual named Ricky Martin who built this MCP and resume will tell more about who this person is.

    Returns:
        str: Information about Ricky to answer questions
    """
    text = ""

    try:
        # Open the PDF file in read-binary mode
        with open('docs/Ricky.pdf', 'rb') as file_obj:
            # Create a PDF reader object
            reader = PdfReader(file_obj)
            # Iterate through all the pages and extract text
            for page in reader.pages:
                text += page.extract_text() or "" # Use an empty string if page.extract_text() returns None
        return str(text)
    except Exception:
        return "was not able to gather specified information"

@mcp.tool()
def fetch_instructions(prompt_name: str) -> str:
    """
    Fetch instructions for a given prompt name from the prompts/ directory

    Args:
        prompt_name (str): Name of the prompt to fetch instructions for
        Available prompts: 
            - write_complete_ppr

    Returns:
        str: Instructions for the given prompt
    """
    
    try:
        script_dir = os.path.dirname(__file__)
        prompt_path = os.path.join(script_dir, "prompts", f"{prompt_name}.md")
        with open(prompt_path, "r") as f:
            return f.read()
    except:
        return ""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
            {period["name"]}:
            Temperature: {period["temperature"]}°{period["temperatureUnit"]}
            Wind: {period["windSpeed"]} {period["windDirection"]}
            Forecast: {period["detailedForecast"]}
            """
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)
    

def main() -> None:
    # Helpful signal (to stderr) so you know it started.
    if sys.stdin.isatty():
        logger.warning(
            "Starting MCP server in STDIO mode. This will look idle until a client connects and sends requests."
        )
        logger.warning(
            "Run with an MCP client (Inspector/Claude Desktop/etc). Do not expect a 'listening on port' message for STDIO."
        )
    else:
        logger.info("Starting MCP server in STDIO mode (stdin is not a TTY).")

    # Start server (blocks)
    mcp.run(transport="stdio")
    # mcp.run(transport='streamable-http')


if __name__ == "__main__":
    main()