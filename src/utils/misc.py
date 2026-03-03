def get_user_profile_url(tg_id: int) -> str:
    return f"tg://user?id={tg_id}"


def get_map_url(service: str, latitude: float, longitude: float) -> str:
    service = service.strip().lower()

    if service == "yandex":
        return f"https://yandex.ru/maps/?pt={longitude},{latitude}&z=17&l=map"

    if service == "google":
        return f"https://www.google.com/maps?q={latitude},{longitude}"

    raise ValueError(f"Unknown map service: {service}")
