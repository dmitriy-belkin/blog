from hypercorn.config import Config
from hypercorn.asyncio import serve

config = Config()
config.bind = ["0.0.0.0:8000"]
config.alpn_protocols = ["h3", "h2", "http/1.1"]  # Включаем поддержку HTTP/3
config.quic_bind = ["0.0.0.0:8000"]  # Добавляем поддержку QUIC
config.access_log = "-"  # Вывод логов доступа в консоль
config.error_log = "-"   # Вывод логов ошибок в консоль
config.loglevel = "debug"

async def main():
    import main as app  # Импортируем ваше FastAPI приложение
    await serve(app.app, config)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
