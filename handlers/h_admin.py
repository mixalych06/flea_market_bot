from aiogram import types, Dispatcher
from create_bot import bot, db, CHAT_ID_BL, CHAT_ID_BEL, ADMIN_ID
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMRefusalAd(StatesGroup):
    photo = State()
    product_name = State()
    specifications = State()
    prise = State()
    contact = State()


async def sends_to_admin(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    ad = db.exists_product(inline_command[1])[0]
    await callback_query.answer(text=f'🚆Объявление {ad[5]} отправлено на проверку',
                                show_alert=True)
    await callback_query.message.delete()
    await bot.send_photo(ADMIN_ID, photo=ad[4],
                         caption=f"<b>{ad[5].strip().upper()}</b>\n{ad[6]}\n<b>Цена: </b>{ad[7]}\n"
                                 f"<i>{ad[8]}</i>\n{ad[10]}", parse_mode='HTML',
                         reply_markup=InlineKeyboardMarkup().add(
                             InlineKeyboardButton("Опубликовать", callback_data=f"add_ad:{ad[0]}"),
                             InlineKeyboardButton("Отказ", callback_data=f"refusal:{ad[0]}")))


async def refusal_ad(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    await callback_query.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton("не корректное название", callback_data=f"not publ:{inline_command[1]}:0"),
            InlineKeyboardButton("не корректное описание", callback_data=f"not publ:{inline_command[1]}:1"),
            InlineKeyboardButton("не корректная цена", callback_data=f"not publ:{inline_command[1]}:2"),
            InlineKeyboardButton("не корректный контакт", callback_data=f"not publ:{inline_command[1]}:3"),
            InlineKeyboardButton("реклама", callback_data=f"not publ:{inline_command[1]}:4"),
            InlineKeyboardButton("Не публикуем", callback_data=f"not publ:{inline_command[1]}:5")))


async def sends_to_chat(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    ad = db.exists_product(inline_command[1])[0]
    await bot.send_message(ad[1], text=f'Объявление {ad[5]} опубликовано на канале Объявления {ad[10]}')
    if ad[10] == 'Благовещенск':
        x = await bot.send_photo(CHAT_ID_BL, photo=ad[4],
                                 caption=f"<b>{ad[5].strip().upper()}</b>\n{ad[6]}\n<b>Цена: </b>{ad[7]}\n"
                                         f"<i>{ad[8]}</i>", parse_mode='HTML')
        db.update_value(x["message_id"], ad[0])
        await callback_query.message.delete()
    elif ad[10] == 'Белогорск':
        x = await bot.send_photo(CHAT_ID_BEL, photo=ad[4],
                                 caption=f"<b>{ad[5].strip().upper()}</b>\n{ad[6]}\n<b>Цена: </b>{ad[7]}\n"
                                         f"<i>{ad[8]}</i>", parse_mode='HTML')
        db.update_value(x["message_id"], ad[0])
        await callback_query.message.delete()


async def not_publ(callback_query: types.CallbackQuery):
    reason_for_failure = ('Не корректно указано название', 'Не корректное описание', 'Не корректная цена',
                          'Не корректная контактная информация', 'Расценено как коммерческое\n'
                                                                 'Стоимость размещения 50 руб.\n'
                                                                 'Разместить+закрепить на 3 суток - 100 руб.\n'
                                                                 'для оплаты свяжитесь с'
                                                                 '<a href="https://t.me/mixalych06">администратором</a>',
                          'Подобные объявления не публикуются')
    inline_command = callback_query.data.split(':')
    ad = db.exists_product(inline_command[1])[0]
    await bot.send_message(ad[1], text=f'Объявление {ad[5]} не опубликовано.\nПричина:\n'
                                       f'{reason_for_failure[int(inline_command[2])]}', parse_mode='HTML')
    db.del_ad_bd(ad[0])
    await callback_query.message.delete()


async def add_col(message: types.Message):
    db.add_column()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(add_col, commands=['add_col'])
    dp.register_callback_query_handler(sends_to_admin, lambda x: x.data.startswith('sends_to_admin'))
    dp.register_callback_query_handler(refusal_ad, lambda x: x.data.startswith('refusal'))
    dp.register_callback_query_handler(not_publ, lambda x: x.data.startswith('not publ'))
    dp.register_callback_query_handler(sends_to_chat, lambda x: x.data.startswith('add_ad'))
