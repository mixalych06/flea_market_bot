from create_bot import bot, db, CHAT_ID_BL, CHAT_ID_BEL, ADMIN_ID
from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher
from keyboards.kb_users import keyword
import time


async def command_start(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'Я специальный бот для публикации объявлений на канале\n'
                                 f'<b> <a href="https://t.me/+zd5Iew3RoQg2ZGJi">Объявления Белогорск</a></b>\n'
                                 f'<b>Хотите разместить объявление? Нажмите кнопку</b>\n'
                                 f'<i>📌Подать объявление📌 и следуйте инструкции</i>\n'
                                 f'<b>Правила размещения:</b>\n'
                                 f'📍Личные не коммерческие объявления размещаются бесплатно\n'
                                 f'📍Все поля обязательны для заполнения\n'
                                 f'📍В разделе контактные данные указываем минимум один способ с вами связаться\n'
                                 f'📍Для исправления объявления в процессе подачи просто нажмите Отмена и начните заполнение снова.\n'
                                 f'📍После проверки ваше объявление появится на канале\n<i>С предложениями и вопросами обращаться к\n'
                                 f'<a href="https://t.me/mixalych06">администратору</a></i>',
                         parse_mode='HTML', reply_markup=keyword)
    # db.add_user(message.from_user.id)


async def command_help(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'Я специальный бот для публикации объявлений на канале\n'
                                 f'<b> <a href="https://t.me/+zd5Iew3RoQg2ZGJi">Объявления Белогорск</a></b>\n'
                                 f'<b>Хотите разместить объявление? Нажмите кнопку</b>\n'
                                 f'<i>📌Подать объявление📌 и следуйте инструкции</i>\n'
                                 f'<b>Правила размещения:</b>\n'
                                 f'📍Личные не коммерческие объявления размещаются бесплатно\n'
                                 f'📍Все поля обязательны для заполнения\n'
                                 f'📍В разделе контактные данные указываем минимум один способ с вами связаться\n'
                                 f'📍Для исправления объявления в процессе подачи просто нажмите Отмена и начните заполнение снова.\n'
                                 f'📍После проверки ваше объявление появится на канале\n<i>С предложениями и вопросами обращаться к\n'
                                 f'<a href="https://t.me/mixalych06">администратору</a></i>',
                         parse_mode='HTML', reply_markup=keyword)


class FSMAddAd(StatesGroup):
    city = State()
    photo = State()
    product_name = State()
    specifications = State()
    prise = State()
    contact = State()


