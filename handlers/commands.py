from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.cr_api import cr_api
from utils.royaleapi import royale_api
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
        "/player &lt;тег&gt; - Статистика игрока\n"
        "/war - Информация о текущей войне\n"
        "/warstats &lt;тег&gt; - Статистика игрока в войне\n"
        "/remind [тег] - Подписаться на напоминания\n"
        "/unremind - Отписаться от напоминаний\n"
        "/remindnow [тег] - Напомнить сейчас\n"
        "/config - Проверить конфигурацию\n"
        "/help - Справка"
    )
    await message.answer(welcome_text, parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = (
        "📖 <b>Справка по командам:</b>\n\n"
        "<b>Основные команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/clan - Получить информацию о клане\n"
        "/members - Получить список участников клана\n"
        "/player &lt;тег&gt; - Получить статистику игрока\n"
        "   Пример: /player 2PP\n"
        "/config - Проверить конфигурацию бота\n\n"
        "<b>Клановая война:</b>\n"
        "/war - Информация о текущей войне\n"
        "/warstats &lt;тег&gt; - Статистика игрока в войне\n"
        "/remind [тег] - Подписаться на напоминания об атаках\n"
        "/unremind - Отписаться от напоминаний\n"
        "/remindnow [тег] - Получить напоминание прямо сейчас\n\n"
        "<b>Примечание:</b> Тег игрока можно указать с # или без него."
    )
    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("config"))
async def cmd_config(message: Message):
    """Обработчик команды /config - проверка конфигурации"""
    from config import CR_API_TOKEN, BOT_TOKEN
    
    config_text = "⚙️ <b>Конфигурация бота:</b>\n\n"
    
    # Проверка токена бота
    if BOT_TOKEN:
        bot_status = "✅ Установлен"
        bot_preview = BOT_TOKEN[:10] + "..." if len(BOT_TOKEN) > 10 else "***"
    else:
        bot_status = "❌ Не установлен"
        bot_preview = "не установлен"
    
    config_text += f"🤖 <b>BOT_TOKEN:</b> {bot_status}\n"
    config_text += f"   <code>{bot_preview}</code>\n\n"
    
    # Проверка API токена
    if CR_API_TOKEN:
        api_status = "✅ Установлен"
        api_preview = CR_API_TOKEN[:10] + "..." if len(CR_API_TOKEN) > 10 else "***"
    else:
        api_status = "❌ Не установлен"
        api_preview = "не установлен"
    
    config_text += f"🔑 <b>CR_API_TOKEN:</b> {api_status}\n"
    config_text += f"   <code>{api_preview}</code>\n\n"
    
    # Проверка тега клана
    if CLAN_TAG:
        clan_status = "✅ Установлен"
        clan_preview = f"#{CLAN_TAG.upper()}"
    else:
        clan_status = "❌ Не установлен"
        clan_preview = "не установлен"
    
    config_text += f"🏰 <b>CLAN_TAG:</b> {clan_status}\n"
    config_text += f"   <code>{clan_preview}</code>\n\n"
    
    if not CR_API_TOKEN or not CLAN_TAG:
        config_text += "⚠️ <b>Внимание:</b> Для работы бота необходимо установить все параметры в файле .env"
    
    await message.answer(config_text, parse_mode="HTML")


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
    from config import CR_API_TOKEN
    
    if not CLAN_TAG:
        await message.answer(
            "❌ Тег клана не настроен. Обратитесь к администратору бота.",
            parse_mode="HTML"
        )
        return
    
    if not CR_API_TOKEN:
        await message.answer(
            "❌ API токен не настроен. Обратитесь к администратору бота.",
            parse_mode="HTML"
        )
        return
    
    await message.answer("⏳ Загружаю список участников...")
    
    members = await cr_api.get_clan_members(CLAN_TAG)
    if members is not None and len(members) > 0:
        text = format_clan_members(members)
        await message.answer(text, parse_mode="HTML")
    else:
        error_msg = (
            "❌ Не удалось получить список участников.\n\n"
            "<b>Возможные причины:</b>\n"
            "• Неверный тег клана (текущий: <code>#{}</code>)\n"
            "• Неверный или отсутствующий API токен\n"
            "• Превышен лимит запросов к API\n"
            "• Проблемы с сетью\n\n"
            "Проверьте логи бота для детальной информации."
        ).format(CLAN_TAG.upper() if CLAN_TAG else "не установлен")
        await message.answer(error_msg, parse_mode="HTML")


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
    
    # Пробуем получить данные из официального API
    player_data = await cr_api.get_player_info(player_tag)
    
    # Если не получилось, пробуем RoyaleAPI
    if not player_data:
        player_data = await royale_api.get_player_stats(player_tag)
    
    if player_data:
        text = format_player_stats(player_data)
        await message.answer(text, parse_mode="HTML")
    else:
        await message.answer(
            "❌ Не удалось получить информацию об игроке. Проверьте правильность тега игрока.",
            parse_mode="HTML"
        )

