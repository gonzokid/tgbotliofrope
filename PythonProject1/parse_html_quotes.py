import re
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# 1. Установите библиотеку если нет
# pip install beautifulsoup4

# Ваш Telegram ID (напишите @userinfobot чтобы узнать)
YOUR_USER_ID = "6756790622"  # ЗАМЕНИТЕ НА ВАШ ID

# Читаем HTML файл
with open('messages.html', 'r', encoding='utf-8') as file:  # или messages.html, как у вас называется
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Находим все сообщения
messages = []

# В экспортированном HTML сообщения обычно в div с классом 'message'
for msg_div in soup.find_all('div', class_='message'):
    # Текст сообщения
    text_div = msg_div.find('div', class_='text')
    if not text_div:
        continue

    text = text_div.get_text().strip()

    # Пропускаем пустые или служебные сообщения
    if not text or text.startswith('/'):
        continue

    # Дата сообщения
    date_div = msg_div.find('div', class_='date')
    date_str = "2024-01-01"  # default
    if date_div:
        date_text = date_div.get_text().strip()
        # Парсим дату, например "15.03.2024"
        match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', date_text)
        if match:
            day, month, year = match.groups()
            date_str = f"{year}-{month}-{day}"

    messages.append({
        'text': text,
        'date': date_str
    })

print(f"Найдено {len(messages)} сообщений")

# Загружаем текущую базу цитат бота
quotes_file = "quotes.json"
if os.path.exists(quotes_file):
    with open(quotes_file, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
else:
    quotes_data = {}

# Добавляем цитаты в базу
if YOUR_USER_ID not in quotes_data:
    quotes_data[YOUR_USER_ID] = {
        "user_id": int(YOUR_USER_ID),
        "quotes": {},
        "next_id": 1
    }

user_quotes = quotes_data[YOUR_USER_ID]
next_id = user_quotes["next_id"]

added = 0
for msg in messages:
    # Проверяем на дубликаты (по тексту)
    is_duplicate = False
    for q in user_quotes["quotes"].values():
        if q["text"] == msg["text"][:100]:  # сравниваем начало текста
            is_duplicate = True
            break

    if not is_duplicate:
        user_quotes["quotes"][str(next_id)] = {
            "id": next_id,
            "text": msg["text"],
            "author": "",  # можно распарсить если есть автор через тире
            "date_added": msg["date"],
            "tags": []
        }
        next_id += 1
        added += 1

user_quotes["next_id"] = next_id

# Сохраняем
with open(quotes_file, 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=2)

print(f"✅ Добавлено {added} новых цитат")
print(f"📊 Всего цитат: {len(user_quotes['quotes'])}")