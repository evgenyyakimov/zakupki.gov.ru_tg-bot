import datetime
from bs4 import BeautifulSoup
import aiohttp
import aiofiles
import asyncio
from aiocsv import AsyncWriter


async def get_data():
    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?recordsPerPage=_50&fz44=on&af=on'

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36',
    }

    async with aiohttp.ClientSession() as session:
        result = await session.get(url, headers=headers)

        soup = BeautifulSoup(await result.text(), 'lxml')

        div_block = soup.find('div', 'search-registry-entrys-block').find_all(
            'div', 'row no-gutters registry-entry__form mr-0')
        # div_block = div.find_all('div', 'row no-gutters registry-entry__form mr-0')

        csv_data = []
        for div in div_block:
            link = div.find('a')['href'].strip()
            num = div.find('div', 'registry-entry__header-mid__number').text.strip()
            body = div.find('div', 'registry-entry__body-value').text.strip()
            price = div.find('div', 'price-block').find('div', 'price-block__value').text.strip()
            customer = div.find('div', 'registry-entry__body-href').text.strip()
            date = div.find('div', 'data-block mt-auto').find('div', 'data-block__value').text.strip()

            csv_data.append(
                [link, num, body, price, customer, date]
            )

    async with aiofiles.open(f'{cur_time}.csv', 'w', encoding='utf-8') as file:
        writer = AsyncWriter(file)

        await writer.writerow(
            [
                'Ссылка',
                'Номер закупки',
                'Объект закупки',
                'Начальная цена',
                'Заказчик',
                'Дата окончания подачи заявок',
            ]
        )
        await writer.writerow(csv_data)

    return f'{cur_time}.csv'


async def main():
    await get_data()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
