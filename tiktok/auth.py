import os
import shutil
import sys
import time

from playwright.sync_api import Playwright, TimeoutError

from config import PROFILE_DIR
from logger import logger

USER_CHROME_PROFILE = PROFILE_DIR


def _find_chrome_executable() -> str:
    candidates = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        shutil.which("google-chrome"),
        shutil.which("chrome"),
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    raise RuntimeError("Google Chrome не найден на системе.")


def _is_logged_in(page) -> bool:
    try:
        login_button = page.locator('[data-e2e="top-login-button"]')
        if login_button.count() == 0 or not login_button.is_visible(timeout=2000):
            return True

        upload_icon = page.locator('[data-e2e="upload-icon"]')
        if upload_icon.is_visible(timeout=2000):
            return True


    except Exception:
        pass

    return False


def login_or_restore_session(playwright: Playwright):
    logger.info("Запуск Chrome с пользовательским профилем...")

    context = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_CHROME_PROFILE,
        headless=False,
        executable_path=_find_chrome_executable(),
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--window-size=1280,800",
        ],
    )

    page = context.pages[0] if context.pages else context.new_page()

    try:
        page.goto("https://www.tiktok.com", timeout=60000)
        time.sleep(5)

        if _is_logged_in(page):
            logger.info("Сессия восстановлена — вы уже вошли.")
            return context

        logger.info("Вход не обнаружен. Открываем страницу логина...")
        page.goto("https://www.tiktok.com/login", timeout=60000)
        logger.info("Выполните вход вручную (QR / Google / почта)...")

        for _ in range(120):
            time.sleep(1)
            if _is_logged_in(page):
                logger.info("Вход выполнен успешно.")
                return context

        logger.error("Вход в аккаунт не завершён. Выход из программы.")
        context.close()
        sys.exit(1)

    except TimeoutError:
        logger.error("Ошибка загрузки страницы TikTok.")
        context.close()
        sys.exit(1)

    return context
