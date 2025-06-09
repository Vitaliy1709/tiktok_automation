import time
from urllib.parse import quote

from playwright.sync_api import Page

from logger import logger


def perform_search(page: Page, query: str) -> bool:
    logger.info(f"Поиск видео: {query!r}")

    search_url = f"https://www.tiktok.com/search/video?q={quote(query)}"
    page.goto(search_url, timeout=15000)
    logger.info(f"Перешли по URL: {search_url}")

    for attempt in range(3):
        links = page.locator('a[href*="/video/"]')
        if links.count() > 0:
            logger.info(f"Найдено {links.count()} видео.")
            time.sleep(1)
            return True

        logger.warning(f"Видео не загрузились, попытка {attempt + 1}/3. Ждём 3 секунды...")
        time.sleep(3)

    logger.error("Видео так и не загрузились.")
    return False
