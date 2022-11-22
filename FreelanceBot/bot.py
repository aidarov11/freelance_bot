from aiogram.utils import executor
from create_bot import dp
from handlers import user, moderator
from database import postgres_db

async def on_startup(_):
    print('Бот вышел в онлайн')
    postgres_db.sql_start()


user.register_handlers_user(dp)
moderator.register_handlers_moderator(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
