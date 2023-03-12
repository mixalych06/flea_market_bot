from aiogram.utils import executor
from create_bot import dp
from handlers.h_users import register_handler_users
from handlers.h_admin import register_handler_admin


register_handler_admin(dp)
register_handler_users(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
