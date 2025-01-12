from playwright.async_api import async_playwright, Page, Response
import json
import asyncio
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import date, timedelta
from sql import HotelPrice

@dataclass_json
class HotelDatePrice:
    ctyhocn: str
    lowest_rate: int
    arrival_date: str
    departure_date: str
    after_tax: int

# Handler for repsonses to request for hotel info
async def handle_response(response: Response) -> dict:
    if "https://www.hilton.com/graphql/customer?appName=dx-res-ui&operationName=hotel_shopAvailOptions_shopPropAvail&originalOpName=getShopAvail&bl=en&ctyhocn=" in response.url:
        try:
            resp = await response.body()
            myjson = json.loads(resp)

            

            return myjson
            # print(len(json.dumps(myjson)))
            # print(response.url)
            # with open(f"out.json", "w") as f:
            #     json.dump(myjson, f)
        except Exception as e:
            print(e)
            pass

# async def wrapper(arrival, departure, lowest_rate):

async def query_hilton(hotel_code: str, arrival_date: date):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Set up handler for all responses
        page.on("response", handle_response)

        ctyhocn = hotel_code.upper()
        arrive_str = date.strftime("%Y-%m-%d")
        depart_date = arrival_date + timedelta(days=1)
        depart_str = depart_date.strftime("%Y-%m-%d")

        url = f"https://www.hilton.com/en/book/reservation/rooms/?ctyhocn={ctyhocn}&arrivalDate={arrive_str}&departureDate={depart_str}&room1NumAdults=1&displayCurrency=USD"
        await page.goto(url)
        await asyncio.sleep(10) 
        await page.screenshot(path="screenshot2.png")

        # Close the browser
        await browser.close()

if __name__ == "__main__":
    asyncio.run(query_hilton())
