from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from utils.messages import TODAY, UNKNOWN_MAP_SERVICE, YESTERDAY

MSK = ZoneInfo("Europe/Moscow")


def get_user_link(user_id: int, username: str | None = None) -> str:
    if username:
        return f"https://t.me/{username}"
    return f'tg://user?id={user_id}'


def get_map_url(service: str, latitude: float, longitude: float) -> str:
    service = service.strip().lower()

    if service == "yandex":
        return f"https://yandex.ru/maps/?pt={longitude},{latitude}&z=17&l=map"

    if service == "google":
        return f"https://www.google.com/maps?q={latitude},{longitude}"

    raise ValueError(UNKNOWN_MAP_SERVICE.format(service=service))


def format_datetime(dt: datetime) -> str:
    if not dt:
        return None
    
    now = datetime.now(MSK)
    dt = dt.astimezone(MSK)

    today = now.date()
    yesterday = today - timedelta(days=1)

    date = dt.date()

    if date == today:
        return f"{TODAY} • {dt.strftime('%H:%M')}"
    elif date == yesterday:
        return f"{YESTERDAY} • {dt.strftime('%H:%M')}"
    else:
        return dt.strftime("%d.%m.%Y • %H:%M")
