"""
Подписка и дневные лимиты.

Правила:
- Админы — безлимит, подписка им не нужна.
- С подпиской — безлимит (навсегда).
- Без подписки — FREE_DAILY_LIMIT запросов в день, сброс в 00:00 UTC.

Любой парсинг / обновление / поиск считается одним запросом.
"""
import db
from config import ADMIN_IDS, FREE_DAILY_LIMIT


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def status(user_id: int) -> dict:
    """Полный статус для UI/сообщений.

    Возвращает:
      subscribed: bool
      unlimited:  bool   (админ или подписчик)
      limit:      int    (дневной лимит)
      used:       int
      remaining:  int    (оставшиеся запросы; -1 = безлимит)
      is_admin:   bool
    """
    admin = is_admin(user_id)
    row = await db.sub_get(user_id)
    subscribed = bool(row.get("is_subscribed"))
    unlimited = admin or subscribed
    used = int(row.get("daily_usage") or 0)
    remaining = -1 if unlimited else max(0, FREE_DAILY_LIMIT - used)
    return {
        "subscribed": subscribed,
        "unlimited": unlimited,
        "limit": FREE_DAILY_LIMIT,
        "used": used,
        "remaining": remaining,
        "is_admin": admin,
    }


async def can_use(user_id: int) -> bool:
    """Можно ли выполнить запрос (без списания)."""
    if is_admin(user_id):
        return True
    row = await db.sub_get(user_id)
    if row.get("is_subscribed"):
        return True
    return int(row.get("daily_usage") or 0) < FREE_DAILY_LIMIT


async def consume(user_id: int) -> dict:
    """Пытается списать один запрос.

    Возвращает: {"ok": bool, "remaining": int|-1, "reason": str}
    Безлимитным (админ/подписчик) ничего не списывает.
    """
    if is_admin(user_id):
        return {"ok": True, "remaining": -1, "reason": "admin"}
    row = await db.sub_get(user_id)
    if row.get("is_subscribed"):
        return {"ok": True, "remaining": -1, "reason": "subscribed"}

    used = int(row.get("daily_usage") or 0)
    if used >= FREE_DAILY_LIMIT:
        return {"ok": False, "remaining": 0, "reason": "limit"}

    new_used = await db.sub_consume(user_id)
    return {"ok": True, "remaining": max(0, FREE_DAILY_LIMIT - new_used), "reason": "free"}


async def grant(user_id: int):
    await db.sub_set(user_id, True)


async def revoke(user_id: int):
    await db.sub_set(user_id, False)
