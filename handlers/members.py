from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, LEFT, MEMBER, ADMINISTRATOR, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import db
import logging

logger = logging.getLogger(__name__)

router = Router()


class RoyaleNicknameState(StatesGroup):
    waiting_for_nickname = State()
    waiting_for_tag = State()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> (MEMBER | ADMINISTRATOR)))
@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED >> (MEMBER | ADMINISTRATOR)))
async def on_new_member(event: ChatMemberUpdated):
    """Обработчик новых участников"""
    user = event.new_chat_member.user
    
    # Проверяем, что это действительно новый участник (не бот)
    if user.is_bot:
        return
    
    # Добавляем пользователя в базу данных
    db.add_user(user.id, user.username)
    
    welcome_text = (
        f"👋 <b>Добро пожаловать, {user.first_name}!</b>\n\n"
        "Для полноценной работы бота, пожалуйста, укажите ваш ник в Clash Royale.\n\n"
        "Отправьте команду /setnick чтобы указать ваш ник и тег игрока."
    )
    
    try:
        await event.bot.send_message(
            chat_id=event.chat.id,
            text=welcome_text,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке приветствия: {e}")


@router.message(lambda m: m.new_chat_members)
async def on_new_members_group(message: Message):
    """Обработчик новых участников в группе"""
    for user in message.new_chat_members:
        if user.is_bot:
            continue
        
        # Добавляем пользователя в базу данных
        db.add_user(user.id, user.username)
        
        welcome_text = (
            f"👋 <b>Добро пожаловать, {user.first_name}!</b>\n\n"
            "Для полноценной работы бота, пожалуйста, укажите ваш ник в Clash Royale.\n\n"
            "Отправьте команду /setnick чтобы указать ваш ник и тег игрока."
        )
        
        try:
            await message.answer(welcome_text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Ошибка при отправке приветствия: {e}")


@router.message(Command("setnick"))
async def cmd_setnick(message: Message, state: FSMContext):
    """Команда для установки ника в рояле"""
    await message.answer(
        "📝 Пожалуйста, отправьте ваш <b>ник в Clash Royale</b> (только имя, без тега):",
        parse_mode="HTML"
    )
    await state.set_state(RoyaleNicknameState.waiting_for_nickname)


@router.message(RoyaleNicknameState.waiting_for_nickname)
async def process_nickname(message: Message, state: FSMContext):
    """Обработка ника"""
    nickname = message.text.strip()
    
    if len(nickname) < 2:
        await message.answer("❌ Ник слишком короткий. Попробуйте еще раз.")
        return
    
    await state.update_data(nickname=nickname)
    await message.answer(
        "🏷️ Теперь отправьте ваш <b>тег игрока</b> (например: 2PP или #2PP):",
        parse_mode="HTML"
    )
    await state.set_state(RoyaleNicknameState.waiting_for_tag)


@router.message(RoyaleNicknameState.waiting_for_tag)
async def process_tag(message: Message, state: FSMContext):
    """Обработка тега"""
    tag = message.text.strip().replace("#", "").upper()
    
    if len(tag) < 3:
        await message.answer("❌ Тег слишком короткий. Попробуйте еще раз.")
        return
    
    data = await state.get_data()
    nickname = data.get("nickname")
    
    # Обновляем информацию в базе данных
    db.update_user_royale_info(message.from_user.id, nickname, tag)
    
    await message.answer(
        f"✅ Отлично! Ваш ник сохранен:\n"
        f"👤 <b>{nickname}</b> #{tag}\n\n"
        f"Теперь вы можете использовать все функции бота!",
        parse_mode="HTML"
    )
    await state.clear()

