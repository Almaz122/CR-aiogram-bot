import aiohttp
from typing import Optional, Dict, List
from config import CR_API_TOKEN, CR_API_BASE_URL


class ClashRoyaleAPI:
    """Класс для работы с Clash Royale API"""
    
    def __init__(self):
        self.base_url = CR_API_BASE_URL
        if not CR_API_TOKEN:
            print("⚠️ ВНИМАНИЕ: CR_API_TOKEN не установлен! API запросы не будут работать.")
        self.headers = {
            "Authorization": f"Bearer {CR_API_TOKEN}",
            "Accept": "application/json"
        }
    
    async def get_clan_info(self, clan_tag: str) -> Optional[Dict]:
        """Получить информацию о клане"""
        try:
            clean_tag = clan_tag.replace('#', '').upper()
            url = f"{self.base_url}/clans/%23{clean_tag}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"Ошибка API при получении информации о клане: статус {response.status}")
                        print(f"URL: {url}")
                        print(f"Ответ: {error_text[:200]}")
                        return None
        except aiohttp.ClientError as e:
            print(f"Ошибка сети при получении информации о клане: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при получении информации о клане: {e}")
            return None
    
    async def get_clan_members(self, clan_tag: str) -> Optional[List[Dict]]:
        """Получить список участников клана"""
        try:
            clean_tag = clan_tag.replace('#', '').upper()
            url = f"{self.base_url}/clans/%23{clean_tag}/members"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("items", [])
                    else:
                        error_text = await response.text()
                        print(f"Ошибка API при получении участников клана: статус {response.status}")
                        print(f"URL: {url}")
                        print(f"Ответ: {error_text[:200]}")
                        if response.status == 403:
                            print("Ошибка 403: Проверьте API токен и его права доступа")
                        elif response.status == 404:
                            print(f"Ошибка 404: Клан с тегом #{clean_tag} не найден")
                        elif response.status == 429:
                            print("Ошибка 429: Превышен лимит запросов к API")
                        return None
        except aiohttp.ClientError as e:
            print(f"Ошибка сети при получении участников клана: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка при получении участников клана: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def get_player_info(self, player_tag: str) -> Optional[Dict]:
        """Получить информацию об игроке"""
        try:
            url = f"{self.base_url}/players/%23{player_tag.replace('#', '')}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            print(f"Ошибка при получении информации об игроке: {e}")
            return None
    
    async def get_clan_war(self, clan_tag: str) -> Optional[Dict]:
        """Получить информацию о текущей клановой войне"""
        try:
            url = f"{self.base_url}/clans/%23{clan_tag.replace('#', '')}/currentwar"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            print(f"Ошибка при получении информации о войне: {e}")
            return None
    
    async def get_player_battle_log(self, player_tag: str) -> Optional[List[Dict]]:
        """Получить историю битв игрока"""
        try:
            url = f"{self.base_url}/players/%23{player_tag.replace('#', '')}/battlelog"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data if isinstance(data, list) else []
                    return None
        except Exception as e:
            print(f"Ошибка при получении истории битв: {e}")
            return None


cr_api = ClashRoyaleAPI()

