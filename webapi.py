"""
Лёгкий HTTP-API для мини-аппа (статус подписки).

Эндпоинты (CORS открыт):
  GET  /api/status   ?initData=<tg webapp initData>  → статус подписки/лимитов

Безопасность: initData проверяется HMAC-подписью по BOT_TOKEN
(алгоритм Telegram WebApp). Подделать user_id нельзя.
"""
import hashlib
import hmac
import logging
from urllib.parse import parse_qsl

from aiohttp import web

from config import BOT_TOKEN, WEBAPI_HOST, WEBAPI_PORT, TON_WALLET, SUBSCRIPTION_PRICE_TON, SUPPORT_USERNAME
import subscription
import db

logger = logging.getLogger(__name__)


def _verify_init_data(init_data: str) -> dict | None:
    """Проверяет подпись initData. Возвращает dict полей или None."""
    if not init_data:
        return None
    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        recv_hash = pairs.pop("hash", None)
        if not recv_hash:
            return None
        check_string = "\n".join(f"{k}={pairs[k]}" for k in sorted(pairs))
        secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calc = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc, recv_hash):
            return None
        return pairs
    except Exception as e:
        logger.debug("initData verify error: %s", e)
        return None


def _user_id(pairs: dict) -> int | None:
    import json
    try:
        user = json.loads(pairs.get("user", "{}"))
        return int(user.get("id"))
    except Exception:
        return None


def _cors(resp: web.Response) -> web.Response:
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


async def _options(request):
    return _cors(web.Response())


async def handle_status(request):
    init_data = request.query.get("initData", "")
    pairs = _verify_init_data(init_data)
    if not pairs:
        return _cors(web.json_response({"error": "bad_init_data"}, status=401))
    uid = _user_id(pairs)
    if not uid:
        return _cors(web.json_response({"error": "no_user"}, status=400))
    st = await subscription.status(uid)
    st["price_ton"] = SUBSCRIPTION_PRICE_TON
    st["ton_wallet"] = TON_WALLET
    st["support"] = SUPPORT_USERNAME
    return _cors(web.json_response(st))


def build_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/api/status", handle_status)
    app.router.add_route("OPTIONS", "/api/{tail:.*}", _options)
    app.router.add_get("/", lambda r: web.json_response({"ok": True, "service": "nft-parser-api"}))
    return app


async def start_webapi():
    """Запускает HTTP-сервер в текущем event loop (не блокирует)."""
    app = build_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPI_HOST, WEBAPI_PORT)
    await site.start()
    logger.info("WebAPI запущен на %s:%s", WEBAPI_HOST, WEBAPI_PORT)
    return runner
