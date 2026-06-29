"""
CryptoBot (Crypto Pay API) — создание счетов и проверка оплаты.
Документация: https://help.crypt.bot/crypto-pay-api
"""
import logging

import aiohttp

from config import CRYPTOBOT_TOKEN, CRYPTOBOT_API, CRYPTOBOT_ASSET, SUBSCRIPTION_PRICE_TON

logger = logging.getLogger(__name__)


def _headers() -> dict:
    return {"Crypto-Pay-API-Token": CRYPTOBOT_TOKEN}


async def create_invoice(user_id: int, amount: float | None = None,
                         description: str = "Подписка на NFT Parser") -> dict | None:
    """Создаёт счёт. Возвращает {invoice_id, pay_url} либо None."""
    amount = amount if amount is not None else SUBSCRIPTION_PRICE_TON
    payload = {
        "asset": CRYPTOBOT_ASSET,
        "amount": str(amount),
        "description": description,
        "payload": str(user_id),
        "allow_comments": False,
        "expires_in": 3600,
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{CRYPTOBOT_API}/createInvoice", json=payload,
                              headers=_headers(),
                              timeout=aiohttp.ClientTimeout(total=15)) as r:
                data = await r.json()
        if not data.get("ok"):
            logger.error("CryptoBot createInvoice error: %s", data)
            return None
        res = data["result"]
        return {
            "invoice_id": res["invoice_id"],
            "pay_url": res.get("bot_invoice_url") or res.get("pay_url")
                       or res.get("mini_app_invoice_url"),
        }
    except Exception as e:
        logger.error("CryptoBot createInvoice exception: %s", e)
        return None


async def get_invoice(invoice_id: int) -> dict | None:
    """Возвращает данные счёта (в т.ч. status: active|paid|expired)."""
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{CRYPTOBOT_API}/getInvoices",
                             params={"invoice_ids": str(invoice_id)},
                             headers=_headers(),
                             timeout=aiohttp.ClientTimeout(total=15)) as r:
                data = await r.json()
        if not data.get("ok"):
            return None
        items = data["result"].get("items", [])
        return items[0] if items else None
    except Exception as e:
        logger.debug("CryptoBot getInvoice exception: %s", e)
        return None
