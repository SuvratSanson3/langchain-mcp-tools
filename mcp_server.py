import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.utilities import GoogleSerperAPIWrapper

# importing the weather api key
load_dotenv("key.env")
weather_api_key = os.getenv("weather_api_key")
serper_api_key = os.getenv("serper_api_key")
os.environ["SERPER_API_KEY"] = serper_api_key

mcp = FastMCP("My App")

# Creating the mcp tools
@mcp.tool(name="calculate_bmi")
def calculate_bmi(weight_kg:float, height_m:float) -> float:
    """
    Calculate the Body Mass Index (BMI) from weight (kg) and height (meters).
    """
    return weight_kg/(height_m**2)

@mcp.tool(name="get_current_weather")
async def get_current_weather(city:str) -> str:
    """
    Fetch current weather conditions for a specified city using WeatherAPI.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no")
        return response.text
    
@mcp.tool(name="search_wikipedia")
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for a query and return a concise summary.
    """
    wikipedia_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=500)
    wikipedia_tool = WikipediaQueryRun(api_wrapper=wikipedia_wrapper)
    return wikipedia_tool.run(query)

@mcp.tool(name="search_arxiv")
def search_arxiv(query: str) -> str:
    """
    Search arXiv for academic papers relevant to the given query.
    """
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=500)
    arxiv_tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
    return arxiv_tool.run(query)


@mcp.tool(name="search_google_serper")
def search_google_serper(query: str) -> str:
    """
    Perform a web search using the Google Serper API and return the top result.
    """
    search = GoogleSerperAPIWrapper()
    return search.run(query)
    
if __name__ == "__main__":
    print("\n--- Starting FastMCP Server via __main__ ---")
    mcp.run()
