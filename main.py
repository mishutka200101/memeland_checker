import asyncio
from itertools import cycle
from os import mkdir
from os.path import exists
from sys import stderr

from better_proxy import Proxy
from loguru import logger

from core import start_checker
from utils import format_private_key
from utils import loader
from data.config import THREADS

logger.remove()
logger.add(stderr, format='<white>{time:HH:mm:ss}</white>'
                          ' | <level>{level: <8}</level>'
                          ' | <cyan>{line}</cyan>'
                          ' - <white>{message}</white>')


async def main() -> None:
    tasks: list = [
        asyncio.create_task(coro=start_checker(private_key=current_account,
                                               proxy=next(proxies_cycled) if proxies_cycled else None,
                                               link=next(links_list) if proxies_cycled else None))
        for current_account in accounts_list
    ]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    if not exists(path='result'):
        mkdir(path='result')

    with open(file='data/proxies.txt',
              mode='r',
              encoding='utf-8-sig') as file:
        proxies_list: list[str] = [Proxy.from_str(
            proxy=row.strip()).as_url for row in file]

    with open(file='data/accounts.txt',
              mode='r',
              encoding='utf-8-sig') as file:
        accounts_list: list[str] = [
            format_private_key(row.strip()) for row in file]

    with open(file='data/links.txt',
              mode='r',
              encoding='utf8-sig') as file:
        links_list = list[str] = [row.strip() for row in file]

    accounts_list: list[str] = [
        current_account for current_account in accounts_list if current_account]

    logger.success(
        f'Успешно загружено {len(accounts_list)} Accounts / {len(proxies_list)} Proxies')

    print()
    loader.semaphore = asyncio.Semaphore(value=THREADS)

    if proxies_list:
        proxies_cycled: cycle = cycle(proxies_list)
        links_cycled: cycle = cycle(links_list)
    else:
        proxies_cycled: None = None

    asyncio.run(main())

    logger.success('Работа успешно завершена')
    input('\nPress Enter to Exit..')
