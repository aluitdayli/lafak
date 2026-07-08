"""
Локальный помощник для переезда базы на новый аккаунт.

Берёт вытащенный со старого сервера `nft_cache.db` и делает МАЛЕНЬКИЙ
`seed_backup.json` только с важными данными (юзеры, подписки, зеркала,
избранное, шаблоны, просмотренные) — без тяжёлого кэша NFT.

Зачем: если сам .db большой (>100 МБ, GitHub его не примет) или веб-загрузка
в /data не работает — кладёшь получившийся seed_backup.json в репозиторий,
деплоишь, и бот сам восстановит данные при старте (см. _maybe_seed_from_backup).

Запуск (рядом должны лежать и nft_cache.db-wal / -shm, если они есть):
    python make_seed.py nft_cache.db
    # → создаст seed_backup.json в текущей папке
"""
import json
import sqlite3
import sys

TABLES = [
    "subscriptions",
    "bot_users",
    "mirrors",
    "favorites",
    "user_templates",
    "viewed_users",
]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "nft_cache.db"
    con = sqlite3.connect(src)
    con.row_factory = sqlite3.Row
    out = {"version": 1, "tables": {}}
    for t in TABLES:
        try:
            rows = [dict(r) for r in con.execute(f"SELECT * FROM {t}")]
        except Exception as e:
            print(f"  ! таблица {t}: {e}")
            rows = []
        out["tables"][t] = rows
        print(f"  {t}: {len(rows)}")
    con.close()
    with open("seed_backup.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("→ seed_backup.json готов. Положи его в репозиторий и задеплой.")


if __name__ == "__main__":
    main()
