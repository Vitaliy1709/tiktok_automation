import random
import time

from playwright.sync_api import Page

from logger import logger
from tiktok.utils import safe_get_text


def watch_videos(page: Page, max_count: int, skip_percent: int):
    logger.info(f"Начинаем просмотр {max_count} видео (пропуск: {skip_percent}%)")

    links = page.locator('a[href*="/video/"]')
    hrefs = []
    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")
        if href and href not in hrefs:
            hrefs.append(href)

    if not hrefs:
        logger.error("Не найдено ни одного видео для просмотра.")
        return

    for idx, video_url in enumerate(hrefs[:max_count], start=1):
        logger.info(f"Видео {idx}/{max_count}: {video_url}")

        page.goto(video_url, timeout=15000)

        duration = 15

        try:
            time_div = page.locator("div.css-1cuqcrm-DivSeekBarTimeContainer.e1ya9dnw1")
            time_div.wait_for(timeout=8000)
            time_text = time_div.inner_text()

            if "/" in time_text:
                total_time_str = time_text.split("/")[-1].strip()
                minutes, seconds = map(int, total_time_str.split(":"))
                duration = minutes * 60 + seconds
                page.wait_for_load_state("networkidle", timeout=duration)
            else:
                logger.warning("Fallback 15 сек.")

        except Exception as e:
            pass

            try:

                author = safe_get_text(page, '[data-e2e="browse-username"]')
                caption = safe_get_text(page, '[data-e2e="browse-video-desc"]')
                likes = safe_get_text(page, '[data-e2e="like-count"]')
                comments = safe_get_text(page, '[data-e2e="comment-count"]')
                shares = safe_get_text(page, '[data-e2e="share-count"]')

                logger.info("Информация о видео:")
                logger.info(f"Автор: {author}")
                logger.info(f"Описание: {caption}")
                logger.info(f"Лайки: {likes}, Комментарии: {comments}, Репосты: {shares}")
                logger.info(f"Длительность: {duration} сек.")
                logger.info("-" * 50)

                time.sleep(duration)

            except Exception as e:
                logger.error(f"Ошибка при просмотре видео: {e}")
                continue

            if random.randint(1, 100) <= skip_percent:
                logger.info("Пропущено по skip_percent")
            else:
                logger.info(f"Просматриваем видео ({duration} сек)...")
                time.sleep(duration)
                logger.info("Просмотр завершён")

            time.sleep(2)

    logger.info("Все видео обработаны.")