async def add_start(message: types.Message):
    number_of_entries = db.number_of_entries_user_products(message.from_user.id)
    if number_of_entries >= 5 and message.from_user.id != ADMIN_ID:
        await message.answer(
            f'🚆Я пока не могу хранить в памяти больше 5-ти объявлений.\nПожалуйста нажмите кнопку Mои объявления и удалите не нужное.\n'
            f'Но ваше объявление останется опубликованым на канале')
        return
    else:
        await FSMAddAd.city.set()
        await message.reply('🚆Выберите ваш город.', reply_markup=InlineKeyboardMarkup().
                            add(InlineKeyboardButton("Благовещенск", callback_data=f"city|Благовещенск"),
                                InlineKeyboardButton("Белогорск", callback_data=f"city|Белогорск")).
                            add(InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_city(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        inline_command = callback_query.data.split('|')
        data['city'] = inline_command[1]
        await FSMAddAd.photo.set()
        await callback_query.message.reply('🚆Отправьте одно фото для обьявления',
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_ad(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data['photo_id'] = message.photo[0].file_id
        await FSMAddAd.next()
        await message.reply('🚆Введите название для обьявление', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_name(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data['product_name'] = message.text
        await FSMAddAd.next()
        await message.reply('🚆Теперь добавьте описание', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_specifications(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data['specifications'] = message.text
        await FSMAddAd.next()
        await message.reply('🚆Укажите цену', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prise'] = message.text
        await FSMAddAd.next()
        await message.reply('🚆Добавьте контактные данные', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_contact(message: types.Message, state: FSMContext):
    async  with state.proxy() as data:
        data['contact'] = message.text
        user = [message.from_id, message.from_user.first_name,
                time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())] + list(data.values())
        await state.finish()
        db.adds_user_products(user)
        id_ad_bd = db.exists_id_product(user[0], user[4])
        await bot.send_photo(message.from_id, photo=data['photo_id'],
                             caption=f"<u><b>{data['product_name'].strip().upper()}</b></u>\n"
                                     f"{data['specifications']}\n<b>Цена: </b>{data['prise']}\n"
                                     f"<i><b>{data['contact']}</b></i>",
                             parse_mode='HTML',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton("Отправить на проверку",
                                                      callback_data=f"sends_to_admin:{id_ad_bd}"),
                                 InlineKeyboardButton("Удалить", callback_data=f"del:{id_ad_bd}")))


async def del_ad(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    db.del_ad_bd(inline_command[1])
    await callback_query.answer(text='🚆Обьявление удалено',
                                show_alert=True)
    await callback_query.message.delete()


async def del_one_ad(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    db.del_ad_bd(inline_command[1])
    try:
        if inline_command[3] == 'Благовещенск':
            await bot.delete_message(CHAT_ID_BL, int(inline_command[2]))
            await callback_query.answer(text='🚆Объявление удалено',
                                        show_alert=True)
        elif inline_command[3] == 'Белогорск' or not inline_command[3]:
            await bot.delete_message(CHAT_ID_BEL, int(inline_command[2]))
            await callback_query.answer(text='🚆Объявление удалено',
                                        show_alert=True)
    except MessageCantBeDeleted:
        await callback_query.answer(text='🚆Объявление удалено',
                                    show_alert=True)
    except MessageToDeleteNotFound:
        await callback_query.answer(text='🚆Не получается показать объявление.\n'
                                         'Нажмите на кнопку 📌Мои объявления📌', cache_time=2,
                                    show_alert=True)


async def cancel_fsm(callback_query: types.CallbackQuery, state: FSMContext):
    '''Отмена ввода обьявления, сброс машины состояния'''
    await state.reset_state()
    inline_command = callback_query.data
    await callback_query.answer(
        text='🚆Вы прервали подачу объявления. Для повторной подачи нажмите не кнопку\n👇👇👇Подать объявление.👇👇👇',
        show_alert=True)
    await callback_query.message.delete()


async def user_ad_all_bd(message: types.Message):
    '''Обрабатывает нажатие кнопки мои объявления'''
    all_prod = db.user_products(message.from_user.id)
    number = 0
    if all_prod:
        if len(all_prod) == 1:
            await bot.send_photo(message.from_user.id, photo=all_prod[number][4],
                                 caption=f"<u><b>{all_prod[number][5].strip().upper()}</b></u>\n{all_prod[number][6]}\n"
                                         f"<b>Цена: </b>{all_prod[number][7]}\n<i>{all_prod[number][8]}</i>\n"
                                         f"<i>опубликовано на канале Обьявления {all_prod[number][10]}</i>",
                                 parse_mode='HTML',
                                 reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                     InlineKeyboardButton(str(number + 1) + '/' + str(len(all_prod)),
                                                          callback_data="null"),
                                     InlineKeyboardButton('❌',
                                                          callback_data=f"delete:{all_prod[number][0]}:"
                                                                        f"{all_prod[number][9]}:"
                                                                        f"{all_prod[number][10]}")))
        elif len(all_prod) > 1:
            await bot.send_photo(message.from_user.id, photo=all_prod[number][4],
                                 caption=f"<u><b>{all_prod[number][5].strip().upper()}</b></u>\n{all_prod[number][6]}\n"
                                         f"<b>Цена: </b>{all_prod[number][7]}\n<i>{all_prod[number][8]}</i>\n"
                                         f"<i>опубликовано на канале Обьявления {all_prod[number][10]}</i>",
                                 parse_mode='HTML',
                                 reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                     InlineKeyboardButton("<<<", callback_data=f"next:{len(all_prod) - 1}"),
                                     InlineKeyboardButton(str(number + 1) + '/' + str(len(all_prod)),
                                                          callback_data="null"),
                                     InlineKeyboardButton('❌',
                                                          callback_data=f"delete:{all_prod[number][0]}:"
                                                                        f"{all_prod[number][9]}:"
                                                                        f"{all_prod[number][10]}"),
                                     InlineKeyboardButton(">>>", callback_data=f"next:{number + 1}")))
            return

    else:
        await message.answer('🚆У вас нет обьявлений')


async def next_ad(callback_query: types.CallbackQuery):
    '''Обрабатывает кнопки вперёд назад удалить при просмотре своих объявлений'''
    inline_command = callback_query.data.split(':')
    all_prod = db.user_products(callback_query.from_user.id)
    number = int(inline_command[1])
    try:
        phot = InputMediaPhoto(media=all_prod[number][4],
                               caption=f"<u><b>{all_prod[number][5].strip().upper()}</b></u>\n{all_prod[number][6]}\n"
                                       f"<b>Цена: </b>{all_prod[number][7]}\n<i>{all_prod[number][8]}</i>\n"
                                       f"<i>опубликовано на канале Обьявления {all_prod[number][10]}</i>",
                               parse_mode='HTML')
        if 0 < number < len(all_prod) - 1:
            await callback_query.bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                        message_id=callback_query.message.message_id,
                                                        media=phot, reply_markup=InlineKeyboardMarkup(row_width=4).add(
                    InlineKeyboardButton("<<<", callback_data=f"next:{number - 1}"),
                    InlineKeyboardButton(str(number + 1) + '/' + str(len(all_prod)), callback_data="null"),
                    InlineKeyboardButton('❌', callback_data=f"delete:{all_prod[number][0]}:"
                                                            f"{all_prod[number][9]}:"
                                                            f"{all_prod[number][10]}"),
                    InlineKeyboardButton(">>>", callback_data=f"next:{number + 1}")))
        elif number == 0:
            await callback_query.bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                        message_id=callback_query.message.message_id,
                                                        media=phot, reply_markup=InlineKeyboardMarkup(row_width=4).add(
                    InlineKeyboardButton("<<<", callback_data=f"next:{len(all_prod) - 1}"),
                    InlineKeyboardButton(str(number + 1) + '/' + str(len(all_prod)), callback_data="null"),
                    InlineKeyboardButton('❌', callback_data=f"delete:{all_prod[number][0]}:"
                                                            f"{all_prod[number][9]}:"
                                                            f"{all_prod[number][10]}"),
                    InlineKeyboardButton(">>>", callback_data=f"next:{number + 1}")))
        elif number == len(all_prod) - 1:
            await callback_query.bot.edit_message_media(chat_id=callback_query.message.chat.id,
                                                        message_id=callback_query.message.message_id,
                                                        media=phot, reply_markup=InlineKeyboardMarkup(row_width=4).add(
                    InlineKeyboardButton("<<<", callback_data=f"next:{number - 1}"),
                    InlineKeyboardButton(str(number + 1) + '/' + str(len(all_prod)), callback_data="null"),
                    InlineKeyboardButton('❌', callback_data=f"delete:{all_prod[number][0]}:"
                                                            f"{all_prod[number][9]}:"
                                                            f"{all_prod[number][10]}"),
                    InlineKeyboardButton(">>>", callback_data=f"next:{0}")))
    except IndexError:
        await callback_query.answer('🚆Не получается показать объявление.\nНажмите на кнопку 📌Мои объявления📌',
                                    cache_time=2)


async def eho(message: types.Message):
    await message.answer(message.text, reply_markup=keyword)


def register_handler_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_help, text=['🆘Помощь'])
    dp.register_message_handler(add_start, text=['📌Подать объявление📌'], state=None)
    dp.register_message_handler(user_ad_all_bd, text=['Мои объявления'])
    dp.register_callback_query_handler(add_city, lambda x: x.data.startswith('city'), state=FSMAddAd.city)
    dp.register_message_handler(add_ad, content_types=['photo'], state=FSMAddAd.photo)
    dp.register_message_handler(add_product_name, state=FSMAddAd.product_name)
    dp.register_message_handler(add_specifications, state=FSMAddAd.specifications)
    dp.register_message_handler(add_price, state=FSMAddAd.prise)
    dp.register_message_handler(add_contact, state=FSMAddAd.contact)
    dp.register_callback_query_handler(cancel_fsm, lambda x: x.data.startswith('cancel'), state='*')
    dp.register_callback_query_handler(del_one_ad, lambda x: x.data.startswith('delete'))
    dp.register_callback_query_handler(next_ad, lambda x: x.data.startswith('next'))
    dp.register_callback_query_handler(del_ad, lambda x: x.data.startswith('del'))
    dp.register_message_handler(eho)
