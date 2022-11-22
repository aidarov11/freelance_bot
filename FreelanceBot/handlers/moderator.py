import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from create_bot import dp, bot

# Keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import menu_kb, menu_kb2, moderator_kb, cancel_mailing_kb, cancel_add_moderator_kb
# FSM
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# DB
from database import postgres_db

"""
    Сделать уведомления об публикаций поста 
    Записывать текст и ид пользователья кто сделал рассылку
"""

async def start_moderator_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        await bot.send_message(message.chat.id, 'Режим Модератора включен', reply_markup=moderator_kb)


async def show_active_adverts_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        adverts = await postgres_db.get_activ_adverts()

        if adverts:
            for advert in adverts:
                await bot.send_message(message.chat.id, f'#{advert[3].replace(" ", "_")}\n<b>{advert[1]}</b>\n\n<code>{advert[2]}</code>\n\n<b>Контакты:</b>\n<code>{advert[6]}</code>\n\n<b>Дедлайн:</b> <code>{advert[4]}</code>\n<b>Бюджет:</b> <code>{advert[5]}</code>', parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Отключить', callback_data=f'soft_delete {advert[0]}')))
        else:
            await bot.send_message(message.chat.id, 'Список активных заданий пуст.', parse_mode='html')


async def verify_adverts_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        adverts = await postgres_db.get_unverified_adverts()

        if adverts:
            for advert in adverts:
                await bot.send_message(message.chat.id, f'#{advert[3].replace(" ", "_")}\n<b>{advert[1]}</b>\n\n<code>{advert[2]}</code>\n\n<b>Контакты:</b>\n<code>{advert[6]}</code>\n\n<b>Дедлайн:</b> <code>{advert[4]}</code>\n<b>Бюджет:</b> <code>{advert[5]}</code>', parse_mode='html', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Проверено', callback_data=f'verified {advert[0]}, {advert[7]}')).add(InlineKeyboardButton('Удалить', callback_data=f'delete {advert[0]}, {advert[7]}')))
        else:
            await bot.send_message(message.chat.id, 'Список заданий ожидающие проверки пуст.', parse_mode='html')


# FSM
class FSMMailing(StatesGroup):
    mailing_text = State()


async def mailing_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 1:
        await FSMMailing.mailing_text.set()

        await bot.send_message(message.chat.id, '<b>Введите текст рассылки:</b>', parse_mode='html', reply_markup=cancel_mailing_kb)
    else:
        await bot.send_message(message.chat.id, 'Эта функция вам недоступна.')


async def cancel_mailing_handler(message: types.Message, state: FSMContext):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        current_state = await state.get_state()

        if current_state is None:
            return

        await state.finish()

        await bot.send_message(message.chat.id, 'Рассылка отменена.', parse_mode='html', reply_markup=moderator_kb)


# Нужно добавить рассылку с фото
async def load_mailing_text(message: types.Message, state: FSMContext):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        users_id = await postgres_db.get_telegram_users_id()

        for user_id in users_id:
            # Обход ошибки (Forbidden: bot was blocked by the user)
            try:
                await bot.send_message(user_id, message.text, parse_mode="html")
            except BotBlocked:
                await asyncio.sleep(1)

        await state.finish()

        await bot.send_message(message.chat.id, 'Рассылка успешно выполнено.', parse_mode='html', reply_markup=moderator_kb)


async def list_of_moderators_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        moderators = await postgres_db.get_list_of_moderators()

        if moderators:
            for moderator in moderators:
                if user_status == 2:
                    await bot.send_message(message.chat.id, f'Имя: {moderator[1]}\nФамилия: {moderator[2]}\nИмя пользователя: @{moderator[3]}', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Отобрать привилегию', callback_data=f'take_away {moderator[0]}')))
                elif user_status == 1:
                    await bot.send_message(message.chat.id, f'Имя: {moderator[1]}\nФамилия: {moderator[2]}\nИмя пользователя: @{moderator[3]}')
        else:
            await bot.send_message(message.chat.id, 'Список модераторов пуст.')


# FSM Add new moderator
class FSMAddModerator(StatesGroup):
    username = State()


async def add_moderator_command(message: types.Message):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 1:
        await FSMAddModerator.username.set()

        await bot.send_message(message.chat.id, '<b>Введите имя пользователя:</b>', parse_mode='html', reply_markup=cancel_add_moderator_kb)
    else:
        await bot.send_message(message.chat.id, 'Эта функция вам недоступна.')


async def cancel_add_moderator_handler(message: types.Message, state: FSMContext):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        current_state = await state.get_state()

        if current_state is None:
            return

        await state.finish()

        await bot.send_message(message.chat.id, 'Добавление модератора отменена.', parse_mode='html', reply_markup=moderator_kb)


async def load_username(message: types.Message, state: FSMContext):
    user_status = await postgres_db.get_user_status(message.chat.id)

    if user_status > 0:
        username = message.text.replace('@', '')

        try:
            await postgres_db.set_moderator_status(username)
        except:
            await state.finish()
            await bot.send_message(message.chat.id, f'Не удалось добавить нового модератора ({message.text})', parse_mode='html', reply_markup=moderator_kb)
        else:
            await state.finish()
            await bot.send_message(message.chat.id, 'Новый модератор успешно добавлен.', parse_mode='html', reply_markup=moderator_kb)


async def exit_command(message: types.Message):
    if await postgres_db.get_user_status(message.from_user.id) == 0:
        await bot.send_message(message.chat.id, 'Режим Модератора выключен.', reply_markup=menu_kb)
    else:
        await bot.send_message(message.chat.id, 'Режим Модератора выключен.', reply_markup=menu_kb2)


async def verify_advert_callback(callback_query: types.CallbackQuery):
    advert_id, tg_id = callback_query.data.replace('verified ', '').split(', ')

    await postgres_db.set_verified(int(advert_id))

    await bot.send_message(int(tg_id), '<b>Ваше объявление успешно опубликовано.</b>', parse_mode='html')

    await callback_query.answer(text='Объявление проверено', show_alert=False)
    await callback_query.message.delete()


async def delete_advert_callback(callback_query: types.CallbackQuery):
    advert_id, tg_id = callback_query.data.replace('delete ', '').split(', ')

    await bot.send_message(int(tg_id), '<b>Dаше объявление не прошло модерацию и было удалено.</b>', parse_mode='html')

    await  postgres_db.delete_advert(advert_id)

    await callback_query.answer(text='Объявление удалено', show_alert=False)
    await callback_query.message.delete()


async def take_away_privilege_callback(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.replace('take_away ', ''))

    await postgres_db.set_user_status(user_id)

    await callback_query.answer(text='Статус пользователя изменен.', show_alert=False)
    await callback_query.message.delete()


def register_handlers_moderator(dp: Dispatcher):
    dp.register_message_handler(start_moderator_command, Text(equals='Режим Модератора'))
    dp.register_message_handler(show_active_adverts_command, Text(equals='Активные задания'))
    dp.register_message_handler(verify_adverts_command, Text(equals='Ожидают проверки'))
    dp.register_message_handler(mailing_command, Text(equals='Сделать рассылку'))
    dp.register_message_handler(list_of_moderators_command, Text(equals='Список модераторов'))
    dp.register_message_handler(add_moderator_command, Text(equals='Добавить модератора'))

    dp.register_message_handler(exit_command, Text(equals='Выйти'))

    # callback
    dp.register_callback_query_handler(verify_advert_callback, lambda x: x.data and x.data.startswith('verified '))
    dp.register_callback_query_handler(delete_advert_callback, lambda x: x.data and x.data.startswith('delete '))
    dp.register_callback_query_handler(take_away_privilege_callback, lambda x: x.data and x.data.startswith('take_away '))

    # FSM
    dp.register_message_handler(cancel_mailing_handler, Text(equals='Отменить рассылку', ignore_case=True), state='*')
    dp.register_message_handler(load_mailing_text, state=FSMMailing.mailing_text)

    dp.register_message_handler(cancel_add_moderator_handler, Text(equals='Отменить добавление модератора', ignore_case=True), state='*')
    dp.register_message_handler(load_username, state=FSMAddModerator.username)
