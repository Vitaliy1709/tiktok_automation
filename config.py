from dotenv import load_dotenv
import os

load_dotenv()

SEARCH_QUERY = os.getenv("SEARCH_QUERY", "")
VIDEO_COUNT = int(os.getenv("VIDEO_COUNT", 10))
SKIP_PERCENT = int(os.getenv("SKIP_PERCENT", 12))
PROFILE_DIR = str(os.getenv("PROFILE_DIR"))
