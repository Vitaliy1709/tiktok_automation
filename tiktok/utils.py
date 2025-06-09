import argparse
import sys

from config import SEARCH_QUERY, VIDEO_COUNT, SKIP_PERCENT
from logger import logger


def parse_args():
    parser = argparse.ArgumentParser(description="TikTok-бот")
    parser.add_argument("--query", type=str, default=SEARCH_QUERY, help="Поисковый запрос")
    parser.add_argument("--count", type=int, default=VIDEO_COUNT, help="Сколько видео просмотреть")
    parser.add_argument("--skip", type=int, default=SKIP_PERCENT, help="Процент пропуска видео")
    args = parser.parse_args()

    if not args.query:
        try:
            args.query = input("Введите поисковый запрос для TikTok: ").strip()
        except UnicodeDecodeError:
            logger.info("Ошибка кодировки ввода. Используйте английские символы.")
            sys.exit(1)
    return args


def safe_get_text(page, selector: str, default: str = "—") -> str:
    try:
        el = page.locator(selector)
        el.wait_for(state="attached", timeout=2000)
        return el.inner_text().strip()
    except Exception:
        return default
