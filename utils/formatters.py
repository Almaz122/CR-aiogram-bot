from typing import List, Dict


def format_clan_info(clan_data: Dict) -> str:
    """Форматирование информации о клане"""
    if not clan_data:
        return "❌ Не удалось получить информацию о клане"
    
    name = clan_data.get("name", "N/A")
    tag = clan_data.get("tag", "N/A")
    description = clan_data.get("description", "Нет описания")
    members = clan_data.get("members", 0)
    score = clan_data.get("clanScore", 0)
    donations = clan_data.get("donationsPerWeek", 0)
    location = clan_data.get("location", {}).get("name", "Не указано")
    type_clan = clan_data.get("type", "open")
    required_trophies = clan_data.get("requiredTrophies", 0)
    
    text = f"🏰 <b>{name}</b> {tag}\n\n"
    text += f"📝 <b>Описание:</b> {description}\n"
    text += f"👥 <b>Участников:</b> {members}/50\n"
    text += f"🏆 <b>Очки клана:</b> {score:,}\n"
    text += f"🎁 <b>Пожертвований в неделю:</b> {donations:,}\n"
    text += f"📍 <b>Локация:</b> {location}\n"
    text += f"🔓 <b>Тип:</b> {type_clan}\n"
    text += f"⚡ <b>Минимум трофеев:</b> {required_trophies:,}"
    
    return text


def format_player_stats(player_data: Dict) -> str:
    """Форматирование статистики игрока"""
    if not player_data:
        return "❌ Не удалось получить информацию об игроке"
    
    name = player_data.get("name", "N/A")
    tag = player_data.get("tag", "N/A")
    exp_level = player_data.get("expLevel", 0)
    trophies = player_data.get("trophies", 0)
    best_trophies = player_data.get("bestTrophies", 0)
    wins = player_data.get("wins", 0)
    losses = player_data.get("losses", 0)
    draws = player_data.get("draws", 0)
    total_battles = wins + losses + draws
    win_rate = (wins / total_battles * 100) if total_battles > 0 else 0
    
    # Трехкоронные победы
    three_crown_wins = player_data.get("threeCrownWins", 0)
    
    # Карты
    cards = player_data.get("cards", [])
    cards_found = len([c for c in cards if c.get("maxLevel", 0) > 0])
    
    # Донаты
    total_donations = player_data.get("totalDonations", 0)
    
    # Войны
    war_day_wins = player_data.get("warDayWins", 0)
    clan_cards_collected = player_data.get("clanCardsCollected", 0)
    
    text = f"👤 <b>{name}</b> {tag}\n\n"
    text += f"⭐ <b>Уровень:</b> {exp_level}\n"
    text += f"🏆 <b>Трофеи:</b> {trophies:,} (лучший: {best_trophies:,})\n\n"
    text += f"⚔️ <b>Битвы:</b>\n"
    text += f"   Побед: {wins:,}\n"
    text += f"   Поражений: {losses:,}\n"
    text += f"   Ничьих: {draws:,}\n"
    text += f"   Всего: {total_battles:,}\n"
    text += f"   Винрейт: {win_rate:.1f}%\n"
    text += f"   Трехкоронных побед: {three_crown_wins:,}\n\n"
    text += f"🃏 <b>Карты:</b> {cards_found}/{len(cards)}\n"
    text += f"🎁 <b>Всего пожертвовано:</b> {total_donations:,}\n"
    text += f"⚔️ <b>Побед в войнах:</b> {war_day_wins}\n"
    text += f"📦 <b>Карт собрано в войнах:</b> {clan_cards_collected:,}"
    
    return text


def format_clan_members(members: List[Dict]) -> str:
    """Форматирование списка участников клана"""
    if not members:
        return "❌ Не удалось получить список участников"
    
    text = f"👥 <b>Участники клана ({len(members)}):</b>\n\n"
    
    # Сортируем по трофеям (по убыванию)
    sorted_members = sorted(members, key=lambda x: x.get("trophies", 0), reverse=True)
    
    for i, member in enumerate(sorted_members[:20], 1):  # Показываем топ-20
        name = member.get("name", "N/A")
        role = member.get("role", "member")
        trophies = member.get("trophies", 0)
        donations = member.get("donations", 0)
        donations_received = member.get("donationsReceived", 0)
        
        role_emoji = {
            "leader": "👑",
            "coLeader": "⭐",
            "elder": "🌟",
            "member": "👤"
        }.get(role, "👤")
        
        text += f"{i}. {role_emoji} <b>{name}</b>\n"
        text += f"   🏆 {trophies:,} | 🎁 {donations}/{donations_received}\n"
    
    if len(members) > 20:
        text += f"\n... и еще {len(members) - 20} участников"
    
    return text

