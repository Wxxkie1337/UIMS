def singleton(cls):
    instances = {}
    
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

def ensure_connected(func):
    async def wrapper(self, *args, **kwargs):
        if self._connection is None:
            raise RuntimeError("База данных не подключена. Вызовите метод connect() перед использованием.")
        return await func(self, *args, **kwargs)
    return wrapper

def get_user_profile_url(tg_id: int) -> str:
    """Возвращает ссылку на профиль Telegram по Telegram ID"""
    return f"tg://user?id={tg_id}"