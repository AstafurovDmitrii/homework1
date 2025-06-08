import aiohttp
import asyncio
import aiosqlite
from typing import List, Dict, Any
import time

# Настройки
DB_NAME = "data/starwars_characters.db"
BASE_URL = "https://swapi.dev/api/people/"
BATCH_SIZE = 5  # Количество одновременных запросов
MAX_RETRIES = 3  # Максимальное количество попыток
RETRY_DELAY = 1  # Задержка между попытками

async def get_character_data(session: aiohttp.ClientSession, char_id: int) -> Dict[str, Any]:
    url = f"{BASE_URL}{char_id}/"
    
    # Пытаемся получить данные с повторами при ошибках
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    data['id'] = char_id  # Добавляем ID в данные
                    return data
                elif response.status == 404:
                    return None
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            await asyncio.sleep(RETRY_DELAY * (attempt + 1))
    
    return None

async def get_related_names(session: aiohttp.ClientSession, urls: List[str]) -> str:
    if not urls:
        return ""
    
    # Получаем все связанные объекты параллельно
    tasks = [session.get(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    
    names = []
    for resp in responses:
        if resp.status == 200:
            data = await resp.json()
            names.append(data.get('name') or data.get('title', ''))
    
    return ", ".join(names)

async def process_character(session: aiohttp.ClientSession, db: aiosqlite.Connection, char_id: int):
    # Получаем данные персонажа
    char_data = await get_character_data(session, char_id)
    if not char_data:
        return
    
    # Параллельно получаем названия связанных сущностей
    tasks = {
        'homeworld': get_related_names(session, [char_data['homeworld']]) if char_data['homeworld'] else "",
        'films': get_related_names(session, char_data['films']),
        'species': get_related_names(session, char_data['species']),
        'starships': get_related_names(session, char_data['starships']),
        'vehicles': get_related_names(session, char_data['vehicles']),
    }
    
    # Ждем завершения всех задач
    results = await asyncio.gather(*tasks.values())
    results_dict = dict(zip(tasks.keys(), results))
    
    # Подготавливаем данные для сохранения
    character = {
        'id': char_data['id'],
        'name': char_data['name'],
        'birth_year': char_data['birth_year'],
        'eye_color': char_data['eye_color'],
        'films': results_dict['films'],
        'gender': char_data['gender'],
        'hair_color': char_data['hair_color'],
        'height': char_data['height'],
        'homeworld': results_dict['homeworld'],
        'mass': char_data['mass'],
        'skin_color': char_data['skin_color'],
        'species': results_dict['species'],
        'starships': results_dict['starships'],
        'vehicles': results_dict['vehicles'],
        'created': char_data['created'],
        'edited': char_data['edited']
    }
    
    # Сохраняем в базу данных
    query = """
    INSERT OR REPLACE INTO characters VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """
    await db.execute(query, tuple(character.values()))
    await db.commit()
    
    print(f"Обработан персонаж {char_id}: {char_data['name']}")

async def find_max_character_id(session: aiohttp.ClientSession) -> int:
    # SWAPI не предоставляет количество персонажей, поэтому находим максимальный ID
    low, high = 1, 1
    
    # Сначала находим верхнюю границу
    while True:
        try:
            async with session.get(f"{BASE_URL}{high}/") as resp:
                if resp.status == 200:
                    high *= 2
                else:
                    break
        except:
            break
    
    # Затем бинарный поиск для точного определения
    last_valid = 0
    while low <= high:
        mid = (low + high) // 2
        try:
            async with session.get(f"{BASE_URL}{mid}/") as resp:
                if resp.status == 200:
                    last_valid = mid
                    low = mid + 1
                else:
                    high = mid - 1
        except:
            high = mid - 1
    
    return last_valid

async def main():
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Определяем максимальный ID персонажа
        max_id = await find_max_character_id(session)
        print(f"Найден максимальный ID персонажа: {max_id}")
        
        # Подключаемся к базе данных
        async with aiosqlite.connect(DB_NAME) as db:
            # Создаем задачи для всех персонажей
            tasks = []
            for char_id in range(1, max_id + 1):
                tasks.append(process_character(session, db, char_id))
                
                # Ограничиваем количество одновременных задач
                if len(tasks) >= BATCH_SIZE:
                    await asyncio.gather(*tasks)
                    tasks = []
            
            # Обрабатываем оставшиеся задачи
            if tasks:
                await asyncio.gather(*tasks)
    
    print(f"Завершено за {time.time() - start_time:.2f} секунд")

if __name__ == "__main__":
    asyncio.run(main())