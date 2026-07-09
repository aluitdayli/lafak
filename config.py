"""
Конфигурация NFT Scanner V8.
"""
import os

# ── Telegram ──────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_БОТА")
BOT_USERNAME = os.getenv("BOT_USERNAME", "ВАШ_USERNAME_БОТА")
ADMIN_IDS = [8972415139, 8332982896]
TELEGRAM_API_SERVER = os.getenv("TELEGRAM_API_SERVER", "")

# ── Mini App ──────────────────────────────────
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://ваш-сайт.github.io/")

# ── Обязательная подписка на канал ────────────
# Бот требует подписку на этот канал для доступа.
# ВАЖНО: бот должен быть АДМИНИСТРАТОРОМ канала, иначе проверка не сработает
# (get_chat_member вернёт ошибку → бот пропускает юзеров, fail-open).
# Чтобы ОТКЛЮЧИТЬ проверку — задай REQUIRED_CHANNEL_ID=0 в окружении.
REQUIRED_CHANNEL_ID = int(os.getenv("REQUIRED_CHANNEL_ID", "-1004443359550"))
REQUIRED_CHANNEL_LINK = os.getenv(
    "REQUIRED_CHANNEL_LINK", "https://t.me/+CFZG6YGfCWFiMzIy"
)

# ── Платная подписка (доступ к боту) ──────────
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "lumpanut")      # без @
FREE_DAILY_LIMIT = int(os.getenv("FREE_DAILY_LIMIT", "5"))         # запросов/день без подписки
SUBSCRIPTION_PRICE_TON = float(os.getenv("SUBSCRIPTION_PRICE_TON", "0.5"))
TON_WALLET = os.getenv("TON_WALLET", "UQD-0F79RLLQRXuDU7DpNN1ndlK62iaPxdI4-7oF-odOsTLU")

# Встроенный HTTP-API для мини-аппа (статус подписки)
WEBAPI_HOST = os.getenv("WEBAPI_HOST", "0.0.0.0")
# Amvera направляет домен на порт 80 (или из env PORT). Для локали можно WEBAPI_PORT.
WEBAPI_PORT = int(os.getenv("PORT", os.getenv("WEBAPI_PORT", "80")))
WEBAPI_ENABLED = os.getenv("WEBAPI_ENABLED", "1") == "1"

# ── БД ────────────────────────────────────────
DB_PATH = os.getenv("DB_PATH", "/data/nft_cache.db")

# ── Скан ──────────────────────────────────────
MAX_CONCURRENT_REQUESTS = 150
REQUEST_TIMEOUT = 5
DELAY_BETWEEN_BATCHES = 0
PROGRESS_UPDATE_INTERVAL = 2  # секунд

# Прокси для peek.tg (обход блокировки IP дата-центра).
# peek.tg режет запросы с IP некоторых хостингов (Amvera → 403). Укажи HTTP(S)
# прокси с чистым IP, и все запросы к peek.tg пойдут через него.
# Формат: http://user:pass@host:port  или  http://host:port
PEEK_PROXY = os.getenv("PEEK_PROXY", "")

# Бюджет времени на фазу парсинга (сек). Больше = глубже скан = больше
# результатов (но дольше). По умолчанию ~3 мин.
PEEK_TIME_BUDGET = int(os.getenv("PEEK_TIME_BUDGET", "180"))

# ── Рандомный парсинг ─────────────────────────
RANDOM_COLLECTIONS_COUNT = 5
RANDOM_ITEMS_PER_COLLECTION = 100

# ── Пагинация ────────────────────────────────
GIFTS_PER_PAGE = 8
MODELS_PER_PAGE = 10
BACKDROPS_PER_PAGE = 10
RESULTS_PER_PAGE = 10        # юзеров на страницу (компактно, влезает в TG)
TOTAL_RESULTS = 200          # макс. результатов за скан

# ── Фильтры NFT ──────────────────────────────
#  код: (min, max, label)
NFT_COUNT_RANGES = {
    "1-3":  (1, 3,   "1–3 NFT"),
    "4-10": (4, 10,  "4–10 NFT"),
    "10+":  (10, 999999, "10+ NFT"),
    "any":  (0, 999999, "Любое кол-во"),
}
DEFAULT_NFT_RANGE = "any"
MAX_NFT_HARD_CAP = 999999

# ── Экспорт ──────────────────────────────────
CSV_DIR = os.getenv("CSV_DIR", "/data/exports")
