import logging

from playwright.sync_api import sync_playwright

from logger import setup_logger
from tiktok.auth import login_or_restore_session
from tiktok.search import perform_search
from tiktok.utils import parse_args
from tiktok.video_watcher import watch_videos


def main():
    args = parse_args()
    logger = setup_logger(name="tiktok_bot", log_file="tiktok_run.log", level=logging.INFO)
    logger.info("Запуск TikTok-бота")

    with sync_playwright() as p:
        context = login_or_restore_session(p)
        page = context.pages[0]

        page.locator('[data-e2e="nav-search"]').wait_for(state="visible", timeout=15000)

        if not perform_search(page, args.query):
            logger.error("Видео нет, выходим.")
            context.close()
            return

        watch_videos(page, max_count=args.count, skip_percent=args.skip)

        context.close()
        logger.info("Работа завершена")


if __name__ == "__main__":
    main()
