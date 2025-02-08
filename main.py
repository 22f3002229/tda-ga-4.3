from fastapi import FastAPI, Query
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Allow all methods
)


@app.get("/country-outline")
async def get_country_outline(country: str = Query(..., description="Country name to fetch Wikipedia page for")):
    url = f"https://en.wikipedia.org/wiki/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        markdown_outline = ""
        
        for heading in headings:
            level = int(heading.name[1])
            markdown_outline += f"{'#' * level} {heading.text.strip()}\n"
        
        return {"country": country, "outline": markdown_outline}

# To run the application, use the command: uvicorn filename:app --reload