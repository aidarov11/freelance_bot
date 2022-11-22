from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot

# Keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import menu_kb, menu_kb2, cancel_kb, categories_kb
# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# DB
from database import postgres_db
# Other
import config

async def start_command(message: types.Message):
    if not await postgres_db.check_user(message.from_user.id):
        await postgres_db.add_user(message)
    else:
        print(f'{message.chat.first_name} already exists')


    if await postgres_db.get_user_status(message.from_user.id) == 0:
        await bot.send_message(message.chat.id, config.WELCOME, reply_markup=menu_kb)
    else:
        await bot.send_message(message.chat.id, config.WELCOME, reply_markup=menu_kb2)


async def show_adverts_handler(message: types.Message):
    adverts = await postgres_db.get_adverts();

    if adverts:
        for advert in adverts:
            await bot.send_message(message.chat.id, f'#{advert[2].replace(" ", "_")}\n<b>{advert[0]}</b>\n\n<code>{advert[1]}</code>\n\n<b>Контакты:</b>\n<code>{advert[5]}</code>\n\n<b>Дедлайн:</b> <code>{advert[3]}</code>\n<b>Бюджет:</b> <code>{advert[4]}</code>', parse_mode='html')
    else:
        await bot.send_message(message.chat.id, '<b>Список заданий пуст.</b>\n\n<code>Мы обязательно уведомим вас о новых заданиях</code>', parse_mode='html')


async def soft_delete_advert_callback(callback_query: types.CallbackQuery):
    advert_id = int(callback_query.data.replace('soft_delete ', ''))
    await postgres_db.soft_delete_advert(advert_id)

    await callback_query.answer(text=f'Ваше объявление удалено!', show_alert=False)
    await callback_query.message.delete()


async def show_my_adverts_handler(message: types.Message):
    tg_id = message.chat.id
    user_id = await postgres_db.get_user_id(tg_id)

    adverts = await postgres_db.get_my_adverts(user_id)

    if adverts:
        for advert in adverts:
            if advert[7]:
                await bot.send_message(message.chat.id, f'<b>Статус:</b> Опубликован\n\n#{advert[3].replace(" ", "_")}\n<b>{advert[1]}</b>\n\n<code>{advert[2]}</code>\n\n<b>Контакты:</b>\n<code>{advert[6]}</code>\n\n<b>Дедлайн:</b> <code>{advert[4]}</code>\n<b>Бюджет:</b> <code>{advert[5]}</code>', parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить объявление', callback_data=f'soft_delete {advert[0]}')))
            else:
                await bot.send_message(message.chat.id, f'<b>Статус:</b> На модерации\n\n#{advert[3].replace(" ", "_")}\n<b>{advert[1]}</b>\n\n<code>{advert[2]}</code>\n\n<b>Контакты:</b>\n<code>{advert[6]}</code>\n\n<b>Дедлайн:</b> <code>{advert[4]}</code>\n<b>Бюджет:</b> <code>{advert[5]}</code>',parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Удалить объявление', callback_data=f'soft_delete {advert[0]}')))
    else:
        await bot.send_message(message.chat.id, '<b>Ваш список заданий пуст.</b>\n\n<code>Что бы добавить нажмите на кнопку</code> <b>"Добавить задание"</b>', parse_mode='html')


# FSM
class FSMUser(StatesGroup):
    title = State()
    description = State()
    category = State()
    deadline = State()
    price = State()
    contacts = State()


async def load_advert_handler(message: types.Message):
    await FSMUser.title.set()

    await bot.send_message(message.chat.id, config.TITLE, parse_mode='html', reply_markup=cancel_kb)


async def cancel_advert_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        return

    await state.finish()

    if await postgres_db.get_user_status(message.from_user.id) == 0:
        await bot.send_message(message.chat.id, config.WELCOME, reply_markup=menu_kb)
    else:
        await bot.send_message(message.chat.id, config.WELCOME, reply_markup=menu_kb2)


async def load_title(message: types.Message, state:  FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await FSMUser.next()
    await bot.send_message(message.chat.id, config.DESCRIPTION, parse_mode='html', reply_markup=cancel_kb)


async def load_description(message: types.Message, state:  FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await FSMUser.next()
    await bot.send_message(message.chat.id, config.CATEGORY, parse_mode='html', reply_markup=categories_kb)


async def load_category(message: types.Message, state:  FSMContext):
    if message.text in await postgres_db.get_category_names():
        category_id = await postgres_db.get_category_id(message.text)
        async with state.proxy() as data:
            data['category_id'] = category_id

        await FSMUser.next()

        await bot.send_message(message.chat.id, config.DEADLINE, parse_mode='html', reply_markup=cancel_kb)
    else:
        await bot.send_message(message.chat.id, config.CATEGORY, parse_mode='html', reply_markup=categories_kb)



async def load_deadline(message: types.Message, state:  FSMContext):
    async with state.proxy() as data:
        data['deadline'] = message.text

    await FSMUser.next()
    await bot.send_message(message.chat.id, config.PRICE, parse_mode='html', reply_markup=cancel_kb)


async def load_price(message: types.Message, state:  FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await FSMUser.next()
    await bot.send_message(message.chat.id, config.CONTACTS, parse_mode='html', reply_markup=cancel_kb)


async def load_contacts(message: types.Message, state:  FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text

        # Add advert [GAVNO CODE]
        tg_id = message.chat.id
        user_id = await postgres_db.get_user_id(tg_id)
        data = list(data.values())

        await postgres_db.add_advert(data, user_id)

    await state.finish()

    if await postgres_db.get_user_status(message.from_user.id) == 0:
        await bot.send_message(message.chat.id, config.FINISH, parse_mode='html', reply_markup=menu_kb)
    else:
        await bot.send_message(message.chat.id, config.FINISH, parse_mode='html', reply_markup=menu_kb2)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(show_adverts_handler, Text(equals='Показать задания'))
    dp.register_message_handler(load_advert_handler, Text(equals='Добавить задание'))
    dp.register_message_handler(show_my_adverts_handler, Text(equals='Мои задания'))

    # callback query
    dp.register_callback_query_handler(soft_delete_advert_callback, lambda x: x.data and x.data.startswith('soft_delete '))

    # FSM
    dp.register_message_handler(cancel_advert_handler, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_title, state=FSMUser.title)
    dp.register_message_handler(load_description, state=FSMUser.description)
    dp.register_message_handler(load_category, state=FSMUser.category)
    dp.register_message_handler(load_deadline, state=FSMUser.deadline)
    dp.register_message_handler(load_price, state=FSMUser.price)
    dp.register_message_handler(load_contacts, state=FSMUser.contacts)
