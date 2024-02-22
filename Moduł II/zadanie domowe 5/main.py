import aiohttp
import argparse
import json
from datetime import datetime, timedelta


async def fetch_exchange_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get('URL_NBP_API') as response:
            data = await response.json()
            return data


def process_exchange_rates(data):
    pass


async def main():
    parser = argparse.ArgumentParser(
        description='Fetch exchange rates from NBP API')
    parser.add_argument('days', type=int, help='Number of days to look back')
    args = parser.parse_args()

    # Pobierz dane z API NBP
    data = await fetch_exchange_rates()

    # Przetwórz i wyświetl dane
    processed_data = process_exchange_rates(data)
    print(processed_data)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
