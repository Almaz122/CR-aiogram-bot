from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.cr_api import cr_api
from utils.formatters import format_clan_info, format_player_stats, format_clan_members
from config import CLAN_TAG

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = (
        "👋 <b>Добро пожаловать в Clash Royale Clan Bot!</b>\n\n"
        "Я помогу вам отслеживать статистику вашего клана и игроков.\n\n"
        "<b>Доступные команды:</b>\n"
        "/clan - Информация о клане\n"
        "/members - Список участников клана\n"
        "/player <тег> - Статистика игрока\n"
        "/help - Справка"
    )
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📖 <b>Справка по командам:</b>\n\n"
        "/start - Начать работу с ботом\n"
        "/clan - Получить информацию о клане\n"
        "/members - Получить список участников клана\n"
        "/player <тег> - Получить статистику игрока\n"
        "   Пример: /player 2PP\n\n"
        "<b>Примечание:</b> Тег игрока можно указать с # или без него."
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("clan"))
async def cmd_clan(message: Message):
    """Обработчик команды /clan"""
    if not CLAN_TAG:
        await message.answer(
            "❌ Тег клана не настроен. Обратитесь к администратору бота.",
            parse_mode="HTML"
        )
        return
    
    await message.answer("⏳ Загружаю информацию о клане...")
    
    clan_data = await cr_api.get_clan_info(CLAN_TAG)
    if clan_data:
        text = format_clan_info(clan_data)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ Не удалось получить информацию о клане. Проверьте правильность тега клана и API токена.",
            parse_mode="HTML"
        )


@router.message(Command("members"))
async def cmd_members(message: Message):
    """Обработчик команды /members"""
    if not CLAN_TAG:
        await message.answer(
            "❌ Тег клана не настроен. Обратитесь к администратору бота.",
            parse_mode="HTML"
        )
        return
    
    await message.answer("⏳ Загружаю список участников...")
    
    members = await cr_api.get_clan_members(CLAN_TAG)
    if members:
        text = format_clan_members(members)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ Не удалось получить список участников. Проверьте правильность тега клана и API токена.",
            parse_mode="HTML"
        )


@router.message(Command("player"))
async def cmd_player(message: Message, state: FSMContext):
    """Обработчик команды /player"""
    # Получаем тег игрока из команды
    command_parts = message.text.split()
    
    if len(command_parts) < 2:
        await message.answer(
            "❌ Укажите тег игрока.\n"
            "Пример: /player 2PP или /player #2PP",
            parse_mode="HTML"
        )
        return
    
    player_tag = command_parts[1].replace("#", "")
    
    await message.answer("⏳ Загружаю статистику игрока...")
    
    player_data = await cr_api.get_player_info(player_tag)
    if player_data:
        text = format_player_stats(player_data)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ Не удалось получить информацию об игроке. Проверьте правильность тега игрока.",
            parse_mode="HTML"
        )

