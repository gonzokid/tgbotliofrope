import random
import time
from datetime import datetime, date, timedelta
from datetime import time as dt_time
import os
import math
import json
from dataclasses import dataclass, field
from typing import Dict, Set, Optional, List, Tuple, Any
from enum import Enum
import asyncio
from collections import defaultdict

from telegram import (
    Update, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, BotCommand
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    JobQueue
)

BOT_TOKEN = "7920018238:AAGOzWWohK7p7w2v7ZX9eQta0fkrcPJFhAU"

# ============ ИНФОРМАЦИЯ О БОТЕ (ПОКАЗЫВАЕТСЯ ДО /start) ============

BOT_SHORT_DESCRIPTION = """
🦍 ГОНЗО БОТ - твой личный помощник для ЕГЭ, задач, рутины и творчества!
"""

BOT_DESCRIPTION = """
🦍 ГОНЗО БОТ v4.5 - многофункциональный помощник

📚 ЕГЭ (15 предметов)
🧮 Математика PRO
🔄 Рутина (привычки, трекинг, плавные переходы)
🔮 Гороскоп и Мемы
📋 Задачи с дедлайнами
📦 Буфер (пароли, дни рождения)
🔢 Нумерология (арканы, совместимость)
📚 Творчество (музыка, книги, стихи, картины)
📖 Цитатник
🗒️ Заметки
🎙️ Голос
⏰ Уведомления (настраиваемые напоминания)

💰 Премиум: 100⭐/мес (базовый) или 250⭐/мес (все включено)
🎟️ Есть промокоды от администратора

Нажми /start чтобы начать!
"""

BOT_INFO = """
╔══════════════════════════════════╗
║        🦍 ГОНЗО БОТ v4.5        ║
╚══════════════════════════════════╝

✨ ЧТО Я УМЕЮ:

📚 ЕГЭ (15 предметов!)
  • Информатика, Математика, Русский язык
  • Физика, Химия, Биология, История
  • Обществознание, Литература, География
  • Английский, Немецкий, Французский
  • Испанский, Китайский
  • Отслеживание прогресса по заданиям
  • Расчет необходимых заданий в день
  • Установка дат экзаменов

🧮 Математика PRO
  • Базовые: корни, логарифмы, степени
  • Продвинутые: факториалы, проценты
  • НОД/НОК, среднее арифметическое
  • Тригонометрия (sin, cos, tg)
  • Комбинаторика (перестановки, сочетания)
  • Решение уравнений
  • Перевод между системами счисления

🔄 РУТИНА
  • Отслеживание привычек (курение, чистка зубов, купание)
  • Плавные переходы между целями
  • Автоматический расчет нормы на каждый день
  • Отметки выполнения (✅ / ❌)
  • Корректировка плана при срывах
  • Финансовые цели с учетом дохода
  • Персональные рекомендации в разделе "Дата"

🔢 НУМЕРОЛОГИЯ
  • Расчет 22 арканов по дате рождения
  • Личный аркан, аркан года, аркан дня
  • Совместимость с другими людьми
  • Синхронизация с днями рождения из Буфера
  • Сохранение истории просмотров
  • Список людей с их арканами

🔮 Гороскоп и Мемы
  • Ежедневный гороскоп на любой знак
  • Случайные мемы для поднятия настроения

📋 Задачи
  • Создание задач с приоритетами
  • Установка дедлайнов
  • Авто-пометка просроченных
  • Статистика выполнения

📦 Буфер
  • Хранение личной информации
  • Менеджер паролей
  • Дни рождения с напоминаниями
  • Автоматическая синхронизация с нумерологией

📚 ТВОРЧЕСТВО
  • Музыкальные альбомы с треками, текстами, концептами и обложками
  • Библиотека книг с жанрами, рейтингом и заметками
  • Коллекция стихов с возможностью поиска по автору
  • Галерея картин с описанием и техникой исполнения

📖 Цитатник
  • Коллекция любимых цитат
  • Случайная цитата дня
  • Удобный просмотр по страницам

🗒️ Заметки
  • Быстрые текстовые заметки

🎙️ Голос
  • Преобразование голоса в текст

⏰ УВЕДОМЛЕНИЯ
  • Настройка времени и дней недели
  • Выбор контента: задачи, рутина, ЕГЭ
  • Гибкие настройки для каждого типа
  • Возможность отключения

⚙️ Настройки
  • Персонализация главного меню
  • Настройка уведомлений

💰 ОПЛАТА (Telegram Stars):
  • Базовый (100⭐/мес): голос, дата, базовая математика
  • Все включено (250⭐/мес): абсолютно все функции
  • Настраиваемый: плати только за нужные опции

🎟️ ПРОМОКОДЫ:
  • Есть скрытые промокоды от администратора
  • Вводи в разделе "💳 Купить подписку"

🚀 Используй /start для начала работы!
"""

# ============ ПРОМОКОДЫ (СКРЫТЫЕ) ============

PROMOCODES = {
    "GONZO50": {
        "discount": 50,
        "type": "percent",
        "uses": 100,
        "used": 0,
        "description": "50% скидка"
    },
    "GONZO70": {
        "discount": 70,
        "type": "percent",
        "uses": 50,
        "used": 0,
        "description": "70% скидка"
    },
    "GONZOFREE": {
        "discount": 100,
        "type": "percent",
        "uses": 10,
        "used": 0,
        "description": "Бесплатный доступ"
    }
}

PROMO_USAGE_FILE = "promo_usage.json"


def load_promo_usage():
    if os.path.exists(PROMO_USAGE_FILE):
        try:
            with open(PROMO_USAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for code in PROMOCODES:
                    if code in data:
                        PROMOCODES[code]["used"] = data[code].get("used", 0)
        except:
            pass


def save_promo_usage():
    data = {code: {"used": info["used"]} for code, info in PROMOCODES.items()}
    try:
        with open(PROMO_USAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass


def validate_promo(code: str) -> Optional[dict]:
    code = code.upper().strip()
    if code in PROMOCODES:
        promo = PROMOCODES[code]
        if promo["used"] < promo["uses"]:
            return promo
    return None


def use_promo(code: str):
    code = code.upper().strip()
    if code in PROMOCODES:
        PROMOCODES[code]["used"] += 1
        save_promo_usage()


# ============ СОСТОЯНИЯ ============
(
    MAIN_MENU, ROUTINE_CIGARETTE_SELECT,
    MATH_MENU, MATH_SQRT, MATH_LOG, MATH_BIN, MATH_POW,
    MATH_FACTORIAL, MATH_PERCENT, MATH_AVG, MATH_GCD_LCM,
    MATH_TRIG, MATH_COMB, MATH_EQ, MATH_CONVERT,
    EGE_SUBJECTS, EGE_SUBJECT_VIEW, EGE_CHEATSHEET_INPUT, EGE_TASK_MENU,
    TASKS_MENU, TASK_ADD_NAME, TASK_ADD_PRIORITY, TASK_ADD_DEADLINE, TASK_MANAGE_SELECT, TASK_MANAGE_ACTION,
    BUFFER_MENU, BUFFER_PERSONAL, BUFFER_PERSONAL_ADD,
    BUFFER_PASSWORDS, BUFFER_PASSWORDS_ADD,
    BUFFER_BIRTHDAYS, BUFFER_BIRTHDAYS_ADD,
    CREATIVITY_MENU,
    CR_MUSIC_MENU, CR_MUSIC_LIST, CR_MUSIC_ALBUM_ADD, CR_MUSIC_ALBUM_VIEW,
    CR_MUSIC_TRACK_ADD, CR_MUSIC_TRACK_VIEW, CR_MUSIC_TRACK_EDIT,
    CR_MUSIC_CONCEPT_INPUT, CR_MUSIC_COVER_INPUT, CR_MUSIC_LYRICS_INPUT,
    CR_MUSIC_ALBUM_DELETE, CR_MUSIC_TRACK_DELETE, CR_MUSIC_SEARCH,
    CR_BOOKS_MENU, CR_BOOKS_ADD, CR_BOOKS_VIEW, CR_BOOKS_DELETE, CR_BOOKS_SEARCH,
    CR_POEMS_MENU, CR_POEMS_ADD, CR_POEMS_VIEW, CR_POEMS_DELETE, CR_POEMS_SEARCH,
    CR_ART_MENU, CR_ART_ADD, CR_ART_VIEW, CR_ART_DELETE,
    QUOTE_MENU, QUOTE_ADD, QUOTE_DELETE,
    HOROSCOPE_MENU, HOROSCOPE_SIGN,
    VOICE_MENU,
    SETTINGS_MENU,
    NOTES_MENU, NOTES_ADD, NOTES_DELETE,
    PAYMENT_MENU, PROMO_INPUT,
    ROUTINE_MENU, ROUTINE_HABIT_SELECT, ROUTINE_HABIT_ADD, ROUTINE_HABIT_EDIT, ROUTINE_HABIT_VIEW,
    ROUTINE_CIGARETTE_START, ROUTINE_CIGARETTE_CURRENT, ROUTINE_CIGARETTE_GOAL, ROUTINE_CIGARETTE_DATE,
    ROUTINE_TEETH_LAST, ROUTINE_TEETH_GOAL, ROUTINE_BATH_LAST, ROUTINE_BATH_GOAL,
    ROUTINE_MONEY_GOAL, ROUTINE_MONEY_INCOME, ROUTINE_MONEY_DATE,
    ROUTINE_CHECKIN, ROUTINE_CHECKIN_DATE, ROUTINE_HISTORY,
    NUMEROLOGY_MENU, NUMEROLOGY_INPUT, NUMEROLOGY_VIEW, NUMEROLOGY_COMPATIBILITY,
    NUMEROLOGY_SELECT_PERSON, NUMEROLOGY_HISTORY,
    NOTIFICATIONS_MENU, NOTIFICATIONS_SET_TIME, NOTIFICATIONS_SET_DAYS,
    NOTIFICATIONS_SET_CONTENT,
) = range(101)

# ============ ТАРИФЫ ============

PREMIUM_FEATURES = {
    "TASKS": {"name": "📋 Задачи", "price": 40, "description": "Менеджер задач с дедлайнами"},
    "BUFFER": {"name": "📦 Буфер", "price": 30, "description": "Хранение паролей и дней рождения"},
    "CREATIVITY": {"name": "📚 Творчество", "price": 30, "description": "Музыка, книги, стихи, картины"},
    "QUOTES": {"name": "📖 Цитатник", "price": 20, "description": "Коллекция цитат"},
    "NOTES": {"name": "🗒️ Заметки", "price": 20, "description": "Текстовые заметки"},
    "HOROSCOPE": {"name": "🔮 Гороскоп/Мем", "price": 15, "description": "Ежедневный гороскоп и случайные мемы"},
    "ROUTINE": {"name": "🔄 Рутина", "price": 35, "description": "Трекинг привычек и плавные переходы"},
    "EGE_ALL": {"name": "📚 ЕГЭ (все предметы)", "price": 50, "description": "Доступ ко всем 15 предметам ЕГЭ"},
    "MATH_ADV": {"name": "🧮 Математика PRO", "price": 30, "description": "Продвинутые математические функции"},
    "NUMEROLOGY": {"name": "🔢 Нумерология", "price": 25, "description": "Арканы и совместимость"},
    "NOTIFICATIONS": {"name": "⏰ Уведомления", "price": 20, "description": "Настраиваемые напоминания"}
}

TARIFFS = {
    "base": {
        "name": "🔹 Базовый",
        "stars": 100,
        "features": ["VOICE", "DATE", "MATH_BASIC"],
        "description": "Голос, дата, базовая математика"
    },
    "full": {
        "name": "💎 Все включено",
        "stars": 250,
        "features": list(PREMIUM_FEATURES.keys()) + ["VOICE", "DATE", "MATH_BASIC", "MATH_ADV"],
        "description": "Все функции бота"
    }
}

# ============ ПРЕДМЕТЫ ЕГЭ ============

SUBJECTS = {
    "informatics": "💻 Информатика",
    "math_profile": "📐 Профильная математика",
    "society": "👥 Обществознание",
    "biology": "🧬 Биология",
    "english": "🇬🇧 Английский язык",
    "history": "📜 История",
    "physics": "⚡ Физика",
    "russian": "🇷🇺 Русский язык",
    "literature": "📚 Литература",
    "geography": "🌍 География",
    "chemistry": "🧪 Химия",
    "german": "🇩🇪 Немецкий язык",
    "french": "🇫🇷 Французский язык",
    "spanish": "🇪🇸 Испанский язык",
    "chinese": "🇨🇳 Китайский язык"
}

SUBJECT_EMOJI = {k: v.split()[0] for k, v in SUBJECTS.items()}
SUBJECT_NAMES_RU = {k: v.split(maxsplit=1)[1] for k, v in SUBJECTS.items()}

TASK_COUNTS = {
    "informatics": 27, "math_profile": 20, "society": 20, "biology": 28,
    "english": 20, "history": 25, "physics": 27, "russian": 26,
    "literature": 17, "geography": 31, "chemistry": 34, "german": 20,
    "french": 20, "spanish": 20, "chinese": 20
}

TASK_NAMES = {s: {i: f"Задание {i}" for i in range(1, TASK_COUNTS[s] + 1)} for s in SUBJECTS.keys()}


# ============ ENUMS ============

class EgeTaskStatus(Enum):
    NOT_STARTED = "❌"
    IN_PROGRESS = "🔄"
    COMPLETED = "✅"


class TaskPriority(Enum):
    LOW = "🟢 Низкий"
    MEDIUM = "🟡 Средний"
    HIGH = "🔴 Высокий"
    URGENT = "⚡ Срочный"


class TaskStatus(Enum):
    NOT_STARTED = "❌ Не начато"
    IN_PROGRESS = "🔄 В процессе"
    COMPLETED = "✅ Завершено"
    OVERDUE = "⚠️ Просрочено"


class HabitType(Enum):
    CIGARETTE = "🚬 Курение"
    TEETH = "🦷 Чистка зубов"
    BATH = "🚿 Купание"
    MONEY = "💰 Накопления"


class HabitUnit(Enum):
    CIGARETTES_PER_DAY = "сигарет в день"
    HOURS_PER_CIGARETTE = "часов на сигарету"
    DAYS = "дней"
    RUBLES = "рублей"


class CheckStatus(Enum):
    DONE = "✅"
    FAILED = "❌"
    SKIPPED = "⏭️"


class WeekDay(Enum):
    MONDAY = "Пн"
    TUESDAY = "Вт"
    WEDNESDAY = "Ср"
    THURSDAY = "Чт"
    FRIDAY = "Пт"
    SATURDAY = "Сб"
    SUNDAY = "Вс"


# ============ DATACLASSЫ ДЛЯ НУМЕРОЛОГИИ ============

@dataclass
class NumerologicalProfile:
    """Нумерологический профиль человека"""
    name: str
    birth_date: date
    arcana: Dict[str, int] = field(default_factory=dict)
    last_calculated: date = None

    def __post_init__(self):
        if self.last_calculated is None:
            self.last_calculated = date.today()
        self.calculate_all_arcana()

    def calculate_all_arcana(self):
        """Рассчитывает все арканы"""
        self.arcana = {
            "personality": self.calculate_personality_arcanum(),
            "soul": self.calculate_soul_arcanum(),
            "growth": self.calculate_growth_arcanum(),
            "year": self.calculate_year_arcanum(),
            "day": self.calculate_day_arcanum()
        }

    def calculate_personality_arcanum(self) -> int:
        total = self.birth_date.day + self.birth_date.month + self.birth_date.year
        return self._reduce_to_arcanum(total)

    def calculate_soul_arcanum(self) -> int:
        return self._reduce_to_arcanum(self.birth_date.day)

    def calculate_growth_arcanum(self) -> int:
        total = self.birth_date.month + self.birth_date.year
        return self._reduce_to_arcanum(total)

    def calculate_year_arcanum(self) -> int:
        today = date.today()
        total = self.birth_date.day + self.birth_date.month + today.year
        return self._reduce_to_arcanum(total)

    def calculate_day_arcanum(self) -> int:
        today = date.today()
        total = today.day + today.month + today.year
        return self._reduce_to_arcanum(total)

    def _reduce_to_arcanum(self, num: int) -> int:
        while num > 22:
            num = sum(int(d) for d in str(num))
        return num if num > 0 else 1

    def get_compatibility(self, other: 'NumerologicalProfile') -> Dict[str, int]:
        compatibility = {}
        for key in self.arcana.keys():
            if key in other.arcana:
                diff = abs(self.arcana[key] - other.arcana[key])
                compatibility[key] = max(0, 100 - (diff * 5))
        total = sum(compatibility.values())
        compatibility["total"] = total // len(compatibility) if compatibility else 0
        return compatibility

    def to_dict(self):
        return {
            "name": self.name,
            "birth_date": self.birth_date.isoformat(),
            "arcana": self.arcana,
            "last_calculated": self.last_calculated.isoformat() if self.last_calculated else None
        }

    @classmethod
    def from_dict(cls, data):
        profile = cls(
            name=data["name"],
            birth_date=date.fromisoformat(data["birth_date"])
        )
        profile.arcana = data.get("arcana", {})
        if data.get("last_calculated"):
            profile.last_calculated = date.fromisoformat(data["last_calculated"])
        return profile


@dataclass
class NotificationSettings:
    """Настройки уведомлений"""
    enabled: bool = False
    time: str = "09:00"
    days: List[str] = field(default_factory=lambda: [d.value for d in WeekDay])
    content_tasks: bool = True
    content_routine: bool = True
    content_ege: bool = False
    last_sent: Optional[datetime] = None

    def to_dict(self):
        return {
            "enabled": self.enabled,
            "time": self.time,
            "days": self.days,
            "content_tasks": self.content_tasks,
            "content_routine": self.content_routine,
            "content_ege": self.content_ege,
            "last_sent": self.last_sent.isoformat() if self.last_sent else None
        }

    @classmethod
    def from_dict(cls, data):
        settings = cls(
            enabled=data.get("enabled", False),
            time=data.get("time", "09:00"),
            days=data.get("days", [d.value for d in WeekDay]),
            content_tasks=data.get("content_tasks", True),
            content_routine=data.get("content_routine", True),
            content_ege=data.get("content_ege", False)
        )
        if data.get("last_sent"):
            settings.last_sent = datetime.fromisoformat(data["last_sent"])
        return settings


# ============ ОСТАЛЬНЫЕ DATACLASSЫ ============

@dataclass
class UserSettings:
    user_id: int
    visible_menu_items: Dict[str, bool] = None
    notifications: Optional[NotificationSettings] = None

    def __post_init__(self):
        if self.visible_menu_items is None:
            self.visible_menu_items = {
                "EGE": True, "MATH": True, "DATE": True, "VOICE": True,
                "TASKS": True, "BUFFER": True, "CREATIVITY": True,
                "QUOTES": True, "NOTES": True, "HOROSCOPE": True,
                "ROUTINE": True, "NUMEROLOGY": True, "NOTIFICATIONS": True,
                "SETTINGS": True, "EXIT": True
            }
        if self.notifications is None:
            self.notifications = NotificationSettings()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "visible_menu_items": self.visible_menu_items,
            "notifications": self.notifications.to_dict() if self.notifications else None
        }

    @classmethod
    def from_dict(cls, data):
        s = cls(user_id=data["user_id"])
        s.visible_menu_items = data.get("visible_menu_items", {})
        if data.get("notifications"):
            s.notifications = NotificationSettings.from_dict(data["notifications"])
        return s


@dataclass
class DailyCheck:
    date: date
    habit_type: str
    expected_value: float
    actual_value: Optional[float] = None
    status: Optional[CheckStatus] = None
    notes: str = ""

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "habit_type": self.habit_type,
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "status": self.status.value if self.status else None,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        status = None
        if data.get("status"):
            for s in CheckStatus:
                if s.value == data["status"]:
                    status = s
                    break
        return cls(
            date=date.fromisoformat(data["date"]),
            habit_type=data["habit_type"],
            expected_value=data["expected_value"],
            actual_value=data.get("actual_value"),
            status=status,
            notes=data.get("notes", "")
        )


@dataclass
class HabitGoal:
    habit_type: str
    target_date: date
    target_value: float
    unit: str
    created_at: Optional[date] = None
    achieved: bool = False
    notes: str = ""

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = date.today()

    def to_dict(self):
        return {
            "habit_type": self.habit_type,
            "target_date": self.target_date.isoformat(),
            "target_value": self.target_value,
            "unit": self.unit,
            "created_at": self.created_at.isoformat(),
            "achieved": self.achieved,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            habit_type=data["habit_type"],
            target_date=date.fromisoformat(data["target_date"]),
            target_value=data["target_value"],
            unit=data["unit"],
            created_at=date.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            achieved=data.get("achieved", False),
            notes=data.get("notes", "")
        )


@dataclass
class HabitState:
    habit_type: str
    current_value: float
    last_updated: date
    unit: str
    goals: List[HabitGoal] = field(default_factory=list)
    history: List[DailyCheck] = field(default_factory=list)

    def to_dict(self):
        return {
            "habit_type": self.habit_type,
            "current_value": self.current_value,
            "last_updated": self.last_updated.isoformat(),
            "unit": self.unit,
            "goals": [g.to_dict() for g in self.goals],
            "history": [h.to_dict() for h in self.history]
        }

    @classmethod
    def from_dict(cls, data):
        state = cls(
            habit_type=data["habit_type"],
            current_value=data["current_value"],
            last_updated=date.fromisoformat(data["last_updated"]),
            unit=data["unit"]
        )
        state.goals = [HabitGoal.from_dict(g) for g in data.get("goals", [])]
        state.history = [DailyCheck.from_dict(h) for h in data.get("history", [])]
        return state

    def get_today_expected(self) -> Optional[float]:
        today = date.today()
        active_goals = [g for g in self.goals if not g.achieved and g.target_date >= today]
        if not active_goals:
            return self.current_value
        next_goal = min(active_goals, key=lambda g: g.target_date)
        if next_goal.target_date == today:
            return next_goal.target_value
        days_total = (next_goal.target_date - next_goal.created_at).days
        days_passed = (today - next_goal.created_at).days
        progress = days_passed / days_total if days_total > 0 else 1
        if self.habit_type == HabitType.CIGARETTE.value:
            if "часов" in self.unit:
                return self.current_value + (next_goal.target_value - self.current_value) * progress
            else:
                return self.current_value - (self.current_value - next_goal.target_value) * progress
        else:
            return self.current_value + (next_goal.target_value - self.current_value) * progress

    def add_check(self, expected: float, actual: float, status: CheckStatus):
        check = DailyCheck(
            date=date.today(),
            habit_type=self.habit_type,
            expected_value=expected,
            actual_value=actual,
            status=status
        )
        self.history.append(check)
        if status == CheckStatus.DONE:
            self.current_value = actual
            self.last_updated = date.today()


@dataclass
class MoneyState:
    current_amount: float = 0
    weekly_income: float = 0
    goals: List[HabitGoal] = field(default_factory=list)
    transactions: List[Dict] = field(default_factory=list)

    def to_dict(self):
        return {
            "current_amount": self.current_amount,
            "weekly_income": self.weekly_income,
            "goals": [g.to_dict() for g in self.goals],
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        state = cls(
            current_amount=data.get("current_amount", 0),
            weekly_income=data.get("weekly_income", 0)
        )
        state.goals = [HabitGoal.from_dict(g) for g in data.get("goals", [])]
        state.transactions = data.get("transactions", [])
        return state


@dataclass
class UserRoutine:
    user_id: int
    cigarettes: Optional[HabitState] = None
    teeth: Optional[HabitState] = None
    bath: Optional[HabitState] = None
    money: Optional[MoneyState] = None

    def __post_init__(self):
        if self.cigarettes is None:
            self.cigarettes = HabitState(
                habit_type=HabitType.CIGARETTE.value,
                current_value=40,
                last_updated=date.today(),
                unit=HabitUnit.CIGARETTES_PER_DAY.value
            )
        if self.teeth is None:
            self.teeth = HabitState(
                habit_type=HabitType.TEETH.value,
                current_value=2,
                last_updated=date.today() - timedelta(days=1),
                unit=HabitUnit.DAYS.value
            )
        if self.bath is None:
            self.bath = HabitState(
                habit_type=HabitType.BATH.value,
                current_value=3,
                last_updated=date.today() - timedelta(days=2),
                unit=HabitUnit.DAYS.value
            )
        if self.money is None:
            self.money = MoneyState()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "cigarettes": self.cigarettes.to_dict() if self.cigarettes else None,
            "teeth": self.teeth.to_dict() if self.teeth else None,
            "bath": self.bath.to_dict() if self.bath else None,
            "money": self.money.to_dict() if self.money else None
        }

    @classmethod
    def from_dict(cls, data):
        routine = cls(user_id=data["user_id"])
        if data.get("cigarettes"):
            routine.cigarettes = HabitState.from_dict(data["cigarettes"])
        if data.get("teeth"):
            routine.teeth = HabitState.from_dict(data["teeth"])
        if data.get("bath"):
            routine.bath = HabitState.from_dict(data["bath"])
        if data.get("money"):
            routine.money = MoneyState.from_dict(data["money"])
        return routine


@dataclass
class SubjectProgress:
    completed_tasks: Set[int] = field(default_factory=set)
    in_progress_tasks: Set[int] = field(default_factory=set)

    def to_dict(self):
        return {"completed_tasks": list(self.completed_tasks),
                "in_progress_tasks": list(self.in_progress_tasks)}

    @classmethod
    def from_dict(cls, data):
        return cls(completed_tasks=set(data.get("completed_tasks", [])),
                   in_progress_tasks=set(data.get("in_progress_tasks", [])))


@dataclass
class UserProgress:
    user_id: int
    subjects: Dict[str, SubjectProgress] = field(default_factory=dict)

    def to_dict(self):
        return {"user_id": self.user_id,
                "subjects": {s: p.to_dict() for s, p in self.subjects.items()}}

    @classmethod
    def from_dict(cls, data):
        subjects = {s: SubjectProgress.from_dict(sd) for s, sd in data.get("subjects", {}).items()}
        return cls(user_id=data["user_id"], subjects=subjects)


@dataclass
class TodoTask:
    id: int
    name: str
    deadline: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.NOT_STARTED
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id, "name": self.name,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority.value, "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data):
        pr = TaskPriority.MEDIUM
        for p in TaskPriority:
            if p.value == data.get("priority"):
                pr = p
                break
        st = TaskStatus.NOT_STARTED
        for s in TaskStatus:
            if s.value == data.get("status"):
                st = s
                break
        return cls(
            id=data["id"], name=data["name"],
            deadline=datetime.fromisoformat(data["deadline"]) if data.get("deadline") else None,
            priority=pr, status=st,
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
        )


@dataclass
class UserTasks:
    user_id: int
    tasks: Dict[int, TodoTask] = field(default_factory=dict)
    next_id: int = 1

    def to_dict(self):
        return {"user_id": self.user_id,
                "tasks": {str(k): v.to_dict() for k, v in self.tasks.items()},
                "next_id": self.next_id}

    @classmethod
    def from_dict(cls, data):
        tasks = {int(k): TodoTask.from_dict(v) for k, v in data.get("tasks", {}).items()}
        return cls(user_id=data["user_id"], tasks=tasks, next_id=data.get("next_id", 1))

    def add_task(self, name, **kw):
        tid = self.next_id
        self.next_id += 1
        self.tasks[tid] = TodoTask(id=tid, name=name, **kw)
        return tid

    def check_deadlines(self):
        now = datetime.now()
        for t in self.tasks.values():
            if t.deadline and t.deadline < now and t.status not in (TaskStatus.COMPLETED, TaskStatus.OVERDUE):
                t.status = TaskStatus.OVERDUE


@dataclass
class QuoteEntry:
    id: int
    text: str
    author: str = ""
    date_added: Optional[date] = None

    def __post_init__(self):
        if self.date_added is None:
            self.date_added = date.today()

    def to_dict(self):
        return {"id": self.id, "text": self.text, "author": self.author,
                "date_added": self.date_added.isoformat()}

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], text=data["text"], author=data.get("author", ""),
                   date_added=date.fromisoformat(data["date_added"]) if data.get("date_added") else None)


@dataclass
class UserQuotes:
    user_id: int
    quotes: Dict[int, QuoteEntry] = field(default_factory=dict)
    next_id: int = 1

    def get_random(self):
        if not self.quotes:
            return None
        qid = random.choice(list(self.quotes.keys()))
        return self.quotes[qid]

    def to_dict(self):
        return {"user_id": self.user_id,
                "quotes": {str(k): v.to_dict() for k, v in self.quotes.items()},
                "next_id": self.next_id}

    @classmethod
    def from_dict(cls, data):
        quotes = {int(k): QuoteEntry.from_dict(v) for k, v in data.get("quotes", {}).items()}
        return cls(user_id=data["user_id"], quotes=quotes, next_id=data.get("next_id", 1))

    def add_quote(self, text, author=""):
        qid = self.next_id
        self.next_id += 1
        self.quotes[qid] = QuoteEntry(id=qid, text=text, author=author)
        return qid


@dataclass
class NoteEntry:
    id: int
    title: str
    text: str
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return {"id": self.id, "title": self.title, "text": self.text,
                "created_at": self.created_at.isoformat()}

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], title=data["title"], text=data["text"],
                   created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None)


@dataclass
class UserNotes:
    user_id: int
    notes: Dict[int, NoteEntry] = field(default_factory=dict)
    next_id: int = 1

    def to_dict(self):
        return {"user_id": self.user_id,
                "notes": {str(k): v.to_dict() for k, v in self.notes.items()},
                "next_id": self.next_id}

    @classmethod
    def from_dict(cls, data):
        notes = {int(k): NoteEntry.from_dict(v) for k, v in data.get("notes", {}).items()}
        return cls(user_id=data["user_id"], notes=notes, next_id=data.get("next_id", 1))

    def add_note(self, title, text):
        nid = self.next_id
        self.next_id += 1
        self.notes[nid] = NoteEntry(id=nid, title=title, text=text)
        return nid


@dataclass
class PasswordEntry:
    service: str
    login: str
    password: str
    notes: str = ""

    def to_dict(self):
        return {"service": self.service, "login": self.login,
                "password": self.password, "notes": self.notes}

    @classmethod
    def from_dict(cls, data):
        return cls(service=data["service"], login=data["login"],
                   password=data["password"], notes=data.get("notes", ""))


@dataclass
class BirthdayEntry:
    name: str
    date: date
    notes: str = ""

    def to_dict(self):
        return {"name": self.name, "date": self.date.isoformat(), "notes": self.notes}

    @classmethod
    def from_dict(cls, data):
        return cls(name=data["name"], date=date.fromisoformat(data["date"]),
                   notes=data.get("notes", ""))


@dataclass
class UserBuffer:
    user_id: int
    personal_info: Dict[str, str] = field(default_factory=dict)
    passwords: List[PasswordEntry] = field(default_factory=list)
    birthdays: List[BirthdayEntry] = field(default_factory=list)

    def to_dict(self):
        return {"user_id": self.user_id, "personal_info": self.personal_info,
                "passwords": [p.to_dict() for p in self.passwords],
                "birthdays": [b.to_dict() for b in self.birthdays]}

    @classmethod
    def from_dict(cls, data):
        b = cls(user_id=data["user_id"])
        b.personal_info = data.get("personal_info", {})
        b.passwords = [PasswordEntry.from_dict(p) for p in data.get("passwords", [])]
        b.birthdays = [BirthdayEntry.from_dict(bd) for bd in data.get("birthdays", [])]
        return b


@dataclass
class MusicTrack:
    id: int
    title: str
    duration: str
    lyrics: str = ""
    notes: str = ""
    order: int = 0

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "lyrics": self.lyrics,
            "notes": self.notes,
            "order": self.order
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            duration=data["duration"],
            lyrics=data.get("lyrics", ""),
            notes=data.get("notes", ""),
            order=data.get("order", 0)
        )


@dataclass
class MusicAlbum:
    id: int
    title: str
    artist: str
    year: int
    genre: str = ""
    concept: str = ""
    cover: str = ""
    tracks: Dict[int, MusicTrack] = field(default_factory=dict)
    next_track_id: int = 1
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_track(self, title: str, duration: str, lyrics: str = "", notes: str = "") -> int:
        track_id = self.next_track_id
        self.next_track_id += 1
        self.tracks[track_id] = MusicTrack(
            id=track_id,
            title=title,
            duration=duration,
            lyrics=lyrics,
            notes=notes,
            order=len(self.tracks)
        )
        return track_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "genre": self.genre,
            "concept": self.concept,
            "cover": self.cover,
            "tracks": {str(k): v.to_dict() for k, v in self.tracks.items()},
            "next_track_id": self.next_track_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data):
        album = cls(
            id=data["id"],
            title=data["title"],
            artist=data["artist"],
            year=data["year"],
            genre=data.get("genre", ""),
            concept=data.get("concept", ""),
            cover=data.get("cover", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )
        album.next_track_id = data.get("next_track_id", 1)
        album.tracks = {int(k): MusicTrack.from_dict(v) for k, v in data.get("tracks", {}).items()}
        return album


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    genre: str = ""
    pages: int = 0
    rating: float = 0.0
    notes: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
            "pages": self.pages,
            "rating": self.rating,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data.get("genre", ""),
            pages=data.get("pages", 0),
            rating=data.get("rating", 0.0),
            notes=data.get("notes", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )


@dataclass
class Poem:
    id: int
    title: str
    author: str
    text: str
    year: int = 0
    notes: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "text": self.text,
            "year": self.year,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            text=data["text"],
            year=data.get("year", 0),
            notes=data.get("notes", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )


@dataclass
class Artwork:
    id: int
    title: str
    artist: str
    year: int
    technique: str = ""
    description: str = ""
    notes: str = ""
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "year": self.year,
            "technique": self.technique,
            "description": self.description,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            artist=data["artist"],
            year=data["year"],
            technique=data.get("technique", ""),
            description=data.get("description", ""),
            notes=data.get("notes", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None
        )


@dataclass
class UserCreativity:
    user_id: int
    music_albums: Dict[int, MusicAlbum] = field(default_factory=dict)
    books: Dict[int, Book] = field(default_factory=dict)
    poems: Dict[int, Poem] = field(default_factory=dict)
    artworks: Dict[int, Artwork] = field(default_factory=dict)
    next_music_id: int = 1
    next_book_id: int = 1
    next_poem_id: int = 1
    next_art_id: int = 1

    def add_music_album(self, title: str, artist: str, year: int, genre: str = "", concept: str = "",
                        cover: str = "") -> int:
        album_id = self.next_music_id
        self.next_music_id += 1
        self.music_albums[album_id] = MusicAlbum(
            id=album_id,
            title=title,
            artist=artist,
            year=year,
            genre=genre,
            concept=concept,
            cover=cover
        )
        return album_id

    def add_book(self, title: str, author: str, year: int, genre: str = "", pages: int = 0, rating: float = 0.0,
                 notes: str = "") -> int:
        book_id = self.next_book_id
        self.next_book_id += 1
        self.books[book_id] = Book(
            id=book_id,
            title=title,
            author=author,
            year=year,
            genre=genre,
            pages=pages,
            rating=rating,
            notes=notes
        )
        return book_id

    def add_poem(self, title: str, author: str, text: str, year: int = 0, notes: str = "") -> int:
        poem_id = self.next_poem_id
        self.next_poem_id += 1
        self.poems[poem_id] = Poem(
            id=poem_id,
            title=title,
            author=author,
            text=text,
            year=year,
            notes=notes
        )
        return poem_id

    def add_artwork(self, title: str, artist: str, year: int, technique: str = "", description: str = "",
                    notes: str = "") -> int:
        art_id = self.next_art_id
        self.next_art_id += 1
        self.artworks[art_id] = Artwork(
            id=art_id,
            title=title,
            artist=artist,
            year=year,
            technique=technique,
            description=description,
            notes=notes
        )
        return art_id

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "music_albums": {str(k): v.to_dict() for k, v in self.music_albums.items()},
            "books": {str(k): v.to_dict() for k, v in self.books.items()},
            "poems": {str(k): v.to_dict() for k, v in self.poems.items()},
            "artworks": {str(k): v.to_dict() for k, v in self.artworks.items()},
            "next_music_id": self.next_music_id,
            "next_book_id": self.next_book_id,
            "next_poem_id": self.next_poem_id,
            "next_art_id": self.next_art_id
        }

    @classmethod
    def from_dict(cls, data):
        creativity = cls(user_id=data["user_id"])
        creativity.next_music_id = data.get("next_music_id", 1)
        creativity.next_book_id = data.get("next_book_id", 1)
        creativity.next_poem_id = data.get("next_poem_id", 1)
        creativity.next_art_id = data.get("next_art_id", 1)

        creativity.music_albums = {int(k): MusicAlbum.from_dict(v) for k, v in data.get("music_albums", {}).items()}
        creativity.books = {int(k): Book.from_dict(v) for k, v in data.get("books", {}).items()}
        creativity.poems = {int(k): Poem.from_dict(v) for k, v in data.get("poems", {}).items()}
        creativity.artworks = {int(k): Artwork.from_dict(v) for k, v in data.get("artworks", {}).items()}

        return creativity


@dataclass
class UserNumerology:
    user_id: int
    profiles: Dict[str, NumerologicalProfile] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)
    next_id: int = 1

    def add_profile(self, name: str, birth_date: date) -> NumerologicalProfile:
        profile = NumerologicalProfile(name=name, birth_date=birth_date)
        self.profiles[name] = profile
        if name not in self.history:
            self.history.append(name)
            if len(self.history) > 20:
                self.history.pop(0)
        return profile

    def get_profile(self, name: str) -> Optional[NumerologicalProfile]:
        return self.profiles.get(name)

    def get_compatibility(self, name1: str, name2: str) -> Optional[Dict[str, int]]:
        profile1 = self.profiles.get(name1)
        profile2 = self.profiles.get(name2)
        if profile1 and profile2:
            return profile1.get_compatibility(profile2)
        return None

    def sync_with_buffer(self, buffer: UserBuffer):
        for birthday in buffer.birthdays:
            if birthday.name not in self.profiles:
                self.add_profile(birthday.name, birthday.date)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "profiles": {name: p.to_dict() for name, p in self.profiles.items()},
            "history": self.history,
            "next_id": self.next_id
        }

    @classmethod
    def from_dict(cls, data):
        numerology = cls(user_id=data["user_id"])
        numerology.profiles = {name: NumerologicalProfile.from_dict(p)
                               for name, p in data.get("profiles", {}).items()}
        numerology.history = data.get("history", [])
        numerology.next_id = data.get("next_id", 1)
        return numerology


# ============ ПЛАТЁЖНАЯ СИСТЕМА ============

class PaymentSystem:
    def __init__(self):
        self.payments_file = "payments.json"
        self.payments = self._load_payments()
        self.user_promos_file = "user_promos.json"
        self.user_promos = self._load_user_promos()

    def _load_payments(self):
        if not os.path.exists(self.payments_file):
            return {}
        try:
            with open(self.payments_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {int(uid): info for uid, info in data.items()}
        except Exception as e:
            print(f"Ошибка загрузки платежей: {e}")
            return {}

    def _save_payments(self):
        try:
            with open(self.payments_file, 'w', encoding='utf-8') as f:
                json.dump({str(uid): info for uid, info in self.payments.items()},
                          f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения платежей: {e}")

    def _load_user_promos(self):
        if not os.path.exists(self.user_promos_file):
            return {}
        try:
            with open(self.user_promos_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {int(uid): info for uid, info in data.items()}
        except Exception as e:
            print(f"Ошибка загрузки промокодов: {e}")
            return {}

    def _save_user_promos(self):
        try:
            with open(self.user_promos_file, 'w', encoding='utf-8') as f:
                json.dump({str(uid): info for uid, info in self.user_promos.items()},
                          f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения промокодов: {e}")

    def get_user_subscription(self, user_id: int) -> dict:
        if user_id not in self.payments:
            return {"tariff": None, "features": [], "active": False}
        payment_info = self.payments[user_id]
        expiry = payment_info.get('expiry_date')
        if expiry:
            try:
                expiry_date = datetime.fromisoformat(expiry).date()
                if expiry_date < date.today():
                    payment_info['active'] = False
                    self._save_payments()
            except:
                pass
        return payment_info

    def has_feature(self, user_id: int, feature: str) -> bool:
        sub = self.get_user_subscription(user_id)
        if not sub.get('active', False):
            return False
        tariff = sub.get('tariff')
        if tariff == 'full':
            return True
        elif tariff == 'base':
            return feature in ['VOICE', 'DATE', 'MATH_BASIC']
        elif tariff == 'custom':
            return feature in sub.get('features', [])
        return False

    def activate_tariff(self, user_id: int, tariff: str, months: int = 1, custom_features=None):
        today = date.today()
        expiry_date = date(today.year + (today.month + months - 1) // 12,
                           ((today.month + months - 1) % 12) + 1,
                           today.day)
        payment_info = {
            'active': True,
            'tariff': tariff,
            'activated_date': today.isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'months': months
        }
        if tariff == 'custom' and custom_features:
            payment_info['features'] = custom_features
        self.payments[user_id] = payment_info
        self._save_payments()

    def apply_promo(self, user_id: int, promo_code: str) -> Optional[dict]:
        promo = validate_promo(promo_code)
        if not promo:
            return None
        if user_id in self.user_promos and promo_code in self.user_promos[user_id]:
            return None
        use_promo(promo_code)
        if user_id not in self.user_promos:
            self.user_promos[user_id] = []
        self.user_promos[user_id].append(promo_code)
        self._save_user_promos()
        return promo


payment_system = PaymentSystem()
load_promo_usage()


# ============ ДАТАБЕЙЗ ============

class Database:
    def __init__(self):
        self.settings: Dict[int, UserSettings] = self._load("settings.json", UserSettings)
        self.quotes: Dict[int, UserQuotes] = self._load("quotes.json", UserQuotes)
        self.notes: Dict[int, UserNotes] = self._load("notes.json", UserNotes)
        self.buffer: Dict[int, UserBuffer] = self._load("buffer.json", UserBuffer)
        self.tasks: Dict[int, UserTasks] = self._load("tasks.json", UserTasks)
        self.ege: Dict[int, UserProgress] = self._load("ege.json", UserProgress)
        self.routine: Dict[int, UserRoutine] = self._load("routine.json", UserRoutine)
        self.creativity: Dict[int, UserCreativity] = self._load("creativity.json", UserCreativity)
        self.numerology: Dict[int, UserNumerology] = self._load("numerology.json", UserNumerology)
        self.ege_subjects_settings: Dict[int, dict] = self._load_dict("ege_subjects.json")
        self.exam_dates: Dict[int, dict] = self._load_dict("exam_dates.json")

    def _load(self, filename, cls):
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {int(uid): cls.from_dict(ud) for uid, ud in data.items()}
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return {}

    def _load_dict(self, filename):
        if not os.path.exists(filename):
            return {}
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return {int(uid): ud for uid, ud in data.items()}
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            return {}

    def _save(self, filename, data):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({str(uid): ud.to_dict() if hasattr(ud, 'to_dict') else ud
                           for uid, ud in data.items()}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения {filename}: {e}")

    def get_settings(self, uid):
        if uid not in self.settings:
            self.settings[uid] = UserSettings(user_id=uid)
        return self.settings[uid]

    def save_settings(self):
        self._save("settings.json", self.settings)

    def get_quotes(self, uid):
        if uid not in self.quotes:
            self.quotes[uid] = UserQuotes(user_id=uid)
        return self.quotes[uid]

    def save_quotes(self):
        self._save("quotes.json", self.quotes)

    def get_notes(self, uid):
        if uid not in self.notes:
            self.notes[uid] = UserNotes(user_id=uid)
        return self.notes[uid]

    def save_notes(self):
        self._save("notes.json", self.notes)

    def get_buffer(self, uid):
        if uid not in self.buffer:
            self.buffer[uid] = UserBuffer(user_id=uid)
        return self.buffer[uid]

    def save_buffer(self):
        self._save("buffer.json", self.buffer)

    def get_tasks(self, uid):
        if uid not in self.tasks:
            self.tasks[uid] = UserTasks(user_id=uid)
        self.tasks[uid].check_deadlines()
        return self.tasks[uid]

    def save_tasks(self):
        self._save("tasks.json", self.tasks)

    def get_ege(self, uid):
        if uid not in self.ege:
            subjects = {s: SubjectProgress() for s in SUBJECTS.keys()}
            self.ege[uid] = UserProgress(user_id=uid, subjects=subjects)
        return self.ege[uid]

    def save_ege(self):
        self._save("ege.json", self.ege)

    def get_routine(self, uid):
        if uid not in self.routine:
            self.routine[uid] = UserRoutine(user_id=uid)
        return self.routine[uid]

    def save_routine(self):
        self._save("routine.json", self.routine)

    def get_creativity(self, uid):
        if uid not in self.creativity:
            self.creativity[uid] = UserCreativity(user_id=uid)
        return self.creativity[uid]

    def save_creativity(self):
        self._save("creativity.json", self.creativity)

    def get_numerology(self, uid):
        if uid not in self.numerology:
            self.numerology[uid] = UserNumerology(user_id=uid)
        return self.numerology[uid]

    def save_numerology(self):
        self._save("numerology.json", self.numerology)

    def get_ege_task_status(self, uid, subject, task_num):
        sp = self.get_ege(uid).subjects.get(subject, SubjectProgress())
        if task_num in sp.completed_tasks:
            return EgeTaskStatus.COMPLETED
        elif task_num in sp.in_progress_tasks:
            return EgeTaskStatus.IN_PROGRESS
        return EgeTaskStatus.NOT_STARTED

    def toggle_ege_task(self, uid, subject, task_num):
        sp = self.get_ege(uid).subjects.get(subject)
        if sp is None:
            return
        cur = self.get_ege_task_status(uid, subject, task_num)
        sp.completed_tasks.discard(task_num)
        sp.in_progress_tasks.discard(task_num)
        if cur == EgeTaskStatus.NOT_STARTED:
            sp.in_progress_tasks.add(task_num)
        elif cur == EgeTaskStatus.IN_PROGRESS:
            sp.completed_tasks.add(task_num)
        self.save_ege()

    def get_ege_subjects_settings(self, uid):
        if uid not in self.ege_subjects_settings:
            self.ege_subjects_settings[uid] = {s: True for s in SUBJECTS.keys()}
        return self.ege_subjects_settings[uid]

    def save_ege_subjects_settings(self):
        self._save("ege_subjects.json", self.ege_subjects_settings)

    def toggle_ege_subject(self, uid, subject):
        settings = self.get_ege_subjects_settings(uid)
        settings[subject] = not settings.get(subject, True)
        self.save_ege_subjects_settings()

    def get_exam_dates(self, uid):
        if uid not in self.exam_dates:
            self.exam_dates[uid] = {}
        return self.exam_dates[uid]

    def set_exam_date(self, uid, subject, exam_date):
        dates = self.get_exam_dates(uid)
        dates[subject] = exam_date.isoformat()
        self._save("exam_dates.json", self.exam_dates)

    def get_exam_date(self, uid, subject):
        dates = self.get_exam_dates(uid)
        date_str = dates.get(subject)
        if date_str:
            try:
                return date.fromisoformat(date_str)
            except:
                return None
        return None

    def get_urgent_tasks(self, uid, days=7):
        tasks = self.get_tasks(uid)
        now = datetime.now()
        urgent = []
        for task in tasks.tasks.values():
            if task.deadline and task.status not in [TaskStatus.COMPLETED, TaskStatus.OVERDUE]:
                days_left = (task.deadline - now).days
                if 0 <= days_left <= days:
                    urgent.append(task)
        return urgent


db = Database()


# ============ УТИЛИТЫ ============

def format_date_russian(d):
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    return f"{d.day} {months[d.month]} {d.year} года"


def get_weekday_russian(weekday):
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    return days[weekday]


def get_zodiac_sign(day: int, month: int) -> str:
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "♈ Овен"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "♉ Телец"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "♊ Близнецы"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "♋ Рак"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "♌ Лев"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "♍ Дева"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "♎ Весы"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "♏ Скорпион"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "♐ Стрелец"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "♑ Козерог"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "♒ Водолей"
    else:
        return "♓ Рыбы"


def get_horoscope(sign: str) -> str:
    horoscopes = [
        "Сегодня звёзды благоволят новым начинаниям. Самое время начать проект, который давно откладывали!",
        "Будьте осторожны в финансовых вопросах. Не подписывайте сомнительные документы.",
        "День благоприятен для общения. Старые друзья напомнят о себе.",
        "Энергия переполняет вас! Направьте её в спорт или творчество.",
        "Возможны небольшие трудности на работе, но вы с ними легко справитесь.",
        "Отличный день для романтических свиданий и признаний в любви.",
        "Прислушайтесь к интуиции — она подскажет верное решение.",
        "Звёзды советуют отдохнуть и набраться сил перед важным рывком.",
        "Удача на вашей стороне! Используйте шанс, который подвернется.",
        "Сегодня лучше избегать конфликтов и сохранять спокойствие.",
        "Ваша креативность сегодня на высоте. Творите и удивляйте!",
        "Хороший день для самообразования и изучения нового."
    ]
    return f"🔮 {sign}\n\n{random.choice(horoscopes)}"


def get_random_meme() -> str:
    memes = [
        "😂 Почему программисты путают Хэллоуин и Рождество?\nПотому что Oct 31 == Dec 25!",
        "🤓 Приходит как-то байт к битам:\n— Что-то я притомился...\n— Отдохни, побайть!",
        "😅 — Почему студенты не любят дроби?\n— Потому что они всегда что-то делят!",
        "😏 Жизнь программиста: сегодня фича, завтра баг, послезавтра legacy.",
        "😂 Разговор двух студентов:\n— Ты на пару идешь?\n— Нет, я уже ушел!"
    ]
    return f"😂 **Мем дня**\n\n{random.choice(memes)}"
# ============ ГОРОСКОП ============

async def show_horoscope_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    keyboard = [
        ["🔮 Гороскоп", "😂 Случайный мем"],
        ["↩️ Назад"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🔮 **Гороскоп и Мемы**\n\n"
        "• Узнай свой гороскоп на сегодня\n"
        "• Получи случайный мем для поднятия настроения",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )
    return HOROSCOPE_MENU


async def horoscope_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад":
        return await go_main(update, context)

    elif t == "🔮 Гороскоп":
        zodiac_signs = [
            ["♈ Овен", "♉ Телец", "♊ Близнецы"],
            ["♋ Рак", "♌ Лев", "♍ Дева"],
            ["♎ Весы", "♏ Скорпион", "♐ Стрелец"],
            ["♑ Козерог", "♒ Водолей", "♓ Рыбы"],
            ["↩️ Назад"]
        ]
        reply_markup = ReplyKeyboardMarkup(zodiac_signs, resize_keyboard=True)
        await update.message.reply_text("Выберите свой знак зодиака:", reply_markup=reply_markup)
        return HOROSCOPE_SIGN

    elif t == "😂 Случайный мем":
        await update.message.reply_text(get_random_meme(), parse_mode=ParseMode.MARKDOWN)
        return HOROSCOPE_MENU

    return HOROSCOPE_MENU


async def horoscope_sign_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад":
        return await show_horoscope_menu(update, context)

    zodiac_signs = ["♈ Овен", "♉ Телец", "♊ Близнецы", "♋ Рак", "♌ Лев", "♍ Дева",
                    "♎ Весы", "♏ Скорпион", "♐ Стрелец", "♑ Козерог", "♒ Водолей", "♓ Рыбы"]

    if t in zodiac_signs:
        horoscope = get_horoscope(t)
        await update.message.reply_text(horoscope, parse_mode=ParseMode.MARKDOWN)
        return HOROSCOPE_SIGN

    return HOROSCOPE_SIGN

def main_kb(uid):
    settings = db.get_settings(uid)
    items = [
        ("EGE", "📂 ЕГЭ"), ("MATH", "🧮 Математика"), ("DATE", "📅 Дата"),
        ("VOICE", "🎙️ Голос"), ("TASKS", "📋 Задачи"), ("BUFFER", "📦 Буфер"),
        ("CREATIVITY", "📚 Творчество"), ("QUOTES", "📖 Цитатник"),
        ("HOROSCOPE", "🔮 Гороскоп/Мем"), ("NOTES", "🗒️ Заметки"),
        ("ROUTINE", "🔄 Рутина"), ("NUMEROLOGY", "🔢 Нумерология"),
        ("NOTIFICATIONS", "⏰ Уведомления"), ("SETTINGS", "⚙️ Настройки"), ("EXIT", "❌ Выход")
    ]
    keyboard, row = [], []
    for key, label in items:
        if key in ["TASKS", "BUFFER", "CREATIVITY", "QUOTES", "NOTES", "HOROSCOPE", "ROUTINE", "NUMEROLOGY",
                   "NOTIFICATIONS"]:
            if not payment_system.has_feature(uid, key):
                continue
        if key == "MATH" and not payment_system.has_feature(uid, "MATH_ADV"):
            if settings.visible_menu_items.get(key, True):
                row.append("🧮 Математика (база)")
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            continue
        if settings.visible_menu_items.get(key, True):
            row.append(label)
            if len(row) == 2:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def back_kb(text="↩️ Назад"):
    return ReplyKeyboardMarkup([[text]], resize_keyboard=True)


# ============ ПЛАТЕЖИ И ПРОМОКОДЫ ============

async def show_payment_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    uid = update.effective_user.id
    sub = payment_system.get_user_subscription(uid)

    text = "💰 **МЕНЮ ОПЛАТЫ**\n\n"

    if sub.get('active', False):
        tariff_info = TARIFFS.get(sub.get('tariff'), {})
        text += f"✅ **У вас активна подписка!**\n"
        text += f"📊 Тариф: {tariff_info.get('name', 'Неизвестный')}\n"
        text += f"📅 Действует до: {sub.get('expiry_date', 'неизвестно')}\n\n"
    else:
        text += "❌ **У вас нет активной подписки**\n\n"

    text += "**Доступные тарифы:**\n"
    text += f"🔹 **Базовый** — {TARIFFS['base']['stars']}⭐/мес\n"
    text += f"  {TARIFFS['base']['description']}\n\n"
    text += f"💎 **Все включено** — {TARIFFS['full']['stars']}⭐/мес\n"
    text += f"  {TARIFFS['full']['description']}\n\n"
    text += f"🔧 **Настраиваемый**\n"
    text += f"  Выбирай только нужные опции\n\n"

    kb = ReplyKeyboardMarkup([
        ["🔹 Базовый 100⭐", "💎 Все включено 250⭐"],
        ["🔧 Настроить свой", "🎟️ Ввести промокод"],
        ["📊 Статус подписки", "↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return PAYMENT_MENU


async def payment_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад":
        return await go_main(update, context)

    elif t == "📊 Статус подписки":
        return await cmd_premium_status(update, context)

    elif t == "🎟️ Ввести промокод":
        await update.message.reply_text(
            "🎟️ **ВВЕДИТЕ ПРОМОКОД**\n\n"
            "Отправьте промокод в чат.\n\n"
            "Промокоды выдаются администратором бота.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_kb()
        )
        context.user_data['awaiting_promo'] = True
        return PROMO_INPUT

    elif t == "🔹 Базовый 100⭐":
        await send_payment_invoice(update, context, "base", TARIFFS['base']['stars'])

    elif t == "💎 Все включено 250⭐":
        await send_payment_invoice(update, context, "full", TARIFFS['full']['stars'])

    elif t == "🔧 Настроить свой":
        return await show_custom_tariff_menu(update, context)

    return PAYMENT_MENU


async def show_custom_tariff_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_payment_menu(update, context)
    if 'custom_features' not in context.user_data:
        context.user_data['custom_features'] = []

    selected = context.user_data['custom_features']
    total = sum(PREMIUM_FEATURES[f]['price'] for f in selected)

    text = "🔧 **НАСТРОЙКА ТАРИФА**\n\n"
    text += f"**Текущая сумма:** {total}⭐/мес\n\n"
    text += "Выберите нужные опции (отправляйте названия):\n\n"

    for key, feature in PREMIUM_FEATURES.items():
        status = "✅ " if key in selected else "❌ "
        text += f"{status}{feature['name']} — {feature['price']}⭐\n"

    text += f"\nПосле выбора всех опций нажмите '✅ Готово и оплатить'"

    kb_buttons = [["✅ Готово и оплатить", "❌ Очистить всё"], ["↩️ Назад"]]

    for key, feature in PREMIUM_FEATURES.items():
        short_name = feature['name'].split()[1] if len(feature['name'].split()) > 1 else feature['name']
        kb_buttons.insert(0, [feature['name']])

    kb = ReplyKeyboardMarkup(kb_buttons, resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return PAYMENT_MENU


async def custom_tariff_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад":
        return await show_payment_menu(update, context)

    elif t == "❌ Очистить всё":
        context.user_data['custom_features'] = []
        return await show_custom_tariff_menu(update, context)

    elif t == "✅ Готово и оплатить":
        features = context.user_data.get('custom_features', [])
        if not features:
            await update.message.reply_text("❌ Выберите хотя бы одну опцию!")
            return await show_custom_tariff_menu(update, context)

        total = sum(PREMIUM_FEATURES[f]['price'] for f in features)
        await send_payment_invoice(update, context, "custom", total, features)

    else:
        for key, feature in PREMIUM_FEATURES.items():
            if t == feature['name']:
                if 'custom_features' not in context.user_data:
                    context.user_data['custom_features'] = []

                if key in context.user_data['custom_features']:
                    context.user_data['custom_features'].remove(key)
                    await update.message.reply_text(f"❌ {feature['name']} удалена")
                else:
                    context.user_data['custom_features'].append(key)
                    await update.message.reply_text(f"✅ {feature['name']} добавлена")

                return await show_custom_tariff_menu(update, context)

    return PAYMENT_MENU


async def send_payment_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE, tariff_type: str, amount: int,
                               features=None):
    if tariff_type == "base":
        title = "Гонзо Бот — Базовый тариф"
        description = "30 дней доступа к базовым функциям"
        payload = "base_tariff"
    elif tariff_type == "full":
        title = "Гонзо Бот — Все включено"
        description = "30 дней доступа ко всем функциям"
        payload = "full_tariff"
    else:
        title = "Гонзо Бот — Настраиваемый тариф"
        description = f"Выбранные опции"
        payload = "custom_tariff"
        if features:
            context.user_data['pending_features'] = features

    try:
        await context.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Тариф", amount=amount)],
            start_parameter=payload
        )
    except Exception as e:
        print(f"Ошибка отправки инвойса: {e}")
        await update.message.reply_text(f"❌ Ошибка при создании счета: {e}")


async def promo_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🔥 ПОЛУЧЕН ПРОМОКОД: {update.message.text}")

    if update.message.text == "↩️ Назад":
        context.user_data.pop('awaiting_promo', None)
        return await show_payment_menu(update, context)

    promo_code = update.message.text.upper().strip()
    user_id = update.effective_user.id

    promo = payment_system.apply_promo(user_id, promo_code)

    if promo:
        discount = promo["discount"]
        context.user_data.pop('awaiting_promo', None)

        if discount == 100:
            payment_system.activate_tariff(user_id, 'full')
            await update.message.reply_text(
                "🎉 **ПОЗДРАВЛЯЮ!**\n\n"
                "Промокод активирован! Вы получили **полный бесплатный доступ** на 1 месяц!\n\n"
                "Все функции бота теперь разблокированы. Спасибо за использование Гонзо Бота! 🦍",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                f"✅ **Промокод активирован!**\n\n"
                f"Ваша скидка: **{discount}%**\n\n"
                f"Теперь выберите тариф для оплаты:",
                parse_mode=ParseMode.MARKDOWN
            )
            text = "💰 **ТАРИФЫ СО СКИДКОЙ**\n\n"
            text += f"🔹 **Базовый** — ~~{TARIFFS['base']['stars']}⭐~~ → **{TARIFFS['base']['stars'] * (100 - discount) // 100}⭐**\n"
            text += f"  {TARIFFS['base']['description']}\n\n"
            text += f"💎 **Все включено** — ~~{TARIFFS['full']['stars']}⭐~~ → **{TARIFFS['full']['stars'] * (100 - discount) // 100}⭐**\n"
            text += f"  {TARIFFS['full']['description']}\n\n"

            context.user_data['active_promo'] = {
                'code': promo_code,
                'discount': discount
            }

            kb = ReplyKeyboardMarkup([
                [f"🔹 Базовый {TARIFFS['base']['stars'] * (100 - discount) // 100}⭐"],
                [f"💎 Все включено {TARIFFS['full']['stars'] * (100 - discount) // 100}⭐"],
                ["❌ Отмена"]
            ], resize_keyboard=True)

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    else:
        await update.message.reply_text(
            "❌ **Неверный или уже использованный промокод!**\n\n"
            "Попробуйте ещё раз или вернитесь к выбору тарифа.",
            parse_mode=ParseMode.MARKDOWN
        )

    return MAIN_MENU


async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    payload = update.message.successful_payment.invoice_payload

    if payload == "base_tariff":
        payment_system.activate_tariff(user_id, 'base')
        await update.message.reply_text(
            "✅ **Базовый тариф активирован!**\n\n"
            "Доступные функции:\n"
            "• 🎙️ Голос\n"
            "• 📅 Дата\n"
            "• 🧮 Базовая математика\n\n"
            "Спасибо за поддержку! ❤️",
            parse_mode=ParseMode.MARKDOWN
        )

    elif payload == "full_tariff":
        payment_system.activate_tariff(user_id, 'full')
        await update.message.reply_text(
            "✅ **Тариф 'Все включено' активирован!**\n\n"
            "Вам доступны абсолютно все функции бота!\n"
            "Спасибо за поддержку! ❤️",
            parse_mode=ParseMode.MARKDOWN
        )

    elif payload == "custom_tariff":
        features = context.user_data.get('pending_features', [])
        payment_system.activate_tariff(user_id, 'custom', custom_features=features)
        context.user_data.pop('pending_features', None)

        total = sum(PREMIUM_FEATURES[f]['price'] for f in features)
        text = "✅ **Настраиваемый тариф активирован!**\n\n"
        text += f"Оплачено: {total}⭐/мес\n\n"
        text += "Доступны функции:\n"
        for f in features:
            text += f"• {PREMIUM_FEATURES[f]['name']}\n"

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def cmd_premium_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    sub = payment_system.get_user_subscription(user_id)

    if sub.get('active', False):
        tariff_info = TARIFFS.get(sub.get('tariff'), {})
        text = f"✅ **У вас активна подписка!**\n\n"
        text += f"📊 Тариф: {tariff_info.get('name', 'Неизвестный')}\n"
        text += f"📅 Действует до: {sub.get('expiry_date', 'неизвестно')}\n"

        if sub.get('tariff') == 'custom':
            text += f"\n📦 Опции:\n"
            for f in sub.get('features', []):
                text += f"• {PREMIUM_FEATURES[f]['name']}\n"

        kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    else:
        kb = ReplyKeyboardMarkup([["💳 Купить подписку", "↩️ Назад"]], resize_keyboard=True)
        await update.message.reply_text(
            "❌ **У вас нет активной подписки**\n\n"
            "Нажмите '💳 Купить подписку' для выбора тарифа.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb
        )


# ============ СТАРТ ============

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    name = update.effective_user.full_name

    await update.message.reply_text(
        f"👋 **Привет, {name}!**\n\n"
        f"Добро пожаловать в **Гонзо Бота**! 🦍\n\n"
        f"{BOT_INFO}",
        parse_mode=ParseMode.MARKDOWN
    )

    photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image.jpg")
    try:
        with open(photo_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo,
                                             caption=f"🦍 Гонзо Бот готов к работе!")
    except FileNotFoundError:
        pass

    kb = ReplyKeyboardMarkup([
        ["📂 ЕГЭ", "🧮 Математика", "📅 Дата"],
        ["🎙️ Голос", "📋 Задачи", "📦 Буфер"],
        ["📚 Творчество", "📖 Цитатник", "🔮 Гороскоп/Мем"],
        ["🔄 Рутина", "🔢 Нумерология", "⏰ Уведомления"],
        ["🗒️ Заметки", "⚙️ Настройки", "💳 Купить подписку"],
        ["❌ Выход"]
    ], resize_keyboard=True)

    await update.message.reply_text("📌 **Главное меню**\n\nВыберите раздел:", parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=kb)
    return MAIN_MENU


async def cmd_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    kb = ReplyKeyboardMarkup([
        ["📂 ЕГЭ", "🧮 Математика", "📅 Дата"],
        ["🎙️ Голос", "📋 Задачи", "📦 Буфер"],
        ["📚 Творчество", "📖 Цитатник", "🔮 Гороскоп/Мем"],
        ["🔄 Рутина", "🔢 Нумерология", "⏰ Уведомления"],
        ["🗒️ Заметки", "⚙️ Настройки", "💳 Купить подписку"],
        ["❌ Выход"]
    ], resize_keyboard=True)
    await update.message.reply_text("📌 Главное меню:", reply_markup=kb)
    return MAIN_MENU


async def go_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    kb = ReplyKeyboardMarkup([
        ["📂 ЕГЭ", "🧮 Математика", "📅 Дата"],
        ["🎙️ Голос", "📋 Задачи", "📦 Буфер"],
        ["📚 Творчество", "📖 Цитатник", "🔮 Гороскоп/Мем"],
        ["🔄 Рутина", "🔢 Нумерология", "⏰ Уведомления"],
        ["🗒️ Заметки", "⚙️ Настройки", "💳 Купить подписку"],
        ["❌ Выход"]
    ], resize_keyboard=True)
    await update.message.reply_text("📌 Главное меню:", reply_markup=kb)
    return MAIN_MENU


# ============ ГЛАВНОЕ МЕНЮ ============
# ============ МАТЕМАТИКА ============

async def show_math_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    uid = update.effective_user.id
    has_advanced = payment_system.has_feature(uid, "MATH_ADV")

    kb_rows = [
        ["√ Корень", "log Логарифм"],
        ["10→2 Двоичная", "📐 Степень"]
    ]

    if has_advanced:
        kb_rows.extend([
            ["📊 Факториал", "🎲 Проценты"],
            ["📈 Среднее", "🔢 НОД/НОК"],
            ["📐 Тригонометрия", "🧮 Комбинаторика"],
            ["📊 Уравнения", "🔢 Системы счисления"]
        ])

    kb_rows.append(["↩️ Назад"])

    kb = ReplyKeyboardMarkup(kb_rows, resize_keyboard=True)

    text = "🧮 **МАТЕМАТИКА**\n\n"
    text += "🔹 **Базовые функции:**\n"
    text += "√ Корень, log Логарифм, Перевод в двоичную, Степень\n\n"

    if has_advanced:
        text += "🔸 **Продвинутые функции (премиум):**\n"
        text += "Факториал, Проценты, Среднее, НОД/НОК\n"
        text += "Тригонометрия, Комбинаторика, Уравнения, Системы счисления\n"
    else:
        text += "🔸 **Продвинутые функции** доступны в премиум-версии\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return MATH_MENU


async def math_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    has_advanced = payment_system.has_feature(uid, "MATH_ADV")

    if t == "↩️ Назад":
        return await go_main(update, context)

    if t == "√ Корень":
        await update.message.reply_text("Введите число:", reply_markup=back_kb())
        return MATH_SQRT
    elif t == "log Логарифм":
        await update.message.reply_text("Основание и число через пробел (напр. 2 8):", reply_markup=back_kb())
        return MATH_LOG
    elif t == "10→2 Двоичная":
        await update.message.reply_text("Введите целое число:", reply_markup=back_kb())
        return MATH_BIN
    elif t == "📐 Степень":
        await update.message.reply_text("Основание и показатель через пробел (напр. 2 10):", reply_markup=back_kb())
        return MATH_POW

    if has_advanced:
        if t == "📊 Факториал":
            await update.message.reply_text("Введите целое число n (n!):", reply_markup=back_kb())
            return MATH_FACTORIAL
        elif t == "🎲 Проценты":
            await update.message.reply_text("Введите: число процент\nНапример: 1000 15", reply_markup=back_kb())
            return MATH_PERCENT
        elif t == "📈 Среднее":
            await update.message.reply_text("Введите числа через пробел:", reply_markup=back_kb())
            return MATH_AVG
        elif t == "🔢 НОД/НОК":
            await update.message.reply_text("Введите два числа через пробел:", reply_markup=back_kb())
            return MATH_GCD_LCM
        elif t == "📐 Тригонометрия":
            await update.message.reply_text("Введите: функция угол\nНапример: sin 30", reply_markup=back_kb())
            return MATH_TRIG
        elif t == "🧮 Комбинаторика":
            await update.message.reply_text("Введите: тип n k\nТипы: p, a, c\nНапример: c 10 3", reply_markup=back_kb())
            return MATH_COMB
        elif t == "📊 Уравнения":
            await update.message.reply_text("Введите a b c для ax²+bx+c=0\nНапример: 1 -3 2", reply_markup=back_kb())
            return MATH_EQ
        elif t == "🔢 Системы счисления":
            await update.message.reply_text("Введите: число из_системы в_систему\nНапример: FF 16 10",
                                            reply_markup=back_kb())
            return MATH_CONVERT

    return MATH_MENU


async def math_sqrt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        n = float(update.message.text)
        if n < 0:
            await update.message.reply_text("❌ Число должно быть >= 0")
            return MATH_SQRT
        await update.message.reply_text(f"√{n} = {math.sqrt(n)}")
    except ValueError:
        await update.message.reply_text("❌ Введите число!")
        return MATH_SQRT
    return await show_math_menu(update, context)


async def math_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError
        base, num = float(parts[0]), float(parts[1])
        if base <= 0 or base == 1 or num <= 0:
            await update.message.reply_text("❌ Некорректные значения!")
            return MATH_LOG
        await update.message.reply_text(f"log_{base}({num}) = {math.log(num, base)}")
    except ValueError:
        await update.message.reply_text("❌ Два числа через пробел!")
        return MATH_LOG
    return await show_math_menu(update, context)


async def math_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        n = int(update.message.text)
        await update.message.reply_text(f"{n}₁₀ = {bin(n)[2:]}₂")
    except ValueError:
        await update.message.reply_text("❌ Введите целое число!")
        return MATH_BIN
    return await show_math_menu(update, context)


async def math_pow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError
        base, exp = float(parts[0]), float(parts[1])
        await update.message.reply_text(f"{base} ^ {exp} = {base ** exp}")
    except ValueError:
        await update.message.reply_text("❌ Два числа через пробел!")
        return MATH_POW
    return await show_math_menu(update, context)


async def math_factorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        n = int(update.message.text)
        if n < 0 or n > 20:
            await update.message.reply_text("❌ Введите число от 0 до 20")
            return MATH_FACTORIAL
        await update.message.reply_text(f"{n}! = {math.factorial(n)}")
    except ValueError:
        await update.message.reply_text("❌ Введите целое число!")
        return MATH_FACTORIAL
    return await show_math_menu(update, context)


async def math_percent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError
        num, percent = float(parts[0]), float(parts[1])
        result = num * percent / 100
        await update.message.reply_text(f"{percent}% от {num} = {result}")
    except ValueError:
        await update.message.reply_text("❌ Введите два числа через пробел!")
        return MATH_PERCENT
    return await show_math_menu(update, context)


async def math_avg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        nums = [float(x) for x in update.message.text.split()]
        if not nums:
            raise ValueError
        avg = sum(nums) / len(nums)
        await update.message.reply_text(f"Среднее: {avg}")
    except ValueError:
        await update.message.reply_text("❌ Введите числа через пробел!")
        return MATH_AVG
    return await show_math_menu(update, context)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


async def math_gcd_lcm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        a, b = map(int, update.message.text.split())
        if a <= 0 or b <= 0:
            await update.message.reply_text("❌ Числа должны быть положительными")
            return MATH_GCD_LCM
        g = gcd(a, b)
        l = lcm(a, b)
        await update.message.reply_text(f"НОД({a}, {b}) = {g}\nНОК({a}, {b}) = {l}")
    except ValueError:
        await update.message.reply_text("❌ Введите два целых числа через пробел!")
        return MATH_GCD_LCM
    return await show_math_menu(update, context)


async def math_trig(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 2:
            raise ValueError
        func, angle_str = parts[0].lower(), parts[1]
        angle = float(angle_str)
        rad = math.radians(angle)

        if func == 'sin':
            result = math.sin(rad)
        elif func == 'cos':
            result = math.cos(rad)
        elif func in ('tan', 'tg'):
            result = math.tan(rad)
        elif func in ('cot', 'ctg'):
            result = 1 / math.tan(rad) if math.tan(rad) != 0 else float('inf')
        else:
            await update.message.reply_text("❌ Используйте: sin, cos, tan, cot")
            return MATH_TRIG

        await update.message.reply_text(f"{func}({angle}°) = {result:.4f}")
    except ValueError:
        await update.message.reply_text("❌ Введите: функция угол\nНапример: sin 30")
        return MATH_TRIG
    return await show_math_menu(update, context)


async def math_comb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 3:
            raise ValueError
        type_c, n, k = parts[0].lower(), int(parts[1]), int(parts[2])

        if k > n:
            await update.message.reply_text("❌ k должно быть ≤ n")
            return MATH_COMB

        if type_c == 'p':
            result = math.factorial(n)
            formula = f"P({n}) = {n}!"
        elif type_c == 'a':
            result = math.factorial(n) // math.factorial(n - k)
            formula = f"A({n},{k}) = {n}!/({n - k})!"
        elif type_c == 'c':
            result = math.factorial(n) // (math.factorial(k) * math.factorial(n - k))
            formula = f"C({n},{k}) = {n}!/({k}!*{n - k}!)"
        else:
            await update.message.reply_text("❌ Тип: p, a, c")
            return MATH_COMB

        await update.message.reply_text(f"{formula}\nРезультат: {result}")
    except ValueError:
        await update.message.reply_text("❌ Введите: тип n k\nНапример: c 10 3")
        return MATH_COMB
    return await show_math_menu(update, context)


async def math_eq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        a, b, c = map(float, update.message.text.split())
        if a == 0:
            if b == 0:
                result = "Нет решений" if c != 0 else "x - любое число"
            else:
                x = -c / b
                result = f"x = {x}"
        else:
            d = b ** 2 - 4 * a * c
            if d < 0:
                result = "Нет действительных корней"
            elif d == 0:
                x = -b / (2 * a)
                result = f"x = {x}"
            else:
                x1 = (-b + math.sqrt(d)) / (2 * a)
                x2 = (-b - math.sqrt(d)) / (2 * a)
                result = f"x₁ = {x1}\nx₂ = {x2}"

        await update.message.reply_text(f"Уравнение: {a}x² + {b}x + {c} = 0\n\n{result}")
    except ValueError:
        await update.message.reply_text("❌ Введите три числа через пробел!")
        return MATH_EQ
    return await show_math_menu(update, context)


async def math_convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_math_menu(update, context)
    try:
        parts = update.message.text.split()
        if len(parts) != 3:
            raise ValueError
        num_str, from_base, to_base = parts[0], int(parts[1]), int(parts[2])

        dec = int(num_str, from_base)

        if to_base == 10:
            result = str(dec)
        elif to_base == 2:
            result = bin(dec)[2:]
        elif to_base == 8:
            result = oct(dec)[2:]
        elif to_base == 16:
            result = hex(dec)[2:].upper()
        else:
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            result = ""
            n = dec
            while n > 0:
                result = digits[n % to_base] + result
                n //= to_base
            result = result or "0"

        await update.message.reply_text(f"{num_str} ({from_base}) = {result} ({to_base})")
    except ValueError:
        await update.message.reply_text("❌ Введите: число из_системы в_систему\nНапример: FF 16 10")
        return MATH_CONVERT
    return await show_math_menu(update, context)


# ============ ЕГЭ ============

async def show_ege_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    kb = ReplyKeyboardMarkup([
        ["📚 Мои предметы", "📊 Общий прогресс"],
        ["⚙️ Настроить предметы", "📅 Даты экзаменов"],
        ["↩️ Назад"]
    ], resize_keyboard=True)
    await update.message.reply_text("📚 **ЕГЭ** — выбери действие:", parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return EGE_SUBJECTS


async def ege_subjects_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад":
        return await go_main(update, context)

    if t == "📚 Мои предметы":
        return await show_my_ege_subjects(update, context)

    elif t == "📊 Общий прогресс":
        if not payment_system.has_feature(uid, "EGE_ALL"):
            return await show_premium_required(update, context, "все предметы ЕГЭ", "EGE_ALL")
        return await show_ege_overall_progress(update, context)

    elif t == "⚙️ Настроить предметы":
        return await show_ege_subjects_settings(update, context)

    elif t == "📅 Даты экзаменов":
        return await show_ege_exam_dates(update, context)

    return EGE_SUBJECTS


async def show_my_ege_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_ege_subjects(update, context)
    uid = update.effective_user.id
    settings = db.get_ege_subjects_settings(uid)

    kb_rows, row = [], []
    for subject, is_active in settings.items():
        if is_active:
            button_text = f"{SUBJECT_EMOJI[subject]} {SUBJECT_NAMES_RU[subject]}"
            row.append(button_text)
            if len(row) == 2:
                kb_rows.append(row)
                row = []

    if row:
        kb_rows.append(row)

    kb_rows.append(["↩️ В меню ЕГЭ"])

    kb = ReplyKeyboardMarkup(kb_rows, resize_keyboard=True)
    await update.message.reply_text("📚 Выбери предмет:", reply_markup=kb)

    context.user_data['ege_mode'] = 'select_subject'
    return EGE_SUBJECT_VIEW


async def show_ege_subjects_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_ege_subjects(update, context)
    uid = update.effective_user.id
    settings = db.get_ege_subjects_settings(uid)

    text = "⚙️ **НАСТРОЙКА ПРЕДМЕТОВ ЕГЭ**\n\n"
    text += "Нажми на предмет, чтобы включить/выключить:\n\n"

    kb_rows, row = [], []
    for subject in sorted(SUBJECT_NAMES_RU.keys(), key=lambda x: SUBJECT_NAMES_RU[x]):
        is_active = settings.get(subject, True)
        status = "✅" if is_active else "❌"
        button_text = f"{status} {SUBJECT_EMOJI[subject]} {SUBJECT_NAMES_RU[subject]}"

        row.append(button_text[:25])
        if len(row) == 2:
            kb_rows.append(row)
            row = []

    if row:
        kb_rows.append(row)

    kb_rows.append(["✅ Готово", "↩️ В меню ЕГЭ"])

    kb = ReplyKeyboardMarkup(kb_rows, resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    context.user_data['ege_mode'] = 'settings'
    return EGE_SUBJECT_VIEW


async def show_ege_overall_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_ege_subjects(update, context)
    uid = update.effective_user.id
    user_progress = db.get_ege(uid)
    settings = db.get_ege_subjects_settings(uid)

    text = "📊 **ОБЩИЙ ПРОГРЕСС ЕГЭ**\n\n"

    total_done, total_tasks = 0, 0
    subject_stats = []

    for subject, is_active in settings.items():
        if not is_active:
            continue

        sp = user_progress.subjects.get(subject, SubjectProgress())
        subject_name = SUBJECT_NAMES_RU.get(subject, subject)
        emoji = SUBJECT_EMOJI.get(subject, "📚")
        total_subj_tasks = TASK_COUNTS.get(subject, 0)
        done = len(sp.completed_tasks)
        in_progress = len(sp.in_progress_tasks)

        total_done += done
        total_tasks += total_subj_tasks

        percentage = ((done + in_progress * 0.5) / total_subj_tasks) * 100 if total_subj_tasks else 0
        exam_date = db.get_exam_date(uid, subject)
        days_left = (exam_date - date.today()).days if exam_date else None

        subject_stats.append({
            'name': subject_name, 'emoji': emoji, 'done': done,
            'in_progress': in_progress, 'total': total_subj_tasks,
            'percentage': percentage, 'days_left': days_left
        })

    if not subject_stats:
        await update.message.reply_text("❌ У тебя не выбрано ни одного предмета!")
        return EGE_SUBJECTS

    subject_stats.sort(key=lambda x: x['percentage'], reverse=True)

    for stat in subject_stats[:10]:
        progress_bar = "█" * int(stat['percentage'] / 5) + "░" * (20 - int(stat['percentage'] / 5))

        text += f"{stat['emoji']} **{stat['name']}**\n"
        text += f"`{progress_bar}` {stat['percentage']:.1f}%\n"
        text += f"✅ {stat['done']}  🔄 {stat['in_progress']}  ❌ {stat['total'] - stat['done'] - stat['in_progress']}\n"

        if stat['days_left'] is not None:
            if stat['days_left'] < 0:
                text += f"⚠️ Экзамен прошёл {abs(stat['days_left'])} дн. назад\n"
            elif stat['days_left'] == 0:
                text += f"🔥 Экзамен СЕГОДНЯ!\n"
            else:
                text += f"⏳ До экзамена: {stat['days_left']} дн.\n"
                remaining = stat['total'] - stat['done']
                if remaining > 0 and stat['days_left'] > 0:
                    per_day = remaining / stat['days_left']
                    text += f"⚡ Нужно делать: **{per_day:.1f}** заданий в день\n"
        text += "\n"

    if total_tasks > 0:
        overall_percentage = (total_done / total_tasks) * 100
        text += "═" * 30 + "\n"
        text += f"📈 **ИТОГО:** {overall_percentage:.1f}% выполнено\n"
        text += f"✅ Заданий: {total_done} из {total_tasks}\n"

    kb = ReplyKeyboardMarkup([["↩️ В меню ЕГЭ"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    return EGE_SUBJECT_VIEW


async def show_ege_exam_dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_ege_subjects(update, context)
    uid = update.effective_user.id
    settings = db.get_ege_subjects_settings(uid)

    text = "📅 **ДАТЫ ЭКЗАМЕНОВ**\n\n"
    text += "Чтобы установить дату, используй:\n"
    text += "`/date_предмет ДД.ММ.ГГГГ`\n"
    text += "Например: `/date_informatics 01.06.2025`\n\n"
    text += "**Текущие даты:**\n"

    has_dates = False
    for subject in sorted(SUBJECT_NAMES_RU.keys(), key=lambda x: SUBJECT_NAMES_RU[x]):
        exam_date = db.get_exam_date(uid, subject)
        subject_name = SUBJECT_NAMES_RU[subject]
        emoji = SUBJECT_EMOJI[subject]

        if exam_date:
            has_dates = True
            days_left = (exam_date - date.today()).days
            days_str = f"(прошло {abs(days_left)} дн.)" if days_left < 0 else f"(осталось {days_left} дн.)"
            text += f"{emoji} {subject_name}: {exam_date.strftime('%d.%m.%Y')} {days_str}\n"
        else:
            if settings.get(subject, True):
                text += f"{emoji} {subject_name}: не установлена ❌\n"

    if not has_dates:
        text += "\n❌ Пока нет установленных дат."

    text += "\n\n✅ После установки даты вернись сюда для обновления"

    kb = ReplyKeyboardMarkup([["↩️ В меню ЕГЭ"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

    return EGE_SUBJECT_VIEW


async def show_ege_subject_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ В меню ЕГЭ":
        return await show_ege_subjects(update, context)

    subject = None
    for key, name in SUBJECT_NAMES_RU.items():
        if t == f"{SUBJECT_EMOJI[key]} {name}":
            subject = key
            break

    if not subject:
        return await show_my_ege_subjects(update, context)

    context.user_data['ege_subject'] = subject
    context.user_data.pop('ege_mode', None)

    uid = update.effective_user.id
    total = TASK_COUNTS[subject]
    sp = db.get_ege(uid).subjects.get(subject, SubjectProgress())
    done = len(sp.completed_tasks)
    prog = len(sp.in_progress_tasks)

    pct = ((done + prog * 0.5) / total) * 100 if total else 0
    filled = int(pct / 5)
    progress_bar = "█" * filled + "░" * (20 - filled)

    text = f"{SUBJECT_EMOJI[subject]} **{SUBJECT_NAMES_RU[subject]}**\n\n"
    text += f"{progress_bar} {pct:.1f}%\n"
    text += f"✅ Завершено: {done}\n"
    text += f"🔄 В процессе: {prog}\n"
    text += f"❌ Осталось: {total - done - prog}\n\n"

    exam_date = db.get_exam_date(uid, subject)
    if exam_date:
        days_left = (exam_date - date.today()).days
        text += f"📅 Экзамен: {exam_date.strftime('%d.%m.%Y')}\n"
        if days_left < 0:
            text += f"⚠️ Экзамен был {abs(days_left)} дн. назад\n"
        elif days_left == 0:
            text += f"🔥 Экзамен СЕГОДНЯ!\n"
        else:
            text += f"⏳ До экзамена: {days_left} дн.\n"
            remaining = total - done
            if remaining > 0 and days_left > 0:
                text += f"⚡ Нужно делать: {remaining / days_left:.1f} заданий в день\n"
    else:
        text += f"📅 Экзамен: не установлен\n"
        text += f"💡 Установи командой /date_{subject}\n\n"

    text += "\n📋 **Задания:**\n"
    for i in range(1, min(11, total + 1)):
        st = db.get_ege_task_status(uid, subject, i)
        text += f"{st.value} {i}. {TASK_NAMES[subject].get(i, f'Задание {i}')}\n"

    if total > 11:
        text += f"... и ещё {total - 11} заданий\n"

    text += "\n💡 Введи номер задания для управления статусом"

    kb = ReplyKeyboardMarkup([
        ["📚 Шпаргалки", "📊 Весь список"],
        ["↩️ В меню ЕГЭ"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return EGE_SUBJECT_VIEW


async def ege_subject_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    for key, name in SUBJECT_NAMES_RU.items():
        if t == f"{SUBJECT_EMOJI[key]} {name}":
            context.user_data['ege_subject'] = key
            context.user_data.pop('ege_mode', None)
            return await show_ege_subject_view(update, context)

    if t == "↩️ В меню ЕГЭ" or t == "↩️ Назад":
        return await show_ege_subjects(update, context)

    mode = context.user_data.get('ege_mode')
    if mode == 'settings':
        for subject, name in SUBJECT_NAMES_RU.items():
            status_emoji = '✅' if db.get_ege_subjects_settings(update.effective_user.id).get(subject, True) else '❌'
            if t == f"{status_emoji} {SUBJECT_EMOJI[subject]} {name}":
                uid = update.effective_user.id
                db.toggle_ege_subject(uid, subject)
                await update.message.reply_text(f"✅ Настройки обновлены")
                return await show_ege_subjects_settings(update, context)

        if t == "✅ Готово":
            context.user_data.pop('ege_mode', None)
            return await show_ege_subjects(update, context)

    if context.user_data.get('ege_subject'):
        if t == "📚 Шпаргалки":
            await update.message.reply_text(
                "Введи номер задания для шпаргалки:",
                reply_markup=back_kb("↩️ Назад к предмету")
            )
            return EGE_CHEATSHEET_INPUT

        if t == "📊 Весь список":
            return await show_full_subject_list(update, context)

        if t.isdigit():
            return await show_ege_task_menu(update, context)

    return await show_my_ege_subjects(update, context)


async def show_full_subject_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_ege_subject_view(update, context)
    subj = context.user_data.get('ege_subject')
    if not subj:
        return await show_my_ege_subjects(update, context)

    uid = update.effective_user.id
    total = TASK_COUNTS[subj]

    text = f"{SUBJECT_EMOJI[subj]} **{SUBJECT_NAMES_RU[subj]}** — полный список:\n\n"

    for i in range(1, total + 1):
        st = db.get_ege_task_status(uid, subj, i)
        text += f"{st.value} {i}. {TASK_NAMES[subj].get(i, f'Задание {i}')}\n"

    text += "\n💡 Введи номер задания для переключения"

    kb = ReplyKeyboardMarkup([["↩️ Назад к предмету"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return EGE_SUBJECT_VIEW


async def ege_cheatsheet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад к предмету":
        return await show_ege_subject_view(update, context)

    if not t.isdigit():
        await update.message.reply_text("❌ Введи номер задания!")
        return EGE_CHEATSHEET_INPUT

    num = int(t)
    subj = context.user_data.get('ege_subject')
    if not subj:
        return await show_my_ege_subjects(update, context)

    total = TASK_COUNTS.get(subj, 0)
    if num < 1 or num > total:
        await update.message.reply_text(f"❌ Задания {num} нет. Всего заданий: {total}")
        return EGE_CHEATSHEET_INPUT

    await update.message.reply_text(f"📚 Шпаргалка для задания {num} в разработке")
    return await show_ege_subject_view(update, context)


async def show_ege_task_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад к предмету":
        return await show_ege_subject_view(update, context)

    if not t.isdigit():
        await update.message.reply_text("❌ Введи номер задания!")
        return EGE_SUBJECT_VIEW

    task_num = int(t)
    subject = context.user_data.get('ege_subject')

    if not subject:
        return await show_my_ege_subjects(update, context)

    total = TASK_COUNTS.get(subject, 0)
    if task_num < 1 or task_num > total:
        await update.message.reply_text(f"❌ Задания {task_num} нет. Всего заданий: {total}")
        return EGE_SUBJECT_VIEW

    context.user_data['current_task'] = task_num

    current_status = db.get_ege_task_status(update.effective_user.id, subject, task_num)
    task_name = TASK_NAMES[subject].get(task_num, f"Задание {task_num}")

    status_text = {
        EgeTaskStatus.NOT_STARTED: "❌ Не начато",
        EgeTaskStatus.IN_PROGRESS: "🔄 В процессе",
        EgeTaskStatus.COMPLETED: "✅ Завершено"
    }

    text = f"📋 **Задание {task_num}**: {task_name}\n\n"
    text += f"Текущий статус: **{status_text[current_status]}**\n\n"
    text += "Выбери новый статус:"

    kb = ReplyKeyboardMarkup([
        ["❌ Не начато", "🔄 В процессе"],
        ["✅ Завершено", "↩️ Назад к предмету"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return EGE_TASK_MENU


async def ege_task_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад к предмету":
        return await show_ege_subject_view(update, context)

    subject = context.user_data.get('ege_subject')
    task_num = context.user_data.get('current_task')

    if not subject or not task_num:
        return await show_my_ege_subjects(update, context)

    uid = update.effective_user.id

    if t == "❌ Не начато":
        sp = db.get_ege(uid).subjects.get(subject)
        if sp:
            sp.completed_tasks.discard(task_num)
            sp.in_progress_tasks.discard(task_num)
            db.save_ege()
        await update.message.reply_text(f"❌ Задание {task_num} отмечено как 'Не начато'")

    elif t == "🔄 В процессе":
        sp = db.get_ege(uid).subjects.get(subject)
        if sp:
            sp.completed_tasks.discard(task_num)
            sp.in_progress_tasks.add(task_num)
            db.save_ege()
        await update.message.reply_text(f"🔄 Задание {task_num} отмечено как 'В процессе'")

    elif t == "✅ Завершено":
        sp = db.get_ege(uid).subjects.get(subject)
        if sp:
            sp.completed_tasks.add(task_num)
            sp.in_progress_tasks.discard(task_num)
            db.save_ege()
        await update.message.reply_text(f"✅ Задание {task_num} отмечено как 'Завершено'")

    else:
        await update.message.reply_text("❌ Выбери статус из кнопок!")
        return EGE_TASK_MENU

    return await show_ege_subject_view(update, context)


# ============ ЗАДАЧИ ============

async def show_tasks_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    kb = ReplyKeyboardMarkup([
        ["📋 Все задачи", "➕ Добавить"],
        ["✅ Завершённые", "⚠️ Просроченные"],
        ["📊 Статистика", "🔧 Управление"],
        ["↩️ Назад"]
    ], resize_keyboard=True)
    await update.message.reply_text("📋 **Менеджер задач**", parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return TASKS_MENU


async def tasks_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    tasks = db.get_tasks(uid)

    if t == "↩️ Назад":
        return await go_main(update, context)
    elif t == "➕ Добавить":
        await update.message.reply_text("Введите название задачи:", reply_markup=back_kb())
        return TASK_ADD_NAME
    elif t == "📋 Все задачи":
        if not tasks.tasks:
            await update.message.reply_text("📋 Задач пока нет.")
            return TASKS_MENU
        text = "📋 **Все задачи:**\n\n"
        for tid, task in sorted(tasks.tasks.items()):
            dl = f" (до {task.deadline.strftime('%d.%m %H:%M')})" if task.deadline else ""
            text += f"#{tid} {task.status.value} {task.name}{dl}\n"
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return TASKS_MENU
    elif t == "✅ Завершённые":
        done = [task for task in tasks.tasks.values() if task.status == TaskStatus.COMPLETED]
        if not done:
            await update.message.reply_text("✅ Нет завершённых задач.")
        else:
            text = "✅ **Завершённые:**\n\n" + "\n".join(f"• {task.name}" for task in done)
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return TASKS_MENU
    elif t == "⚠️ Просроченные":
        overdue = [task for task in tasks.tasks.values() if task.status == TaskStatus.OVERDUE]
        if not overdue:
            await update.message.reply_text("⚠️ Нет просроченных задач.")
        else:
            text = "⚠️ **Просроченные:**\n\n" + "\n".join(f"• {task.name}" for task in overdue)
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return TASKS_MENU
    elif t == "📊 Статистика":
        total = len(tasks.tasks)
        done = sum(1 for task in tasks.tasks.values() if task.status == TaskStatus.COMPLETED)
        prog = sum(1 for task in tasks.tasks.values() if task.status == TaskStatus.IN_PROGRESS)
        over = sum(1 for task in tasks.tasks.values() if task.status == TaskStatus.OVERDUE)
        ns = total - done - prog - over
        await update.message.reply_text(
            f"📊 **Статистика:**\n\nВсего: {total}\n✅ Завершено: {done}\n"
            f"🔄 В процессе: {prog}\n❌ Не начато: {ns}\n⚠️ Просрочено: {over}",
            parse_mode=ParseMode.MARKDOWN
        )
        return TASKS_MENU
    elif t == "🔧 Управление":
        if not tasks.tasks:
            await update.message.reply_text("Задач нет.")
            return TASKS_MENU
        text = "Введите ID задачи для управления:\n\n"
        for tid, task in sorted(tasks.tasks.items()):
            text += f"#{tid} {task.status.value} {task.name}\n"
        await update.message.reply_text(text, reply_markup=back_kb())
        return TASK_MANAGE_SELECT
    return TASKS_MENU


async def task_add_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_tasks_menu(update, context)
    context.user_data['new_task_name'] = update.message.text
    kb = ReplyKeyboardMarkup(
        [["🟢 Низкий", "🟡 Средний"], ["🔴 Высокий", "⚡ Срочный"]],
        resize_keyboard=True)
    await update.message.reply_text("Выберите приоритет:", reply_markup=kb)
    return TASK_ADD_PRIORITY


async def task_add_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pmap = {"🟢 Низкий": TaskPriority.LOW, "🟡 Средний": TaskPriority.MEDIUM,
            "🔴 Высокий": TaskPriority.HIGH, "⚡ Срочный": TaskPriority.URGENT}
    if update.message.text not in pmap:
        await update.message.reply_text("Выберите из кнопок!")
        return TASK_ADD_PRIORITY
    context.user_data['new_task_priority'] = pmap[update.message.text]
    kb = ReplyKeyboardMarkup([["Пропустить"]], resize_keyboard=True)
    await update.message.reply_text("Дедлайн (ДД.ММ.ГГГГ ЧЧ:ММ) или 'Пропустить':", reply_markup=kb)
    return TASK_ADD_DEADLINE


async def task_add_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    deadline = None
    if t.lower() != "пропустить":
        try:
            deadline = datetime.strptime(t, "%d.%m.%Y %H:%M")
        except ValueError:
            await update.message.reply_text("❌ Формат: ДД.ММ.ГГГГ ЧЧ:ММ")
            return TASK_ADD_DEADLINE
    uid = update.effective_user.id
    tasks = db.get_tasks(uid)
    tid = tasks.add_task(
        name=context.user_data.pop('new_task_name'),
        priority=context.user_data.pop('new_task_priority'),
        deadline=deadline)
    db.save_tasks()
    await update.message.reply_text(f"✅ Задача #{tid} создана!")
    return await show_tasks_menu(update, context)


async def task_manage_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_tasks_menu(update, context)
    if not t.lstrip('#').isdigit():
        await update.message.reply_text("Введите ID задачи (число).")
        return TASK_MANAGE_SELECT
    tid = int(t.lstrip('#'))
    uid = update.effective_user.id
    tasks = db.get_tasks(uid)
    task = tasks.tasks.get(tid)
    if not task:
        await update.message.reply_text(f"❌ Задача #{tid} не найдена.")
        return TASK_MANAGE_SELECT
    context.user_data['manage_task_id'] = tid
    dl = task.deadline.strftime('%d.%m.%Y %H:%M') if task.deadline else "нет"
    text = (f"📋 #{tid}: {task.name}\n"
            f"Статус: {task.status.value}\n"
            f"Приоритет: {task.priority.value}\n"
            f"Дедлайн: {dl}")
    kb = ReplyKeyboardMarkup(
        [["▶️ В процесс", "✅ Завершить"], ["🗑️ Удалить", "↩️ Назад"]],
        resize_keyboard=True)
    await update.message.reply_text(text, reply_markup=kb)
    return TASK_MANAGE_ACTION


async def task_manage_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_tasks_menu(update, context)
    uid = update.effective_user.id
    tasks = db.get_tasks(uid)
    tid = context.user_data.get('manage_task_id')
    task = tasks.tasks.get(tid) if tid else None
    if not task:
        return await show_tasks_menu(update, context)
    if t == "▶️ В процесс":
        task.status = TaskStatus.IN_PROGRESS
        db.save_tasks()
        await update.message.reply_text(f"🔄 Задача #{tid} в процессе!")
    elif t == "✅ Завершить":
        task.status = TaskStatus.COMPLETED
        db.save_tasks()
        await update.message.reply_text(f"✅ Задача #{tid} завершена!")
    elif t == "🗑️ Удалить":
        del tasks.tasks[tid]
        db.save_tasks()
        await update.message.reply_text(f"🗑️ Задача #{tid} удалена!")
    return await show_tasks_menu(update, context)


# ============ БУФЕР ============

async def show_buffer_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    kb = ReplyKeyboardMarkup(
        [["👤 Личная инфо", "🔐 Пароли"], ["🎂 Дни рождения", "↩️ Назад"]],
        resize_keyboard=True)
    await update.message.reply_text("📦 **Буфер**", parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return BUFFER_MENU


async def buffer_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await go_main(update, context)
    elif t == "👤 Личная инфо":
        return await show_buffer_personal(update, context)
    elif t == "🔐 Пароли":
        return await show_buffer_passwords(update, context)
    elif t == "🎂 Дни рождения":
        return await show_buffer_birthdays(update, context)
    return BUFFER_MENU


async def show_buffer_personal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_buffer_menu(update, context)
    uid = update.effective_user.id
    buf = db.get_buffer(uid)
    text = "👤 **Личная информация:**\n\n"
    if buf.personal_info:
        for k, v in buf.personal_info.items():
            text += f"• {k}: {v}\n"
    else:
        text += "Пока пусто.\n"
    text += "\nЧтобы добавить, введите: ключ: значение"
    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return BUFFER_PERSONAL


async def buffer_personal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_buffer_menu(update, context)
    if ':' in t:
        key, val = t.split(':', 1)
        uid = update.effective_user.id
        buf = db.get_buffer(uid)
        buf.personal_info[key.strip()] = val.strip()
        db.save_buffer()
        await update.message.reply_text(f"✅ Сохранено: {key.strip()}")
        return await show_buffer_personal(update, context)
    await update.message.reply_text("❌ Формат: ключ: значение")
    return BUFFER_PERSONAL


async def show_buffer_passwords(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_buffer_menu(update, context)
    uid = update.effective_user.id
    buf = db.get_buffer(uid)
    text = "🔐 **Пароли:**\n\n"
    if buf.passwords:
        for i, p in enumerate(buf.passwords, 1):
            text += f"{i}. {p.service} | {p.login} | {p.password}"
            if p.notes:
                text += f" | {p.notes}"
            text += "\n"
    else:
        text += "Пока пусто.\n"
    text += "\nДобавить: сервис | логин | пароль | заметки"
    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return BUFFER_PASSWORDS


async def buffer_passwords_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_buffer_menu(update, context)
    parts = t.split('|')
    if len(parts) < 3:
        await update.message.reply_text("❌ Формат: сервис | логин | пароль | заметки")
        return BUFFER_PASSWORDS
    uid = update.effective_user.id
    buf = db.get_buffer(uid)
    buf.passwords.append(PasswordEntry(
        service=parts[0].strip(), login=parts[1].strip(),
        password=parts[2].strip(), notes=parts[3].strip() if len(parts) > 3 else ""))
    db.save_buffer()
    await update.message.reply_text(f"✅ Пароль для {parts[0].strip()} сохранён!")
    return await show_buffer_passwords(update, context)


async def show_buffer_birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_buffer_menu(update, context)
    uid = update.effective_user.id
    buf = db.get_buffer(uid)
    text = "🎂 **Дни рождения:**\n\n"
    if buf.birthdays:
        today = date.today()
        for b in sorted(buf.birthdays, key=lambda x: (x.date.month, x.date.day)):
            bday = date(today.year, b.date.month, b.date.day)
            if bday < today:
                bday = date(today.year + 1, b.date.month, b.date.day)
            days = (bday - today).days
            text += f"• {b.name}: {b.date.strftime('%d.%m.%Y')}"
            if b.notes:
                text += f" ({b.notes})"
            text += f" — через {days} дн.\n"
    else:
        text += "Пока пусто.\n"
    text += "\nДобавить: имя | ДД.ММ.ГГГГ | заметки"
    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return BUFFER_BIRTHDAYS


async def buffer_birthdays_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_buffer_menu(update, context)
    parts = t.split('|')
    if len(parts) < 2:
        await update.message.reply_text("❌ Формат: имя | ДД.ММ.ГГГГ | заметки")
        return BUFFER_BIRTHDAYS
    try:
        bdate = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()
    except ValueError:
        await update.message.reply_text("❌ Неверная дата!")
        return BUFFER_BIRTHDAYS
    uid = update.effective_user.id
    buf = db.get_buffer(uid)
    buf.birthdays.append(BirthdayEntry(
        name=parts[0].strip(), date=bdate,
        notes=parts[2].strip() if len(parts) > 2 else ""))
    db.save_buffer()
    await update.message.reply_text(f"✅ День рождения {parts[0].strip()} сохранён!")
    return await show_buffer_birthdays(update, context)


# ============ ЦИТАТНИК ============

async def show_quote_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    kb = ReplyKeyboardMarkup(
        [["📖 Случайная", "➕ Добавить"], ["📋 Все цитаты", "🗑️ Удалить"], ["↩️ Назад"]],
        resize_keyboard=True)
    await update.message.reply_text("📖 **Цитатник**", parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return QUOTE_MENU


async def quote_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    quotes = db.get_quotes(uid)

    if t == "↩️ Назад":
        return await go_main(update, context)

    if t == "📖 Случайная":
        q = quotes.get_random()
        if q:
            text = f"📖 **Цитата #{q.id}**\n\n"
            text += f"_{q.text}_\n\n"
            if q.author:
                text += f"— {q.author}"
            if q.date_added:
                text += f"\n📅 {q.date_added.strftime('%d.%m.%Y')}"
        else:
            text = "📖 Цитат пока нет."
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return QUOTE_MENU

    elif t == "➕ Добавить":
        await update.message.reply_text(
            "📝 Введите цитату. Автора через |\nНапример: Быть или не быть | Шекспир",
            reply_markup=back_kb())
        return QUOTE_ADD

    elif t == "📋 Все цитаты":
        if not quotes.quotes:
            await update.message.reply_text("📖 У тебя пока нет цитат. Добавь первую через ➕ Добавить!")
            return QUOTE_MENU

        text = "📋 **Все цитаты:**\n\n"
        for qid, q in sorted(quotes.quotes.items()):
            text += f"#{qid}: {q.text[:50]}...\n"
            if q.author:
                text += f"   — {q.author}\n"

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return QUOTE_MENU

    elif t == "🗑️ Удалить":
        if not quotes.quotes:
            await update.message.reply_text("📖 Удалять нечего.")
            return QUOTE_MENU

        text = "🗑️ **Удаление**\n\nВведи номер цитаты:\n\n"
        for qid, q in sorted(quotes.quotes.items()):
            text += f"#{qid}: {q.text[:30]}...\n"

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_kb())
        return QUOTE_DELETE

    return QUOTE_MENU


async def quote_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_quote_menu(update, context)
    uid = update.effective_user.id
    quotes = db.get_quotes(uid)
    if '|' in t:
        text, author = t.split('|', 1)
        qid = quotes.add_quote(text.strip(), author.strip())
    else:
        qid = quotes.add_quote(t)
    db.save_quotes()
    await update.message.reply_text(f"✅ Цитата #{qid} сохранена!")
    return await show_quote_menu(update, context)


async def quote_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_quote_menu(update, context)
    if not t.isdigit():
        await update.message.reply_text("❌ Введи число!")
        return QUOTE_DELETE
    qid = int(t)
    uid = update.effective_user.id
    quotes = db.get_quotes(uid)
    if qid in quotes.quotes:
        del quotes.quotes[qid]
        db.save_quotes()
        await update.message.reply_text(f"✅ Цитата #{qid} удалена!")
    else:
        await update.message.reply_text(f"❌ Цитата #{qid} не найдена!")
    return await show_quote_menu(update, context)


# ============ ЗАМЕТКИ ============

async def show_notes_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    uid = update.effective_user.id
    notes = db.get_notes(uid)
    text = "🗒️ **Заметки:**\n\n"
    if notes.notes:
        for nid, note in sorted(notes.notes.items()):
            text += f"#{nid}: {note.title} ({note.created_at.strftime('%d.%m')})\n"
        text += "\nВведите ID для просмотра"
    else:
        text += "Пока нет заметок."
    kb = ReplyKeyboardMarkup([["➕ Добавить", "🗑️ Удалить"], ["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return NOTES_MENU


async def notes_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await go_main(update, context)
    if t == "➕ Добавить":
        await update.message.reply_text(
            "Введите заметку: заголовок | текст\nНапример: Идея | Надо сделать",
            reply_markup=back_kb())
        return NOTES_ADD
    if t == "🗑️ Удалить":
        await update.message.reply_text("Введите ID заметки:", reply_markup=back_kb())
        return NOTES_DELETE
    if t.isdigit():
        nid = int(t)
        uid = update.effective_user.id
        notes = db.get_notes(uid)
        note = notes.notes.get(nid)
        if note:
            await update.message.reply_text(
                f"🗒️ #{nid}: {note.title}\n📅 {note.created_at.strftime('%d.%m.%Y %H:%M')}\n\n{note.text}")
        else:
            await update.message.reply_text("❌ Заметка не найдена!")
    return NOTES_MENU


async def notes_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_notes_menu(update, context)
    uid = update.effective_user.id
    notes = db.get_notes(uid)
    if '|' in t:
        title, text = t.split('|', 1)
        nid = notes.add_note(title.strip(), text.strip())
    else:
        nid = notes.add_note("Без названия", t)
    db.save_notes()
    await update.message.reply_text(f"✅ Заметка #{nid} сохранена!")
    return await show_notes_menu(update, context)


async def notes_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await show_notes_menu(update, context)
    if not t.isdigit():
        await update.message.reply_text("Введите число!")
        return NOTES_DELETE
    nid = int(t)
    uid = update.effective_user.id
    notes = db.get_notes(uid)
    if nid in notes.notes:
        del notes.notes[nid]
        db.save_notes()
        await update.message.reply_text(f"✅ Заметка #{nid} удалена!")
    else:
        await update.message.reply_text("❌ Не найдена!")
    return await show_notes_menu(update, context)


# ============ ТВОРЧЕСТВО ============

async def show_creativity_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    kb = ReplyKeyboardMarkup([
        ["🎵 Музыка", "📖 Книги"],
        ["📝 Стихи", "🎨 Картины"],
        ["↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(
        "📚 **ТВОРЧЕСТВО**\n\n"
        "Выберите категорию:\n\n"
        "🎵 **Музыка** — альбомы, треки, тексты, концепты\n"
        "📖 **Книги** — библиотека с рейтингами и жанрами\n"
        "📝 **Стихи** — коллекция стихотворений\n"
        "🎨 **Картины** — галерея произведений искусства",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )
    return CREATIVITY_MENU


async def creativity_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад":
        return await go_main(update, context)
    elif t == "🎵 Музыка":
        return await show_music_menu(update, context)
    elif t == "📖 Книги":
        return await show_books_menu(update, context)
    elif t == "📝 Стихи":
        return await show_poems_menu(update, context)
    elif t == "🎨 Картины":
        return await show_art_menu(update, context)

    return CREATIVITY_MENU


# ============ МУЗЫКА ============

async def show_music_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_creativity_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    text = "🎵 **МУЗЫКАЛЬНАЯ БИБЛИОТЕКА**\n\n"

    if creativity.music_albums:
        text += f"**Всего альбомов:** {len(creativity.music_albums)}\n"
        text += "**Последние добавленные:**\n"

        sorted_albums = sorted(creativity.music_albums.values(), key=lambda x: x.created_at, reverse=True)[:5]
        for album in sorted_albums:
            text += f"• {album.title} — {album.artist} ({album.year}) — {len(album.tracks)} треков\n"
    else:
        text += "У вас пока нет альбомов. Добавьте первый!\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Добавить альбом", "📋 Список альбомов"],
        ["🔍 Поиск", "↩️ Назад в творчество"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_MUSIC_MENU


async def music_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в творчество":
        return await show_creativity_menu(update, context)
    elif t == "➕ Добавить альбом":
        await update.message.reply_text(
            "🎵 **ДОБАВЛЕНИЕ АЛЬБОМА**\n\n"
            "Введите данные в формате:\n"
            "Название | Исполнитель | Год | Жанр\n\n"
            "Например:\n"
            "OK Computer | Radiohead | 1997 | Rock",
            reply_markup=back_kb("↩️ Назад в музыку")
        )
        return CR_MUSIC_ALBUM_ADD
    elif t == "📋 Список альбомов":
        return await show_music_album_list(update, context)
    elif t == "🔍 Поиск":
        await update.message.reply_text(
            "Введите название альбома или исполнителя для поиска:",
            reply_markup=back_kb("↩️ Назад в музыку")
        )
        return CR_MUSIC_SEARCH

    return CR_MUSIC_MENU


async def music_album_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в музыку":
        return await show_music_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 3:
            raise ValueError("Недостаточно данных")

        title = parts[0].strip()
        artist = parts[1].strip()
        year = int(parts[2].strip())
        genre = parts[3].strip() if len(parts) > 3 else ""

        album_id = creativity.add_music_album(title, artist, year, genre)
        db.save_creativity()

        context.user_data['current_album_id'] = album_id

        await update.message.reply_text(
            f"✅ Альбом '{title}' добавлен!\n\n"
            f"Теперь вы можете добавить треки, концепт и обложку.",
            reply_markup=ReplyKeyboardMarkup([
                ["➕ Добавить треки", "📝 Добавить концепт"],
                ["🖼️ Добавить обложку", "✅ Завершить"],
                ["↩️ Назад в музыку"]
            ], resize_keyboard=True)
        )
        return CR_MUSIC_ALBUM_VIEW

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Название | Исполнитель | Год | Жанр"
        )
        return CR_MUSIC_ALBUM_ADD


async def show_music_album_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в музыку":
        return await show_music_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    if not creativity.music_albums:
        await update.message.reply_text("У вас пока нет альбомов.")
        return await show_music_menu(update, context)

    text = "📋 **СПИСОК АЛЬБОМОВ**\n\n"

    sorted_albums = sorted(creativity.music_albums.values(), key=lambda x: x.created_at, reverse=True)

    for album in sorted_albums:
        text += f"**#{album.id}** {album.title} — {album.artist} ({album.year})\n"
        text += f"   Жанр: {album.genre or 'не указан'}, Треков: {len(album.tracks)}\n\n"

    text += "\nВведите ID альбома для просмотра и управления"

    kb = ReplyKeyboardMarkup([
        ["↩️ Назад в музыку"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_MUSIC_LIST


async def music_album_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в музыку":
        return await show_music_menu(update, context)

    if t.isdigit():
        album_id = int(t)
        uid = update.effective_user.id
        creativity = db.get_creativity(uid)

        if album_id in creativity.music_albums:
            context.user_data['current_album_id'] = album_id
            return await show_music_album_detail(update, context)

    await update.message.reply_text("❌ Введите корректный ID альбома")
    return await show_music_album_list(update, context)


async def show_music_album_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        await update.message.reply_text("❌ Альбом не найден")
        return await show_music_menu(update, context)

    album = creativity.music_albums[album_id]

    text = f"🎵 **{album.title}**\n"
    text += f"**Исполнитель:** {album.artist}\n"
    text += f"**Год:** {album.year}\n"
    text += f"**Жанр:** {album.genre or 'не указан'}\n"

    if album.concept:
        text += f"\n**Концепт:** {album.concept}\n"

    if album.cover:
        text += f"**Обложка:** {album.cover}\n"

    text += f"\n**Треки ({len(album.tracks)}):**\n"

    if album.tracks:
        sorted_tracks = sorted(album.tracks.values(), key=lambda x: x.order)
        for track in sorted_tracks:
            text += f"  {track.order + 1}. {track.title} ({track.duration})\n"
            if track.lyrics:
                text += f"     📝 Есть текст\n"
    else:
        text += "  Пока нет треков\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Добавить трек", "📝 Текст трека"],
        ["📝 Концепт", "🖼️ Обложка"],
        ["✏️ Редактировать", "🗑️ Удалить альбом"],
        ["↩️ К списку альбомов"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_MUSIC_ALBUM_VIEW


async def music_album_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    album = creativity.music_albums[album_id]

    if t == "↩️ К списку альбомов":
        return await show_music_album_list(update, context)

    elif t == "➕ Добавить трек":
        await update.message.reply_text(
            "🎵 **ДОБАВЛЕНИЕ ТРЕКА**\n\n"
            "Введите данные в формате:\n"
            "Название | Длительность | Текст (опционально)\n\n"
            "Например:\n"
            "Paranoid Android | 6:23 | Текст песни...",
            reply_markup=back_kb("↩️ К альбому")
        )
        return CR_MUSIC_TRACK_ADD

    elif t == "📝 Текст трека":
        if not album.tracks:
            await update.message.reply_text("❌ Сначала добавьте треки")
            return await show_music_album_detail(update, context)

        text = "📝 **ВЫБОР ТРЕКА ДЛЯ ТЕКСТА**\n\n"
        for track in album.tracks.values():
            text += f"#{track.id}: {track.title}\n"

        text += "\nВведите ID трека:"

        await update.message.reply_text(text, reply_markup=back_kb("↩️ К альбому"))
        return CR_MUSIC_TRACK_EDIT

    elif t == "📝 Концепт":
        await update.message.reply_text(
            "📝 **КОНЦЕПТ АЛЬБОМА**\n\n"
            "Опишите концепцию альбома, идею, историю создания:",
            reply_markup=back_kb("↩️ К альбому")
        )
        return CR_MUSIC_CONCEPT_INPUT

    elif t == "🖼️ Обложка":
        await update.message.reply_text(
            "🖼️ **ОБЛОЖКА АЛЬБОМА**\n\n"
            "Введите ссылку на изображение или опишите обложку:",
            reply_markup=back_kb("↩️ К альбому")
        )
        return CR_MUSIC_COVER_INPUT

    elif t == "✏️ Редактировать":
        await update.message.reply_text(
            "✏️ **РЕДАКТИРОВАНИЕ АЛЬБОМА**\n\n"
            "Введите новые данные в формате:\n"
            "Название | Исполнитель | Год | Жанр",
            reply_markup=back_kb("↩️ К альбому")
        )
        return CR_MUSIC_ALBUM_ADD

    elif t == "🗑️ Удалить альбом":
        del creativity.music_albums[album_id]
        db.save_creativity()
        await update.message.reply_text(f"✅ Альбом '{album.title}' удален")
        return await show_music_album_list(update, context)

    return CR_MUSIC_ALBUM_VIEW


async def music_track_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ К альбому":
        return await show_music_album_detail(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    album = creativity.music_albums[album_id]

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        title = parts[0].strip()
        duration = parts[1].strip()
        lyrics = parts[2].strip() if len(parts) > 2 else ""

        track_id = album.add_track(title, duration, lyrics)
        db.save_creativity()

        await update.message.reply_text(f"✅ Трек '{title}' добавлен!")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Название | Длительность | Текст"
        )
        return CR_MUSIC_TRACK_ADD

    return await show_music_album_detail(update, context)


async def music_track_edit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ К альбому":
        return await show_music_album_detail(update, context)

    if not update.message.text.isdigit():
        await update.message.reply_text("❌ Введите ID трека")
        return CR_MUSIC_TRACK_EDIT

    track_id = int(update.message.text)
    context.user_data['current_track_id'] = track_id

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    album = creativity.music_albums[album_id]

    if track_id not in album.tracks:
        await update.message.reply_text("❌ Трек не найден")
        return CR_MUSIC_TRACK_EDIT

    track = album.tracks[track_id]

    await update.message.reply_text(
        f"📝 **ТЕКСТ ПЕСНИ: {track.title}**\n\n"
        f"Текущий текст:\n{track.lyrics or 'Пусто'}\n\n"
        "Введите новый текст песни:",
        reply_markup=back_kb("↩️ К альбому")
    )
    return CR_MUSIC_LYRICS_INPUT


async def music_lyrics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ К альбому":
        return await show_music_album_detail(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')
    track_id = context.user_data.get('current_track_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    album = creativity.music_albums[album_id]

    if track_id not in album.tracks:
        await update.message.reply_text("❌ Трек не найден")
        return await show_music_album_detail(update, context)

    album.tracks[track_id].lyrics = update.message.text
    db.save_creativity()

    await update.message.reply_text("✅ Текст сохранен!")
    return await show_music_album_detail(update, context)


async def music_concept_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ К альбому":
        return await show_music_album_detail(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    creativity.music_albums[album_id].concept = update.message.text
    db.save_creativity()

    await update.message.reply_text("✅ Концепт сохранен!")
    return await show_music_album_detail(update, context)


async def music_cover_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ К альбому":
        return await show_music_album_detail(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    album_id = context.user_data.get('current_album_id')

    if not album_id or album_id not in creativity.music_albums:
        return await show_music_menu(update, context)

    creativity.music_albums[album_id].cover = update.message.text
    db.save_creativity()

    await update.message.reply_text("✅ Обложка сохранена!")
    return await show_music_album_detail(update, context)


async def music_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в музыку":
        return await show_music_menu(update, context)

    query = update.message.text.lower()
    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    results = []
    for album in creativity.music_albums.values():
        if query in album.title.lower() or query in album.artist.lower():
            results.append(album)

    if not results:
        await update.message.reply_text("❌ Ничего не найдено")
        return await show_music_menu(update, context)

    text = "🔍 **РЕЗУЛЬТАТЫ ПОИСКА**\n\n"
    for album in results:
        text += f"**#{album.id}** {album.title} — {album.artist} ({album.year})\n"
        text += f"   Треков: {len(album.tracks)}\n\n"

    text += "Введите ID альбома для просмотра"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    return CR_MUSIC_LIST


# ============ КНИГИ ============

async def show_books_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_creativity_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    text = "📖 **БИБЛИОТЕКА КНИГ**\n\n"

    if creativity.books:
        text += f"**Всего книг:** {len(creativity.books)}\n"
        text += "**Последние добавленные:**\n"

        sorted_books = sorted(creativity.books.values(), key=lambda x: x.created_at, reverse=True)[:5]
        for book in sorted_books:
            rating_stars = "⭐" * int(book.rating) + "☆" * (5 - int(book.rating))
            text += f"• {book.title} — {book.author} ({book.year}) {rating_stars}\n"
    else:
        text += "У вас пока нет книг. Добавьте первую!\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Добавить книгу", "📋 Список книг"],
        ["🔍 Поиск по автору", "↩️ Назад в творчество"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_BOOKS_MENU


async def books_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в творчество":
        return await show_creativity_menu(update, context)
    elif t == "➕ Добавить книгу":
        await update.message.reply_text(
            "📖 **ДОБАВЛЕНИЕ КНИГИ**\n\n"
            "Введите данные в формате:\n"
            "Название | Автор | Год | Жанр | Страниц | Рейтинг (1-5) | Заметки\n\n"
            "Например:\n"
            "1984 | Джордж Оруэлл | 1949 | Антиутопия | 328 | 5 | Классика",
            reply_markup=back_kb("↩️ Назад в книги")
        )
        return CR_BOOKS_ADD
    elif t == "📋 Список книг":
        return await show_books_list(update, context)
    elif t == "🔍 Поиск по автору":
        await update.message.reply_text(
            "Введите имя автора для поиска:",
            reply_markup=back_kb("↩️ Назад в книги")
        )
        return CR_BOOKS_SEARCH

    return CR_BOOKS_MENU


async def books_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в книги":
        return await show_books_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 3:
            raise ValueError("Недостаточно данных")

        title = parts[0].strip()
        author = parts[1].strip()
        year = int(parts[2].strip())
        genre = parts[3].strip() if len(parts) > 3 else ""
        pages = int(parts[4].strip()) if len(parts) > 4 and parts[4].strip() else 0
        rating = float(parts[5].strip()) if len(parts) > 5 and parts[5].strip() else 0.0
        notes = parts[6].strip() if len(parts) > 6 else ""

        book_id = creativity.add_book(title, author, year, genre, pages, rating, notes)
        db.save_creativity()

        await update.message.reply_text(f"✅ Книга '{title}' добавлена!")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Название | Автор | Год | Жанр | Страниц | Рейтинг | Заметки"
        )
        return CR_BOOKS_ADD

    return await show_books_menu(update, context)


async def show_books_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в книги":
        return await show_books_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    if not creativity.books:
        await update.message.reply_text("У вас пока нет книг.")
        return await show_books_menu(update, context)

    text = "📋 **СПИСОК КНИГ**\n\n"

    sorted_books = sorted(creativity.books.values(), key=lambda x: x.title)

    for book in sorted_books:
        rating_stars = "⭐" * int(book.rating) + "☆" * (5 - int(book.rating))
        text += f"**#{book.id}** {book.title} — {book.author} ({book.year})\n"
        text += f"   Жанр: {book.genre or 'не указан'}, Страниц: {book.pages or '?'}, Рейтинг: {rating_stars}\n\n"

    text += "\nВведите ID книги для просмотра и управления"

    kb = ReplyKeyboardMarkup([
        ["↩️ Назад в книги"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_BOOKS_VIEW


async def books_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в книги":
        return await show_books_menu(update, context)

    if t.isdigit():
        book_id = int(t)
        uid = update.effective_user.id
        creativity = db.get_creativity(uid)

        if book_id in creativity.books:
            book = creativity.books[book_id]

            rating_stars = "⭐" * int(book.rating) + "☆" * (5 - int(book.rating))

            text = f"📖 **{book.title}**\n\n"
            text += f"**Автор:** {book.author}\n"
            text += f"**Год:** {book.year}\n"
            text += f"**Жанр:** {book.genre or 'не указан'}\n"
            text += f"**Страниц:** {book.pages or 'не указано'}\n"
            text += f"**Рейтинг:** {rating_stars}\n\n"

            if book.notes:
                text += f"**Заметки:**\n{book.notes}\n"

            kb = ReplyKeyboardMarkup([
                ["✏️ Редактировать", "🗑️ Удалить"],
                ["↩️ К списку книг"]
            ], resize_keyboard=True)

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

            context.user_data['current_book_id'] = book_id
            return CR_BOOKS_VIEW

    await update.message.reply_text("❌ Введите корректный ID книги")
    return await show_books_list(update, context)


async def books_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ К списку книг":
        return await show_books_list(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    book_id = context.user_data.get('current_book_id')

    if not book_id or book_id not in creativity.books:
        return await show_books_menu(update, context)

    if t == "🗑️ Удалить":
        book = creativity.books[book_id]
        del creativity.books[book_id]
        db.save_creativity()
        await update.message.reply_text(f"✅ Книга '{book.title}' удалена")
        return await show_books_list(update, context)

    elif t == "✏️ Редактировать":
        await update.message.reply_text(
            "✏️ **РЕДАКТИРОВАНИЕ КНИГИ**\n\n"
            "Введите новые данные в формате:\n"
            "Название | Автор | Год | Жанр | Страниц | Рейтинг | Заметки",
            reply_markup=back_kb("↩️ К книге")
        )
        return CR_BOOKS_ADD

    return CR_BOOKS_VIEW


async def books_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в книги":
        return await show_books_menu(update, context)

    author = update.message.text.lower()
    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    results = [book for book in creativity.books.values() if author in book.author.lower()]

    if not results:
        await update.message.reply_text(f"❌ Книги автора '{update.message.text}' не найдены")
        return await show_books_menu(update, context)

    text = f"🔍 **КНИГИ АВТОРА {update.message.text}**\n\n"
    for book in results:
        rating_stars = "⭐" * int(book.rating) + "☆" * (5 - int(book.rating))
        text += f"**#{book.id}** {book.title} ({book.year}) {rating_stars}\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    return await show_books_list(update, context)


# ============ СТИХИ ============

async def show_poems_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_creativity_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    text = "📝 **КОЛЛЕКЦИЯ СТИХОВ**\n\n"

    if creativity.poems:
        text += f"**Всего стихов:** {len(creativity.poems)}\n"
        text += "**Последние добавленные:**\n"

        sorted_poems = sorted(creativity.poems.values(), key=lambda x: x.created_at, reverse=True)[:5]
        for poem in sorted_poems:
            text += f"• {poem.title} — {poem.author} ({poem.year or 'год неизвестен'})\n"
    else:
        text += "У вас пока нет стихов. Добавьте первый!\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Добавить стих", "📋 Список стихов"],
        ["🔍 Поиск по автору", "↩️ Назад в творчество"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_POEMS_MENU


async def poems_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в творчество":
        return await show_creativity_menu(update, context)
    elif t == "➕ Добавить стих":
        await update.message.reply_text(
            "📝 **ДОБАВЛЕНИЕ СТИХА**\n\n"
            "Введите данные в формате:\n"
            "Название | Автор | Год | Текст | Заметки\n\n"
            "Например:\n"
            "Я вас любил | Александр Пушкин | 1829 | Я вас любил: любовь еще, быть может... | Классика",
            reply_markup=back_kb("↩️ Назад в стихи")
        )
        return CR_POEMS_ADD
    elif t == "📋 Список стихов":
        return await show_poems_list(update, context)
    elif t == "🔍 Поиск по автору":
        await update.message.reply_text(
            "Введите имя автора для поиска:",
            reply_markup=back_kb("↩️ Назад в стихи")
        )
        return CR_POEMS_SEARCH

    return CR_POEMS_MENU


async def poems_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в стихи":
        return await show_poems_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 4:
            raise ValueError("Недостаточно данных")

        title = parts[0].strip()
        author = parts[1].strip()
        year = int(parts[2].strip()) if parts[2].strip() else 0
        text = parts[3].strip()
        notes = parts[4].strip() if len(parts) > 4 else ""

        poem_id = creativity.add_poem(title, author, text, year, notes)
        db.save_creativity()

        await update.message.reply_text(f"✅ Стих '{title}' добавлен!")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Название | Автор | Год | Текст | Заметки"
        )
        return CR_POEMS_ADD

    return await show_poems_menu(update, context)


async def show_poems_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в стихи":
        return await show_poems_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    if not creativity.poems:
        await update.message.reply_text("У вас пока нет стихов.")
        return await show_poems_menu(update, context)

    text = "📋 **СПИСОК СТИХОВ**\n\n"

    sorted_poems = sorted(creativity.poems.values(), key=lambda x: x.author)

    for poem in sorted_poems:
        text += f"**#{poem.id}** {poem.title} — {poem.author} ({poem.year or 'год неизвестен'})\n"
        text += f"   {poem.text[:50]}...\n\n"

    text += "\nВведите ID стиха для просмотра полного текста"

    kb = ReplyKeyboardMarkup([
        ["↩️ Назад в стихи"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_POEMS_VIEW


async def poems_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в стихи":
        return await show_poems_menu(update, context)

    if t.isdigit():
        poem_id = int(t)
        uid = update.effective_user.id
        creativity = db.get_creativity(uid)

        if poem_id in creativity.poems:
            poem = creativity.poems[poem_id]

            text = f"📝 **{poem.title}**\n"
            text += f"**Автор:** {poem.author}\n"
            text += f"**Год:** {poem.year or 'неизвестен'}\n\n"
            text += f"{poem.text}\n\n"

            if poem.notes:
                text += f"**Заметки:** {poem.notes}\n"

            kb = ReplyKeyboardMarkup([
                ["🗑️ Удалить", "↩️ К списку стихов"]
            ], resize_keyboard=True)

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

            context.user_data['current_poem_id'] = poem_id
            return CR_POEMS_VIEW

    await update.message.reply_text("❌ Введите корректный ID стиха")
    return await show_poems_list(update, context)


async def poems_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ К списку стихов":
        return await show_poems_list(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    poem_id = context.user_data.get('current_poem_id')

    if not poem_id or poem_id not in creativity.poems:
        return await show_poems_menu(update, context)

    if t == "🗑️ Удалить":
        poem = creativity.poems[poem_id]
        del creativity.poems[poem_id]
        db.save_creativity()
        await update.message.reply_text(f"✅ Стих '{poem.title}' удален")
        return await show_poems_list(update, context)

    return CR_POEMS_VIEW


async def poems_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в стихи":
        return await show_poems_menu(update, context)

    author = update.message.text.lower()
    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    results = [poem for poem in creativity.poems.values() if author in poem.author.lower()]

    if not results:
        await update.message.reply_text(f"❌ Стихи автора '{update.message.text}' не найдены")
        return await show_poems_menu(update, context)

    text = f"🔍 **СТИХИ АВТОРА {update.message.text}**\n\n"
    for poem in results:
        text += f"**#{poem.id}** {poem.title} ({poem.year or 'год неизвестен'})\n"
        text += f"   {poem.text[:50]}...\n\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    return await show_poems_list(update, context)


# ============ КАРТИНЫ ============

async def show_art_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_creativity_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    text = "🎨 **ГАЛЕРЕЯ КАРТИН**\n\n"

    if creativity.artworks:
        text += f"**Всего картин:** {len(creativity.artworks)}\n"
        text += "**Последние добавленные:**\n"

        sorted_art = sorted(creativity.artworks.values(), key=lambda x: x.created_at, reverse=True)[:5]
        for art in sorted_art:
            text += f"• {art.title} — {art.artist} ({art.year})\n"
    else:
        text += "У вас пока нет картин. Добавьте первую!\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Добавить картину", "📋 Список картин"],
        ["↩️ Назад в творчество"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_ART_MENU


async def art_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в творчество":
        return await show_creativity_menu(update, context)
    elif t == "➕ Добавить картину":
        await update.message.reply_text(
            "🎨 **ДОБАВЛЕНИЕ КАРТИНЫ**\n\n"
            "Введите данные в формате:\n"
            "Название | Художник | Год | Техника | Описание | Заметки\n\n"
            "Например:\n"
            "Звездная ночь | Винсент Ван Гог | 1889 | Масло | Ночной пейзаж... | Постимпрессионизм",
            reply_markup=back_kb("↩️ Назад в галерею")
        )
        return CR_ART_ADD
    elif t == "📋 Список картин":
        return await show_art_list(update, context)

    return CR_ART_MENU


async def art_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в галерею":
        return await show_art_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 3:
            raise ValueError("Недостаточно данных")

        title = parts[0].strip()
        artist = parts[1].strip()
        year = int(parts[2].strip())
        technique = parts[3].strip() if len(parts) > 3 else ""
        description = parts[4].strip() if len(parts) > 4 else ""
        notes = parts[5].strip() if len(parts) > 5 else ""

        art_id = creativity.add_artwork(title, artist, year, technique, description, notes)
        db.save_creativity()

        await update.message.reply_text(f"✅ Картина '{title}' добавлена!")

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Название | Художник | Год | Техника | Описание | Заметки"
        )
        return CR_ART_ADD

    return await show_art_menu(update, context)


async def show_art_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад в галерею":
        return await show_art_menu(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)

    if not creativity.artworks:
        await update.message.reply_text("У вас пока нет картин.")
        return await show_art_menu(update, context)

    text = "📋 **СПИСОК КАРТИН**\n\n"

    sorted_art = sorted(creativity.artworks.values(), key=lambda x: x.artist)

    for art in sorted_art:
        text += f"**#{art.id}** {art.title} — {art.artist} ({art.year})\n"
        text += f"   Техника: {art.technique or 'не указана'}\n\n"

    text += "\nВведите ID картины для просмотра деталей"

    kb = ReplyKeyboardMarkup([
        ["↩️ Назад в галерею"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return CR_ART_VIEW


async def art_select_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ Назад в галерею":
        return await show_art_menu(update, context)

    if t.isdigit():
        art_id = int(t)
        uid = update.effective_user.id
        creativity = db.get_creativity(uid)

        if art_id in creativity.artworks:
            art = creativity.artworks[art_id]

            text = f"🎨 **{art.title}**\n\n"
            text += f"**Художник:** {art.artist}\n"
            text += f"**Год:** {art.year}\n"
            text += f"**Техника:** {art.technique or 'не указана'}\n\n"

            if art.description:
                text += f"**Описание:**\n{art.description}\n\n"

            if art.notes:
                text += f"**Заметки:** {art.notes}\n"

            kb = ReplyKeyboardMarkup([
                ["🗑️ Удалить", "↩️ К списку картин"]
            ], resize_keyboard=True)

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)

            context.user_data['current_art_id'] = art_id
            return CR_ART_VIEW

    await update.message.reply_text("❌ Введите корректный ID картины")
    return await show_art_list(update, context)


async def art_detail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text

    if t == "↩️ К списку картин":
        return await show_art_list(update, context)

    uid = update.effective_user.id
    creativity = db.get_creativity(uid)
    art_id = context.user_data.get('current_art_id')

    if not art_id or art_id not in creativity.artworks:
        return await show_art_menu(update, context)

    if t == "🗑️ Удалить":
        art = creativity.artworks[art_id]
        del creativity.artworks[art_id]
        db.save_creativity()
        await update.message.reply_text(f"✅ Картина '{art.title}' удалена")
        return await show_art_list(update, context)

    return CR_ART_VIEW


# ============ ГОЛОС ============

async def show_voice_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    kb = ReplyKeyboardMarkup([["ℹ️ Как работает", "↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(
        "🎙️ **Голос**\n\nОтправьте голосовое сообщение — я переведу в текст!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb)
    return VOICE_MENU


async def voice_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "↩️ Назад":
        return await go_main(update, context)
    if t == "ℹ️ Как работает":
        await update.message.reply_text(
            "1. Отправьте голосовое сообщение\n"
            "2. Бот распознает речь\n"
            "3. Получите текст!\n\n"
            "⚠️ Нужны библиотеки: librosa, soundfile, speech_recognition")
    return VOICE_MENU


async def voice_transcribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.voice:
        return

    msg = await update.message.reply_text("🔄 Распознаю...")
    temp_files = []

    try:
        import speech_recognition
        import librosa
        import soundfile as sf

        file = await update.message.voice.get_file()
        file_bytes = await file.download_as_bytearray()

        temp_ogg = f"temp_{update.effective_chat.id}_{int(time.time())}.ogg"
        temp_wav = f"temp_{update.effective_chat.id}_{int(time.time())}.wav"
        temp_files = [temp_ogg, temp_wav]

        with open(temp_ogg, 'wb') as f:
            f.write(file_bytes)

        audio, sr = librosa.load(temp_ogg, sr=16000)
        sf.write(temp_wav, audio, sr)

        recognizer = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(temp_wav) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ru-RU")

        await msg.delete()
        await update.message.reply_text(f"🎙️ {text}")

    except ImportError:
        await msg.edit_text(
            "❌ Библиотеки для распознавания не установлены.\npip install librosa soundfile SpeechRecognition")
    except Exception as e:
        await msg.edit_text(f"❌ Ошибка: {str(e)}")

    finally:
        for fp in temp_files:
            try:
                if os.path.exists(fp):
                    os.remove(fp)
            except:
                pass


# ============ НАСТРОЙКИ ============

async def show_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)
    uid = update.effective_user.id
    settings = db.get_settings(uid)
    items = [
        ("EGE", "📂 ЕГЭ"), ("MATH", "🧮 Математика"), ("DATE", "📅 Дата"),
        ("VOICE", "🎙️ Голос"), ("TASKS", "📋 Задачи"), ("BUFFER", "📦 Буфер"),
        ("CREATIVITY", "📚 Творчество"), ("QUOTES", "📖 Цитатник"),
        ("HOROSCOPE", "🔮 Гороскоп/Мем"), ("NOTES", "🗒️ Заметки"),
        ("ROUTINE", "🔄 Рутина"), ("NUMEROLOGY", "🔢 Нумерология"),
        ("NOTIFICATIONS", "⏰ Уведомления")
    ]

    text = "⚙️ **Настройки меню**\n\nНажмите на пункт чтобы вкл/выкл:\n\n"
    kb_items = []

    for key, label in items:
        if key in ["TASKS", "BUFFER", "CREATIVITY", "QUOTES", "NOTES", "HOROSCOPE", "ROUTINE", "NUMEROLOGY",
                   "NOTIFICATIONS"]:
            if not payment_system.has_feature(uid, key):
                continue

        on = settings.visible_menu_items.get(key, True)
        status = "✅" if on else "❌"
        text += f"{status} {label}\n"
        kb_items.append(label)

    sub = payment_system.get_user_subscription(uid)
    if sub.get('active', False):
        tariff_name = TARIFFS.get(sub.get('tariff'), {}).get('name', 'Подписка')
        kb_items.append(f"💎 {tariff_name}")
    else:
        kb_items.append("💰 Купить подписку")

    keyboard, row = [], []
    for item in kb_items:
        row.append(item)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append(["✅ Готово"])

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return SETTINGS_MENU


async def settings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "✅ Готово":
        return await go_main(update, context)

    if t == "💰 Купить подписку":
        return await show_payment_menu(update, context)

    if t.startswith("💎"):
        return await cmd_premium_status(update, context)

    mapping = {
        "📂 ЕГЭ": "EGE", "🧮 Математика": "MATH", "📅 Дата": "DATE",
        "🎙️ Голос": "VOICE", "📋 Задачи": "TASKS", "📦 Буфер": "BUFFER",
        "📚 Творчество": "CREATIVITY", "📖 Цитатник": "QUOTES",
        "🔮 Гороскоп/Мем": "HOROSCOPE", "🗒️ Заметки": "NOTES",
        "🔄 Рутина": "ROUTINE", "🔢 Нумерология": "NUMEROLOGY",
        "⏰ Уведомления": "NOTIFICATIONS"
    }

    if t in mapping:
        settings = db.get_settings(uid)
        key = mapping[t]
        settings.visible_menu_items[key] = not settings.visible_menu_items.get(key, True)
        db.save_settings()
        return await show_settings_menu(update, context)

    return SETTINGS_MENU
async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    t = update.message.text
    uid = update.effective_user.id

    if t == "📂 ЕГЭ":
        if payment_system.has_feature(uid, "EGE_ALL"):
            return await show_ege_subjects(update, context)
        else:
            return await show_premium_required(update, context, "все предметы ЕГЭ", "EGE_ALL")

    elif t == "🧮 Математика" or t == "🧮 Математика (база)":
        return await show_math_menu(update, context)

    elif t == "📅 Дата":
        return await show_detailed_date(update, context)

    elif t == "🎙️ Голос":
        return await show_voice_menu(update, context)

    elif t == "📋 Задачи":
        if not payment_system.has_feature(uid, "TASKS"):
            return await show_premium_required(update, context, "Задачи", "TASKS")
        return await show_tasks_menu(update, context)

    elif t == "📦 Буфер":
        if not payment_system.has_feature(uid, "BUFFER"):
            return await show_premium_required(update, context, "Буфер", "BUFFER")
        return await show_buffer_menu(update, context)

    elif t == "📚 Творчество":
        if not payment_system.has_feature(uid, "CREATIVITY"):
            return await show_premium_required(update, context, "Творчество", "CREATIVITY")
        return await show_creativity_menu(update, context)

    elif t == "📖 Цитатник":
        if not payment_system.has_feature(uid, "QUOTES"):
            return await show_premium_required(update, context, "Цитатник", "QUOTES")
        return await show_quote_menu(update, context)

    elif t == "🔮 Гороскоп/Мем":
        if not payment_system.has_feature(uid, "HOROSCOPE"):
            return await show_premium_required(update, context, "Гороскоп/Мем", "HOROSCOPE")
        return await show_horoscope_menu(update, context)

    elif t == "🔄 Рутина":
        if not payment_system.has_feature(uid, "ROUTINE"):
            return await show_premium_required(update, context, "Рутина", "ROUTINE")
        return await show_routine_menu(update, context)

    elif t == "🔢 Нумерология":
        if not payment_system.has_feature(uid, "NUMEROLOGY"):
            return await show_premium_required(update, context, "Нумерология", "NUMEROLOGY")
        return await show_numerology_menu(update, context)

    elif t == "⏰ Уведомления":
        if not payment_system.has_feature(uid, "NOTIFICATIONS"):
            return await show_premium_required(update, context, "Уведомления", "NOTIFICATIONS")
        return await show_notifications_menu(update, context)

    elif t == "🗒️ Заметки":
        if not payment_system.has_feature(uid, "NOTES"):
            return await show_premium_required(update, context, "Заметки", "NOTES")
        return await show_notes_menu(update, context)

    elif t == "💳 Купить подписку":
        return await show_payment_menu(update, context)

    elif t == "⚙️ Настройки":
        return await show_settings_menu(update, context)

    elif t == "❌ Выход":
        await update.message.reply_text("👋 До свидания! /start чтобы вернуться.",
                                        reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    await update.message.reply_text("Выберите пункт меню:")
    return MAIN_MENU


async def show_premium_required(update: Update, context: ContextTypes.DEFAULT_TYPE, feature_name: str,
                                feature_key: str):
    feature_info = PREMIUM_FEATURES.get(feature_key, {})
    price = feature_info.get('price', '?')

    kb = ReplyKeyboardMarkup([
        ["💳 Купить подписку"],
        ["↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(
        f"❌ Функция **{feature_name}** недоступна в вашем тарифе!\n\n"
        f"💎 Можно добавить за +{price}⭐/мес\n"
        f"📦 Или подключи тариф 'Все включено' за 250⭐/мес",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb
    )
    return MAIN_MENU


# ============ ДАТА С РЕКОМЕНДАЦИЯМИ ИЗ РУТИНЫ ============

async def show_detailed_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    uid = update.effective_user.id
    now = datetime.now()
    today = date.today()

    text = "📅 **ГОНЗО ДАТА**\n"
    text += "═" * 30 + "\n\n"

    day_of_year = (now - datetime(now.year, 1, 1)).days + 1
    week_num = now.isocalendar()[1]
    weekday_ru = get_weekday_russian(now.weekday())

    text += f"**🗓️ Сегодня:** {now.strftime('%d.%m.%Y')}\n"
    text += f"**⏰ Время:** {now.strftime('%H:%M:%S')}\n"
    text += f"**📊 День года:** {day_of_year}\n"
    text += f"**📅 Неделя:** {week_num}\n"
    text += f"**📆 День недели:** {weekday_ru}\n\n"

    zodiac = get_zodiac_sign(today.day, today.month)
    text += f"**🔮 Знак зодиака:** {zodiac}\n\n"

    text += "─" * 30 + "\n\n"

    if payment_system.has_feature(uid, "ROUTINE"):
        routine = db.get_routine(uid)
        text += "🔄 **РЕКОМЕНДАЦИИ НА СЕГОДНЯ**\n\n"

        if routine.cigarettes:
            expected = routine.cigarettes.get_today_expected()
            unit = routine.cigarettes.unit

            if "сигарет" in unit:
                hours_between = 24 / expected if expected > 0 else 0
                text += f"🚬 **Курение:** {expected:.1f} {unit}\n"
                text += f"   → Рекомендуется курить каждые **{hours_between:.1f}** часа\n"

                if expected <= 5:
                    text += f"   🎉 Отличный прогресс! Скоро бросишь!\n"
                elif expected <= 10:
                    text += f"   👍 Хороший результат, продолжай снижать\n"
                elif expected <= 20:
                    text += f"   💪 Держись, цель достижима\n"
                else:
                    text += f"   ⚡ Не сдавайся, каждый день важен\n"

            elif "часов" in unit:
                cigarettes_per_day = 24 / expected if expected > 0 else 0
                text += f"🚬 **Курение:** 1 сигарета каждые {expected:.1f} часов\n"
                text += f"   → Это примерно {cigarettes_per_day:.1f} сигарет в день\n"

                if cigarettes_per_day <= 5:
                    text += f"   🎉 Отличный прогресс!\n"
                elif cigarettes_per_day <= 10:
                    text += f"   👍 Хороший результат\n"
                else:
                    text += f"   💪 Продолжай увеличивать интервалы\n"

        if routine.teeth:
            expected = routine.teeth.get_today_expected()
            days_since = (today - routine.teeth.last_updated).days

            if days_since >= expected:
                text += f"🦷 **Чистка зубов:** Нужно почистить!\n"
                text += f"   → Прошло {days_since} дн., норма раз в {expected:.0f} дн.\n"
            else:
                next_day = expected - days_since
                text += f"🦷 **Чистка зубов:** через {next_day} дн.\n"
                text += f"   → План: раз в {expected:.0f} дней\n"

            if expected == 1:
                text += f"   ✨ Ежедневная чистка - отличная привычка!\n"
            elif expected == 2:
                text += f"   👍 Хороший режим\n"

        if routine.bath:
            expected = routine.bath.get_today_expected()
            days_since = (today - routine.bath.last_updated).days

            if days_since >= expected:
                text += f"🚿 **Купание:** Нужно помыться!\n"
                text += f"   → Прошло {days_since} дн., норма раз в {expected:.0f} дн.\n"
            else:
                next_day = expected - days_since
                text += f"🚿 **Купание:** через {next_day} дн.\n"
                text += f"   → План: раз в {expected:.0f} дней\n"

        if routine.money and routine.money.goals:
            goal = routine.money.goals[0]
            days_left = (goal.target_date - today).days
            needed_per_day = (goal.target_value - routine.money.current_amount) / days_left if days_left > 0 else 0
            text += f"💰 **Накопления:** {routine.money.current_amount:.0f}₽ из {goal.target_value:.0f}₽\n"
            text += f"   → Осталось дней: {days_left}, нужно {needed_per_day:.0f}₽/день\n"

            if routine.money.weekly_income > 0:
                can_save = routine.money.weekly_income / 7
                if can_save >= needed_per_day:
                    text += f"   ✅ Цель выполнима с твоим доходом\n"
                else:
                    text += f"   ⚠️ Нужно больше откладывать\n"

        text += "\n" + "─" * 30 + "\n\n"

    if payment_system.has_feature(uid, "EGE_ALL"):
        ege_settings = db.get_ege_subjects_settings(uid)
        active_exams = []

        for subject, is_active in ege_settings.items():
            if is_active:
                exam_date = db.get_exam_date(uid, subject)
                if exam_date:
                    days_left = (exam_date - today).days
                    subject_name = SUBJECT_NAMES_RU.get(subject, subject)
                    emoji = SUBJECT_EMOJI.get(subject, "📚")

                    if days_left < 0:
                        status = f"прошёл {abs(days_left)} дн. назад"
                    elif days_left == 0:
                        status = "**СЕГОДНЯ!** 🔥"
                    else:
                        status = f"осталось {days_left} дн."

                    active_exams.append((days_left, emoji, subject_name, status))

        if active_exams:
            active_exams.sort()
            text += "📚 **Экзамены ЕГЭ:**\n"
            for days_left, emoji, subject_name, status in active_exams[:5]:
                text += f"  • {emoji} {subject_name}: {status}\n"
            text += "\n"

    if payment_system.has_feature(uid, "TASKS"):
        urgent_tasks = db.get_urgent_tasks(uid, days=7)

        if urgent_tasks:
            text += "⚠️ **Горящие задачи:**\n"
            for task in sorted(urgent_tasks, key=lambda x: x.deadline)[:5]:
                days_left = (task.deadline - now).days
                if days_left == 0:
                    deadline_str = "**СЕГОДНЯ!** 🔥"
                elif days_left == 1:
                    deadline_str = "завтра"
                else:
                    deadline_str = f"через {days_left} дн."

                text += f"  • {task.name} — {deadline_str}\n"
            text += "\n"

    if payment_system.has_feature(uid, "QUOTES"):
        quotes = db.get_quotes(uid)
        if quotes.quotes:
            q = quotes.get_random()
            text += "📖 **Цитата дня:**\n"
            text += f"  _\"{q.text}\"_\n"
            if q.author:
                text += f"  — *{q.author}*\n"
            text += "\n"

    if payment_system.has_feature(uid, "HOROSCOPE"):
        text += "🔮 **Гороскоп дня:**\n"
        text += f"  {get_horoscope(zodiac)}\n\n"
        text += "😂 **Мем дня:**\n"
        text += f"  {get_random_meme()}\n"

    text += "\n" + "═" * 30

    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return MAIN_MENU
# ============ РУТИНА ============

async def show_routine_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "🔄 **УПРАВЛЕНИЕ РУТИНОЙ**\n\n"
    text += "Выберите привычку для настройки или отметки:\n\n"

    if routine.cigarettes:
        expected = routine.cigarettes.get_today_expected()
        text += f"🚬 **Курение**\n"
        text += f"   Сегодня норма: {expected:.1f} {routine.cigarettes.unit}\n"
        text += f"   Текущий показатель: {routine.cigarettes.current_value:.1f}\n\n"

    if routine.teeth:
        expected = routine.teeth.get_today_expected()
        days_since = (date.today() - routine.teeth.last_updated).days
        text += f"🦷 **Чистка зубов**\n"
        text += f"   Норма: раз в {expected:.0f} дней\n"
        text += f"   Прошло дней: {days_since}\n\n"

    if routine.bath:
        expected = routine.bath.get_today_expected()
        days_since = (date.today() - routine.bath.last_updated).days
        text += f"🚿 **Купание**\n"
        text += f"   Норма: раз в {expected:.0f} дней\n"
        text += f"   Прошло дней: {days_since}\n\n"

    if routine.money:
        text += f"💰 **Накопления**\n"
        text += f"   Сейчас: {routine.money.current_amount:.0f}₽\n"
        if routine.money.weekly_income:
            text += f"   Доход в неделю: {routine.money.weekly_income:.0f}₽\n"
        if routine.money.goals:
            goal = routine.money.goals[0]
            days_left = (goal.target_date - date.today()).days
            text += f"   Цель: {goal.target_value:.0f}₽ до {goal.target_date.strftime('%d.%m.%Y')}\n"
            text += f"   Осталось дней: {days_left}\n"

    kb = ReplyKeyboardMarkup([
        ["🚬 Курение", "🦷 Чистка зубов"],
        ["🚿 Купание", "💰 Накопления"],
        ["✅ Отметить сегодня", "📊 Статистика"],
        ["➕ Новая цель", "↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_MENU


async def routine_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад":
        return await go_main(update, context)

    elif t == "🚬 Курение":
        return await show_cigarette_menu(update, context)

    elif t == "🦷 Чистка зубов":
        return await show_teeth_menu(update, context)

    elif t == "🚿 Купание":
        return await show_bath_menu(update, context)

    elif t == "💰 Накопления":
        return await show_money_menu(update, context)

    elif t == "✅ Отметить сегодня":
        return await show_checkin_menu(update, context)

    elif t == "📊 Статистика":
        return await show_routine_stats(update, context)

    elif t == "➕ Новая цель":
        return await show_add_goal_menu(update, context)

    return ROUTINE_MENU


# --- КУРЕНИЕ ---

async def show_cigarette_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "🚬 **УПРАВЛЕНИЕ КУРЕНИЕМ**\n\n"

    if routine.cigarettes:
        expected = routine.cigarettes.get_today_expected()
        text += f"**Текущий статус:**\n"
        text += f"• Сегодня норма: {expected:.1f} {routine.cigarettes.unit}\n"
        text += f"• Текущий уровень: {routine.cigarettes.current_value:.1f}\n\n"

        if routine.cigarettes.goals:
            text += "**Активные цели:**\n"
            for g in routine.cigarettes.goals:
                if not g.achieved:
                    days_left = (g.target_date - date.today()).days
                    text += f"• До {g.target_date.strftime('%d.%m.%Y')}: {g.target_value} {g.unit} (осталось {days_left} дн.)\n"
        else:
            text += "**Нет активных целей.** Создайте новую цель для плавного снижения.\n"
    else:
        text += "**Нет данных о курении.** Создайте цель, чтобы начать отслеживание.\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Новая цель", "📝 Текущий уровень"],
        ["✅ Отметить сегодня", "📊 История"],
        ["↩️ Назад в рутину"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_CIGARETTE_SELECT


async def cigarette_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад в рутину":
        return await show_routine_menu(update, context)

    elif t == "➕ Новая цель":
        await update.message.reply_text(
            "🚬 **НОВАЯ ЦЕЛЬ ДЛЯ КУРЕНИЯ**\n\n"
            "Введите данные в формате:\n"
            "цель | дата | единица измерения\n\n"
            "Примеры:\n"
            "• 20 | 31.03.2025 | сигарет в день\n"
            "• 2 | 30.04.2025 | часов на сигарету\n\n"
            "Сейчас вы курите примерно 40 сигарет в день (2 пачки).",
            reply_markup=back_kb()
        )
        return ROUTINE_CIGARETTE_GOAL

    elif t == "📝 Текущий уровень":
        await update.message.reply_text(
            "Введите текущее потребление (например: 35 сигарет в день):",
            reply_markup=back_kb()
        )
        return ROUTINE_CIGARETTE_CURRENT

    elif t == "✅ Отметить сегодня":
        return await show_cigarette_checkin(update, context)

    elif t == "📊 История":
        return await show_cigarette_history(update, context)

    return ROUTINE_CIGARETTE_SELECT


async def show_cigarette_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    if not routine.cigarettes or not routine.cigarettes.history:
        await update.message.reply_text("📊 История пока пуста.")
        return await show_cigarette_menu(update, context)

    text = "📊 **ИСТОРИЯ КУРЕНИЯ**\n\n"

    for check in routine.cigarettes.history[-10:]:
        date_str = check.date.strftime('%d.%m.%Y')
        status = check.status.value if check.status else "❓"
        expected = check.expected_value
        actual = check.actual_value if check.actual_value else "-"
        text += f"{date_str}: {status} План: {expected}, Факт: {actual}\n"

    text += "\n✅ - выполнено, ❌ - провал, ⏭️ - пропущено"

    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_CIGARETTE_SELECT


async def cigarette_goal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_cigarette_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        target_value = float(parts[0].strip())
        target_date = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()
        unit = parts[2].strip() if len(parts) > 2 else HabitUnit.CIGARETTES_PER_DAY.value

        goal = HabitGoal(
            habit_type=HabitType.CIGARETTE.value,
            target_date=target_date,
            target_value=target_value,
            unit=unit
        )

        if not routine.cigarettes:
            routine.cigarettes = HabitState(
                habit_type=HabitType.CIGARETTE.value,
                current_value=40,
                last_updated=date.today(),
                unit=unit
            )

        routine.cigarettes.goals.append(goal)
        db.save_routine()

        await update.message.reply_text(
            f"✅ Цель сохранена!\n\n"
            f"К {target_date.strftime('%d.%m.%Y')} вы хотите достичь {target_value} {unit}.\n"
            f"Я буду рассчитывать плавное снижение каждый день."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: цель | дата | единица\n"
            "Например: 20 | 31.03.2025 | сигарет в день"
        )
        return ROUTINE_CIGARETTE_GOAL

    return await show_routine_menu(update, context)


async def cigarette_current_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_cigarette_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        parts = update.message.text.split()
        value = float(parts[0])
        unit = ' '.join(parts[1:]) if len(parts) > 1 else HabitUnit.CIGARETTES_PER_DAY.value

        if not routine.cigarettes:
            routine.cigarettes = HabitState(
                habit_type=HabitType.CIGARETTE.value,
                current_value=value,
                last_updated=date.today(),
                unit=unit
            )
        else:
            routine.cigarettes.current_value = value
            routine.cigarettes.last_updated = date.today()
            if unit != routine.cigarettes.unit:
                routine.cigarettes.unit = unit

        db.save_routine()

        await update.message.reply_text(f"✅ Текущий уровень обновлен: {value} {unit}")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        return ROUTINE_CIGARETTE_CURRENT

    return await show_routine_menu(update, context)


async def show_cigarette_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    if not routine.cigarettes:
        await update.message.reply_text("Сначала настройте привычку в разделе '🚬 Курение'.")
        return await show_cigarette_menu(update, context)

    expected = routine.cigarettes.get_today_expected()

    text = f"✅ **ОТМЕТКА ЗА СЕГОДНЯ**\n\n"
    text += f"🚬 По плану сегодня: {expected:.1f} {routine.cigarettes.unit}\n\n"
    text += "Сколько вы выкурили сегодня?"

    kb = ReplyKeyboardMarkup([
        [f"{expected:.0f}", f"{expected + 2:.0f}", f"{expected - 2:.0f}"],
        ["⏭️ Пропустить", "↩️ Назад"]
    ], resize_keyboard=True)

    context.user_data['checkin_type'] = 'cigarette'
    context.user_data['expected_value'] = expected

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_CHECKIN


# --- ЧИСТКА ЗУБОВ ---

async def show_teeth_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "🦷 **ЧИСТКА ЗУБОВ**\n\n"

    if routine.teeth:
        expected = routine.teeth.get_today_expected()
        days_since = (date.today() - routine.teeth.last_updated).days

        text += f"**Текущий статус:**\n"
        text += f"• Норма: раз в {expected:.0f} дней\n"
        text += f"• Последний раз: {days_since} дней назад\n\n"

        if days_since >= expected:
            text += "⚠️ **Нужно почистить зубы сегодня!**\n\n"

        if routine.teeth.goals:
            text += "**Цели:**\n"
            for g in routine.teeth.goals:
                if not g.achieved:
                    text += f"• Достичь частоты раз в {g.target_value:.0f} дней до {g.target_date.strftime('%d.%m.%Y')}\n"
    else:
        text += "**Нет данных.** Создайте цель, чтобы начать отслеживание.\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Новая цель", "✅ Отметить чистку"],
        ["📝 Установить частоту", "📊 История"],
        ["↩️ Назад в рутину"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_HABIT_SELECT


async def teeth_goal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_teeth_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        target_value = float(parts[0].strip())
        target_date = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()

        goal = HabitGoal(
            habit_type=HabitType.TEETH.value,
            target_date=target_date,
            target_value=target_value,
            unit=HabitUnit.DAYS.value
        )

        if not routine.teeth:
            routine.teeth = HabitState(
                habit_type=HabitType.TEETH.value,
                current_value=2,
                last_updated=date.today() - timedelta(days=1),
                unit=HabitUnit.DAYS.value
            )

        routine.teeth.goals.append(goal)
        db.save_routine()

        await update.message.reply_text(
            f"✅ Цель сохранена!\n\n"
            f"К {target_date.strftime('%d.%m.%Y')} вы будете чистить зубы раз в {target_value:.0f} дней."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: частота | дата\n"
            "Например: 1 | 30.04.2025"
        )
        return ROUTINE_TEETH_GOAL

    return await show_routine_menu(update, context)


async def teeth_current_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_teeth_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        value = float(update.message.text)

        if not routine.teeth:
            routine.teeth = HabitState(
                habit_type=HabitType.TEETH.value,
                current_value=value,
                last_updated=date.today() - timedelta(days=value),
                unit=HabitUnit.DAYS.value
            )
        else:
            routine.teeth.current_value = value

        db.save_routine()

        await update.message.reply_text(f"✅ Частота обновлена: раз в {value:.0f} дней")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        return ROUTINE_TEETH_LAST

    return await show_routine_menu(update, context)


async def teeth_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    if not routine.teeth:
        await update.message.reply_text("Сначала настройте привычку.")
        return await show_teeth_menu(update, context)

    routine.teeth.last_updated = date.today()
    expected = routine.teeth.get_today_expected()
    routine.teeth.add_check(expected, 1, CheckStatus.DONE)
    db.save_routine()

    await update.message.reply_text("✅ Отмечено! Зубы почищены.")
    return await show_teeth_menu(update, context)


# --- КУПАНИЕ ---

async def show_bath_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "🚿 **КУПАНИЕ**\n\n"

    if routine.bath:
        expected = routine.bath.get_today_expected()
        days_since = (date.today() - routine.bath.last_updated).days

        text += f"**Текущий статус:**\n"
        text += f"• Норма: раз в {expected:.0f} дней\n"
        text += f"• Последний раз: {days_since} дней назад\n\n"

        if days_since >= expected:
            text += "⚠️ **Нужно помыться сегодня!**\n\n"

        if routine.bath.goals:
            text += "**Цели:**\n"
            for g in routine.bath.goals:
                if not g.achieved:
                    text += f"• Достичь частоты раз в {g.target_value:.0f} дней до {g.target_date.strftime('%d.%m.%Y')}\n"
    else:
        text += "**Нет данных.** Создайте цель, чтобы начать отслеживание.\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Новая цель", "✅ Отметить купание"],
        ["📝 Установить частоту", "📊 История"],
        ["↩️ Назад в рутину"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_HABIT_SELECT


async def bath_goal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_bath_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        target_value = float(parts[0].strip())
        target_date = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()

        goal = HabitGoal(
            habit_type=HabitType.BATH.value,
            target_date=target_date,
            target_value=target_value,
            unit=HabitUnit.DAYS.value
        )

        if not routine.bath:
            routine.bath = HabitState(
                habit_type=HabitType.BATH.value,
                current_value=3,
                last_updated=date.today() - timedelta(days=2),
                unit=HabitUnit.DAYS.value
            )

        routine.bath.goals.append(goal)
        db.save_routine()

        await update.message.reply_text(
            f"✅ Цель сохранена!\n\n"
            f"К {target_date.strftime('%d.%m.%Y')} вы будете мыться раз в {target_value:.0f} дней."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: частота | дата\n"
            "Например: 1 | 30.04.2025"
        )
        return ROUTINE_BATH_GOAL

    return await show_routine_menu(update, context)


async def bath_current_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_bath_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        value = float(update.message.text)

        if not routine.bath:
            routine.bath = HabitState(
                habit_type=HabitType.BATH.value,
                current_value=value,
                last_updated=date.today() - timedelta(days=value),
                unit=HabitUnit.DAYS.value
            )
        else:
            routine.bath.current_value = value

        db.save_routine()

        await update.message.reply_text(f"✅ Частота обновлена: раз в {value:.0f} дней")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")
        return ROUTINE_BATH_LAST

    return await show_routine_menu(update, context)


async def bath_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    if not routine.bath:
        await update.message.reply_text("Сначала настройте привычку.")
        return await show_bath_menu(update, context)

    routine.bath.last_updated = date.today()
    expected = routine.bath.get_today_expected()
    routine.bath.add_check(expected, 1, CheckStatus.DONE)
    db.save_routine()

    await update.message.reply_text("✅ Отмечено! Помылись.")
    return await show_bath_menu(update, context)


# --- ДЕНЬГИ ---

async def show_money_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "💰 **УПРАВЛЕНИЕ НАКОПЛЕНИЯМИ**\n\n"

    if routine.money:
        text += f"**Текущий баланс:** {routine.money.current_amount:.0f}₽\n"
        if routine.money.weekly_income:
            text += f"**Доход в неделю:** {routine.money.weekly_income:.0f}₽\n\n"

        if routine.money.goals:
            text += "**Активные цели:**\n"
            for g in routine.money.goals:
                if not g.achieved:
                    days_left = (g.target_date - date.today()).days
                    needed = (g.target_value - routine.money.current_amount) / days_left if days_left > 0 else 0
                    text += f"• {g.target_value:.0f}₽ до {g.target_date.strftime('%d.%m.%Y')}\n"
                    text += f"  Осталось дней: {days_left}, нужно {needed:.0f}₽/день\n\n"
        else:
            text += "**Нет активных целей.** Создайте цель для накопления.\n"
    else:
        text += "**Нет данных.** Создайте цель, чтобы начать отслеживание.\n"

    kb = ReplyKeyboardMarkup([
        ["➕ Новая цель", "💰 Пополнить"],
        ["📝 Доход", "📊 Статистика"],
        ["↩️ Назад в рутину"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_HABIT_SELECT


async def money_goal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_money_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        target_value = float(parts[0].strip())
        target_date = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()

        goal = HabitGoal(
            habit_type=HabitType.MONEY.value,
            target_date=target_date,
            target_value=target_value,
            unit=HabitUnit.RUBLES.value
        )

        if not routine.money:
            routine.money = MoneyState()

        routine.money.goals.append(goal)
        db.save_routine()

        await update.message.reply_text(
            f"✅ Цель сохранена!\n\n"
            f"К {target_date.strftime('%d.%m.%Y')} вы накопите {target_value:.0f}₽."
        )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: сумма | дата\n"
            "Например: 50000 | 31.12.2025"
        )
        return ROUTINE_MONEY_GOAL

    return await show_routine_menu(update, context)


async def money_add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_money_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        amount = float(update.message.text)

        if not routine.money:
            routine.money = MoneyState()

        routine.money.current_amount += amount
        routine.money.transactions.append({
            "date": date.today().isoformat(),
            "amount": amount,
            "type": "income"
        })

        db.save_routine()

        await update.message.reply_text(f"✅ Добавлено {amount}₽. Текущий баланс: {routine.money.current_amount:.0f}₽")

    except ValueError:
        await update.message.reply_text("❌ Введите число (сумму в рублях)")
        return ROUTINE_MONEY_DATE

    return await show_money_menu(update, context)


async def money_income_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_money_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    try:
        income = float(update.message.text)

        if not routine.money:
            routine.money = MoneyState()

        routine.money.weekly_income = income
        db.save_routine()

        await update.message.reply_text(f"✅ Доход установлен: {income}₽ в неделю")

    except ValueError:
        await update.message.reply_text("❌ Введите число (доход в рублях в неделю)")
        return ROUTINE_MONEY_INCOME

    return await show_money_menu(update, context)


# --- ОБЩИЕ ФУНКЦИИ ---

async def show_checkin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "✅ **ОТМЕТКА ЗА СЕГОДНЯ**\n\n"
    text += "Выберите, что отметить:\n"

    kb = ReplyKeyboardMarkup([
        ["🚬 Курение", "🦷 Чистка зубов"],
        ["🚿 Купание", "💰 Накопления"],
        ["↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_CHECKIN


async def checkin_value_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    uid = update.effective_user.id
    routine = db.get_routine(uid)

    checkin_type = context.user_data.get('checkin_type')
    expected = context.user_data.get('expected_value')

    try:
        if update.message.text == "⏭️ Пропустить":
            actual = None
            status = CheckStatus.SKIPPED
        else:
            actual = float(update.message.text)
            if checkin_type == 'cigarette':
                if actual <= expected:
                    status = CheckStatus.DONE
                else:
                    status = CheckStatus.FAILED
            else:
                status = CheckStatus.DONE

        if checkin_type == 'cigarette' and routine.cigarettes:
            routine.cigarettes.add_check(expected, actual, status)
            db.save_routine()

            if status == CheckStatus.DONE:
                await update.message.reply_text(f"✅ Молодец! Ты выполнил план ({actual} {routine.cigarettes.unit})")
            elif status == CheckStatus.FAILED:
                new_expected = (expected + actual) / 2
                await update.message.reply_text(
                    f"❌ Не выполнил план. Новая норма на завтра: {new_expected:.1f} {routine.cigarettes.unit}\n"
                    f"Не сдавайся! Каждая неудача приближает к успеху."
                )
            else:
                await update.message.reply_text("⏭️ Пропущено")

    except ValueError:
        await update.message.reply_text("❌ Введите число")
        return ROUTINE_CHECKIN

    return await show_routine_menu(update, context)


async def show_routine_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    routine = db.get_routine(uid)

    text = "📊 **СТАТИСТИКА РУТИНЫ**\n\n"

    if routine.cigarettes and routine.cigarettes.history:
        text += "🚬 **Курение**\n"
        last_7 = routine.cigarettes.history[-7:]
        success_rate = sum(1 for h in last_7 if h.status == CheckStatus.DONE) / len(last_7) * 100
        text += f"• Выполнение за 7 дней: {success_rate:.0f}%\n"
        avg = sum(h.actual_value for h in last_7 if h.actual_value) / len([h for h in last_7 if h.actual_value]) if any(
            h.actual_value for h in last_7) else 0
        text += f"• Среднее за 7 дней: {avg:.1f} {routine.cigarettes.unit}\n\n"

    if routine.teeth and routine.teeth.history:
        text += "🦷 **Чистка зубов**\n"
        total_days = (date.today() - routine.teeth.history[0].date).days if routine.teeth.history else 0
        cleanings = len([h for h in routine.teeth.history if h.status == CheckStatus.DONE])
        text += f"• Всего чисток: {cleanings}\n"
        if cleanings > 0:
            text += f"• Средняя частота: раз в {total_days / cleanings:.1f} дней\n\n"

    if routine.money:
        text += "💰 **Накопления**\n"
        text += f"• Текущий баланс: {routine.money.current_amount:.0f}₽\n"
        if routine.money.goals:
            goal = routine.money.goals[0]
            progress = (routine.money.current_amount / goal.target_value) * 100
            text += f"• Прогресс к цели: {progress:.1f}%\n"

    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_MENU


async def show_add_goal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_routine_menu(update, context)

    text = "➕ **НОВАЯ ЦЕЛЬ**\n\n"
    text += "Выберите тип привычки:\n"

    kb = ReplyKeyboardMarkup([
        ["🚬 Курение", "🦷 Чистка зубов"],
        ["🚿 Купание", "💰 Накопления"],
        ["↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return ROUTINE_HABIT_SELECT


# ============ НУМЕРОЛОГИЯ ============

ARCANA_MEANINGS = {
    1: "Маг — начало, инициатива, лидерство, уверенность",
    2: "Верховная Жрица — интуиция, тайна, знания, мудрость",
    3: "Императрица — плодородие, творчество, изобилие, забота",
    4: "Император — власть, структура, порядок, авторитет",
    5: "Иерофант — традиции, обучение, духовность, наставничество",
    6: "Влюбленные — выбор, отношения, любовь, гармония",
    7: "Колесница — движение, контроль, воля, победа",
    8: "Сила — внутренняя сила, мужество, терпение, страсть",
    9: "Отшельник — мудрость, уединение, поиск истины",
    10: "Колесо Фортуны — удача, циклы, судьба, перемены",
    11: "Справедливость — баланс, правда, закон, карма",
    12: "Повешенный — жертва, новый взгляд, ожидание",
    13: "Смерть — трансформация, окончание, новое начало",
    14: "Умеренность — баланс, гармония, умеренность",
    15: "Дьявол — искушение, материализм, зависимость",
    16: "Башня — разрушение, кризис, освобождение",
    17: "Звезда — надежда, вдохновение, мечты",
    18: "Луна — иллюзии, страхи, интуиция",
    19: "Солнце — успех, радость, процветание",
    20: "Суд — возрождение, прощение, оценка",
    21: "Мир — завершение, целостность, путешествия",
    22: "Шут — новое начало, спонтанность, доверие"
}


async def show_numerology_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    uid = update.effective_user.id
    numerology = db.get_numerology(uid)

    buffer = db.get_buffer(uid)
    numerology.sync_with_buffer(buffer)
    db.save_numerology()

    text = "🔢 **НУМЕРОЛОГИЯ**\n\n"
    text += "Рассчитайте свои арканы по дате рождения или проверьте совместимость.\n\n"

    if numerology.history:
        text += "**Недавно просмотренные:**\n"
        for name in numerology.history[-5:]:
            profile = numerology.get_profile(name)
            if profile:
                text += f"• {name} — личный аркан: {profile.arcana.get('personality', '?')}\n"
        text += "\n"

    kb = ReplyKeyboardMarkup([
        ["🔢 Рассчитать арканы", "❤️ Совместимость"],
        ["📋 Список людей", "↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return NUMEROLOGY_MENU


async def numerology_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id

    if t == "↩️ Назад":
        return await go_main(update, context)

    elif t == "🔢 Рассчитать арканы":
        await update.message.reply_text(
            "🔢 **ВВЕДИТЕ ДАТУ РОЖДЕНИЯ**\n\n"
            "Формат: Имя | ДД.ММ.ГГГГ\n\n"
            "Например:\n"
            "Артур | 15.06.1995",
            reply_markup=back_kb()
        )
        return NUMEROLOGY_INPUT

    elif t == "❤️ Совместимость":
        numerology = db.get_numerology(uid)

        if len(numerology.profiles) < 2:
            await update.message.reply_text(
                "❌ Нужно минимум 2 человека для расчета совместимости.\n"
                "Сначала добавьте людей через '🔢 Рассчитать арканы'."
            )
            return NUMEROLOGY_MENU

        text = "❤️ **ВЫБЕРИТЕ ПЕРВОГО ЧЕЛОВЕКА**\n\n"
        for name in numerology.profiles.keys():
            text += f"• {name}\n"

        text += "\nВведите имя первого человека:"

        await update.message.reply_text(text, reply_markup=back_kb())
        context.user_data['compatibility_step'] = 'first'
        return NUMEROLOGY_COMPATIBILITY

    elif t == "📋 Список людей":
        return await show_numerology_people_list(update, context)

    return NUMEROLOGY_MENU


async def numerology_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_numerology_menu(update, context)

    uid = update.effective_user.id
    numerology = db.get_numerology(uid)

    try:
        parts = update.message.text.split('|')
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")

        name = parts[0].strip()
        birth_date = datetime.strptime(parts[1].strip(), "%d.%m.%Y").date()

        profile = numerology.add_profile(name, birth_date)
        db.save_numerology()

        text = f"🔢 **АРКАНЫ {name}**\n\n"
        text += f"📅 Дата рождения: {birth_date.strftime('%d.%m.%Y')}\n\n"

        text += f"**Личный аркан:** {profile.arcana['personality']}\n"
        text += f"_{ARCANA_MEANINGS[profile.arcana['personality']]}_\n\n"

        text += f"**Аркан души:** {profile.arcana['soul']}\n"
        text += f"_{ARCANA_MEANINGS[profile.arcana['soul']]}_\n\n"

        text += f"**Аркан роста:** {profile.arcana['growth']}\n"
        text += f"_{ARCANA_MEANINGS[profile.arcana['growth']]}_\n\n"

        text += f"**Аркан года:** {profile.arcana['year']}\n"
        text += f"_{ARCANA_MEANINGS[profile.arcana['year']]}_\n\n"

        text += f"**Аркан дня:** {profile.arcana['day']}\n"
        text += f"_{ARCANA_MEANINGS[profile.arcana['day']]}_\n"

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка: {str(e)}\n\n"
            "Используйте формат: Имя | ДД.ММ.ГГГГ"
        )
        return NUMEROLOGY_INPUT

    return await show_numerology_menu(update, context)


async def show_numerology_people_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_numerology_menu(update, context)

    uid = update.effective_user.id
    numerology = db.get_numerology(uid)

    if not numerology.profiles:
        await update.message.reply_text("📋 Список людей пуст. Добавьте первого через '🔢 Рассчитать арканы'.")
        return await show_numerology_menu(update, context)

    text = "📋 **СПИСОК ЛЮДЕЙ**\n\n"

    for name, profile in numerology.profiles.items():
        text += f"**{name}**\n"
        text += f"📅 {profile.birth_date.strftime('%d.%m.%Y')}\n"
        text += f"🔢 Личный аркан: {profile.arcana.get('personality', '?')}\n"
        text += f"🔄 Аркан года: {profile.arcana.get('year', '?')}\n\n"

    text += "Введите имя для просмотра полных арканов"

    kb = ReplyKeyboardMarkup([["↩️ Назад"]], resize_keyboard=True)
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return NUMEROLOGY_VIEW


async def numerology_view_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_numerology_menu(update, context)

    name = update.message.text.strip()
    uid = update.effective_user.id
    numerology = db.get_numerology(uid)

    profile = numerology.get_profile(name)
    if not profile:
        await update.message.reply_text(f"❌ Человек с именем '{name}' не найден.")
        return await show_numerology_people_list(update, context)

    text = f"🔢 **АРКАНЫ {name}**\n\n"
    text += f"📅 Дата рождения: {profile.birth_date.strftime('%d.%m.%Y')}\n\n"

    text += f"**Личный аркан:** {profile.arcana['personality']}\n"
    text += f"_{ARCANA_MEANINGS[profile.arcana['personality']]}_\n\n"

    text += f"**Аркан души:** {profile.arcana['soul']}\n"
    text += f"_{ARCANA_MEANINGS[profile.arcana['soul']]}_\n\n"

    text += f"**Аркан роста:** {profile.arcana['growth']}\n"
    text += f"_{ARCANA_MEANINGS[profile.arcana['growth']]}_\n\n"

    text += f"**Аркан года:** {profile.arcana['year']}\n"
    text += f"_{ARCANA_MEANINGS[profile.arcana['year']]}_\n\n"

    text += f"**Аркан дня:** {profile.arcana['day']}\n"
    text += f"_{ARCANA_MEANINGS[profile.arcana['day']]}_\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    return await show_numerology_people_list(update, context)


async def numerology_compatibility_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        context.user_data.pop('compatibility_step', None)
        return await show_numerology_menu(update, context)

    uid = update.effective_user.id
    numerology = db.get_numerology(uid)
    step = context.user_data.get('compatibility_step')

    if step == 'first':
        name1 = update.message.text.strip()
        if name1 not in numerology.profiles:
            await update.message.reply_text(f"❌ Человек '{name1}' не найден. Введите имя из списка.")
            return NUMEROLOGY_COMPATIBILITY

        context.user_data['compat_name1'] = name1
        context.user_data['compatibility_step'] = 'second'

        text = "❤️ **ВЫБЕРИТЕ ВТОРОГО ЧЕЛОВЕКА**\n\n"
        for name in numerology.profiles.keys():
            if name != name1:
                text += f"• {name}\n"

        text += "\nВведите имя второго человека:"

        await update.message.reply_text(text)
        return NUMEROLOGY_COMPATIBILITY

    elif step == 'second':
        name2 = update.message.text.strip()
        name1 = context.user_data.get('compat_name1')

        if name2 not in numerology.profiles:
            await update.message.reply_text(f"❌ Человек '{name2}' не найден. Введите имя из списка.")
            return NUMEROLOGY_COMPATIBILITY

        compatibility = numerology.get_compatibility(name1, name2)

        if compatibility:
            text = f"❤️ **СОВМЕСТИМОСТЬ: {name1} и {name2}**\n\n"

            text += f"**Личная совместимость:** {compatibility.get('personality', 0)}%\n"
            text += f"**Совместимость душ:** {compatibility.get('soul', 0)}%\n"
            text += f"**Совместимость роста:** {compatibility.get('growth', 0)}%\n"
            text += f"**Годовая совместимость:** {compatibility.get('year', 0)}%\n"
            text += f"**Дневная совместимость:** {compatibility.get('day', 0)}%\n\n"

            total = compatibility.get('total', 0)
            text += f"**ОБЩАЯ СОВМЕСТИМОСТЬ: {total}%**\n\n"

            if total >= 80:
                text += "✨ Идеальная совместимость! Вы созданы друг для друга!"
            elif total >= 60:
                text += "💫 Хорошая совместимость. Есть все шансы на гармоничные отношения."
            elif total >= 40:
                text += "⭐ Средняя совместимость. Над отношениями нужно работать."
            else:
                text += "⚠️ Низкая совместимость. Возможны конфликты и непонимание."

            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

        context.user_data.pop('compatibility_step', None)
        context.user_data.pop('compat_name1', None)
        return await show_numerology_menu(update, context)

    return NUMEROLOGY_COMPATIBILITY


# ============ УВЕДОМЛЕНИЯ ============

async def show_notifications_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await go_main(update, context)

    uid = update.effective_user.id
    settings = db.get_settings(uid)
    notif = settings.notifications

    days_map = {"Пн": "Понедельник", "Вт": "Вторник", "Ср": "Среда",
                "Чт": "Четверг", "Пт": "Пятница", "Сб": "Суббота", "Вс": "Воскресенье"}
    days_full = [days_map.get(day, day) for day in notif.days]
    days_str = ", ".join(days_full) if notif.days else "никогда"

    text = "⏰ **НАСТРОЙКА УВЕДОМЛЕНИЙ**\n\n"
    status = "✅ Включены" if notif.enabled else "❌ Отключены"
    text += f"**Статус:** {status}\n"
    text += f"**Время:** {notif.time}\n"
    text += f"**Дни:** {days_str}\n\n"

    text += "**Содержание:**\n"
    text += f"• Задачи: {'✅' if notif.content_tasks else '❌'}\n"
    text += f"• Рутина: {'✅' if notif.content_routine else '❌'}\n"
    text += f"• ЕГЭ: {'✅' if notif.content_ege else '❌'}\n\n"

    kb = ReplyKeyboardMarkup([
        [f"{'⏸️ Выключить' if notif.enabled else '▶️ Включить'}"],
        ["⏰ Установить время", "📅 Выбрать дни"],
        ["📋 Выбрать контент", "📊 Проверить"],
        ["↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    return NOTIFICATIONS_MENU


async def notifications_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    settings = db.get_settings(uid)

    if t == "↩️ Назад":
        return await go_main(update, context)

    elif t in ["▶️ Включить", "⏸️ Выключить"]:
        settings.notifications.enabled = not settings.notifications.enabled
        db.save_settings()

        if settings.notifications.enabled:
            await schedule_notifications(update, context, uid)
            await update.message.reply_text("✅ Уведомления включены!")
        else:
            await update.message.reply_text("⏸️ Уведомления выключены")

        return await show_notifications_menu(update, context)

    elif t == "⏰ Установить время":
        await update.message.reply_text(
            "Введите время в формате ЧЧ:ММ (например, 09:00):",
            reply_markup=back_kb()
        )
        return NOTIFICATIONS_SET_TIME

    elif t == "📅 Выбрать дни":
        days_keyboard = []
        for day in WeekDay:
            status = "✅" if day.value in settings.notifications.days else "❌"
            days_keyboard.append([f"{status} {day.value}"])
        days_keyboard.append(["✅ Готово", "↩️ Назад"])

        await update.message.reply_text(
            "Выберите дни для уведомлений:",
            reply_markup=ReplyKeyboardMarkup(days_keyboard, resize_keyboard=True)
        )
        return NOTIFICATIONS_SET_DAYS

    elif t == "📋 Выбрать контент":
        kb = ReplyKeyboardMarkup([
            [f"{'✅' if settings.notifications.content_tasks else '❌'} Задачи"],
            [f"{'✅' if settings.notifications.content_routine else '❌'} Рутина"],
            [f"{'✅' if settings.notifications.content_ege else '❌'} ЕГЭ"],
            ["✅ Готово", "↩️ Назад"]
        ], resize_keyboard=True)

        await update.message.reply_text(
            "Выберите, что включать в уведомления:",
            reply_markup=kb
        )
        return NOTIFICATIONS_SET_CONTENT

    elif t == "📊 Проверить":
        await send_test_notification(update, context)
        return NOTIFICATIONS_MENU

    return NOTIFICATIONS_MENU


async def notifications_set_time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "↩️ Назад":
        return await show_notifications_menu(update, context)

    try:
        time_str = update.message.text.strip()
        datetime.strptime(time_str, "%H:%M")

        uid = update.effective_user.id
        settings = db.get_settings(uid)
        settings.notifications.time = time_str
        db.save_settings()

        await update.message.reply_text(f"✅ Время установлено: {time_str}")

        if settings.notifications.enabled:
            await schedule_notifications(update, context, uid)

    except ValueError:
        await update.message.reply_text("❌ Неверный формат! Используйте ЧЧ:ММ (например, 09:00)")
        return NOTIFICATIONS_SET_TIME

    return await show_notifications_menu(update, context)


async def notifications_set_days_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    settings = db.get_settings(uid)

    if t == "↩️ Назад":
        return await show_notifications_menu(update, context)

    if t == "✅ Готово":
        return await show_notifications_menu(update, context)

    for day in WeekDay:
        if t.endswith(day.value):
            if day.value in settings.notifications.days:
                settings.notifications.days.remove(day.value)
            else:
                settings.notifications.days.append(day.value)
            db.save_settings()
            break

    days_keyboard = []
    for day in WeekDay:
        status = "✅" if day.value in settings.notifications.days else "❌"
        days_keyboard.append([f"{status} {day.value}"])
    days_keyboard.append(["✅ Готово", "↩️ Назад"])

    await update.message.reply_text(
        "Выберите дни для уведомлений:",
        reply_markup=ReplyKeyboardMarkup(days_keyboard, resize_keyboard=True)
    )
    return NOTIFICATIONS_SET_DAYS


async def notifications_set_content_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    uid = update.effective_user.id
    settings = db.get_settings(uid)

    if t == "↩️ Назад":
        return await show_notifications_menu(update, context)

    if t == "✅ Готово":
        return await show_notifications_menu(update, context)

    if "Задачи" in t:
        settings.notifications.content_tasks = not settings.notifications.content_tasks
    elif "Рутина" in t:
        settings.notifications.content_routine = not settings.notifications.content_routine
    elif "ЕГЭ" in t:
        settings.notifications.content_ege = not settings.notifications.content_ege

    db.save_settings()

    kb = ReplyKeyboardMarkup([
        [f"{'✅' if settings.notifications.content_tasks else '❌'} Задачи"],
        [f"{'✅' if settings.notifications.content_routine else '❌'} Рутина"],
        [f"{'✅' if settings.notifications.content_ege else '❌'} ЕГЭ"],
        ["✅ Готово", "↩️ Назад"]
    ], resize_keyboard=True)

    await update.message.reply_text(
        "Выберите, что включать в уведомления:",
        reply_markup=kb
    )
    return NOTIFICATIONS_SET_CONTENT


async def schedule_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    settings = db.get_settings(user_id)

    if not settings.notifications.enabled:
        return

    current_jobs = context.job_queue.get_jobs_by_name(f"notify_{user_id}")
    for job in current_jobs:
        job.schedule_removal()

    time_parts = settings.notifications.time.split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1])

    days_map = {"Пн": 0, "Вт": 1, "Ср": 2, "Чт": 3, "Пт": 4, "Сб": 5, "Вс": 6}
    days_numbers = tuple(days_map[day] for day in settings.notifications.days if day in days_map)

    context.job_queue.run_daily(
        send_daily_notification,
        time=dt_time(hour=hour, minute=minute),
        days=days_numbers,
        data=user_id,
        name=f"notify_{user_id}"
    )


async def send_daily_notification(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    user_id = job.data

    settings = db.get_settings(user_id)
    if not settings.notifications.enabled:
        return

    today = date.today().strftime("%a")[:2]
    if today not in settings.notifications.days:
        return

    text = "⏰ **ЕЖЕДНЕВНОЕ УВЕДОМЛЕНИЕ**\n\n"

    if settings.notifications.content_tasks:
        tasks = db.get_tasks(user_id)
        urgent = db.get_urgent_tasks(user_id, days=3)
        if urgent:
            text += "📋 **Горящие задачи:**\n"
            for task in urgent[:3]:
                days_left = (task.deadline - datetime.now()).days
                text += f"• {task.name} — осталось {days_left} дн.\n"
            text += "\n"

    if settings.notifications.content_routine:
        routine = db.get_routine(user_id)
        text += "🔄 **Рутина сегодня:**\n"

        if routine.cigarettes:
            expected = routine.cigarettes.get_today_expected()
            text += f"🚬 Курить: {expected:.1f} {routine.cigarettes.unit}\n"

        if routine.teeth:
            days_since = (date.today() - routine.teeth.last_updated).days
            expected = routine.teeth.get_today_expected()
            if days_since >= expected:
                text += f"🦷 **Нужно почистить зубы!**\n"

        if routine.bath:
            days_since = (date.today() - routine.bath.last_updated).days
            expected = routine.bath.get_today_expected()
            if days_since >= expected:
                text += f"🚿 **Нужно помыться!**\n"

        text += "\n"

    if settings.notifications.content_ege:
        ege_settings = db.get_ege_subjects_settings(user_id)
        active_exams = []

        for subject, is_active in ege_settings.items():
            if is_active:
                exam_date = db.get_exam_date(user_id, subject)
                if exam_date:
                    days_left = (exam_date - date.today()).days
                    if 0 <= days_left <= 30:
                        subject_name = SUBJECT_NAMES_RU.get(subject, subject)
                        active_exams.append((days_left, subject_name))

        if active_exams:
            active_exams.sort()
            text += "📚 **Ближайшие экзамены:**\n"
            for days_left, subject_name in active_exams[:3]:
                text += f"• {subject_name} — через {days_left} дн.\n"

    try:
        await context.bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Ошибка отправки уведомления пользователю {user_id}: {e}")


async def send_test_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    text = "📊 **ТЕСТОВОЕ УВЕДОМЛЕНИЕ**\n\n"
    text += "Если вы это видите, значит уведомления настроены правильно!\n\n"

    settings = db.get_settings(user_id)
    text += f"⏰ Время: {settings.notifications.time}\n"
    text += f"📅 Дни: {', '.join(settings.notifications.days)}\n\n"

    text += "**Содержимое будет таким:**\n"
    if settings.notifications.content_tasks:
        text += "• Задачи\n"
    if settings.notifications.content_routine:
        text += "• Рутина\n"
    if settings.notifications.content_ege:
        text += "• ЕГЭ\n"

    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ============ КОМАНДЫ ДЛЯ ДАТ ЕГЭ ============

async def cmd_set_exam_date(update: Update, context: ContextTypes.DEFAULT_TYPE, subject: str):
    if not context.args:
        await update.message.reply_text(f"❌ Укажи дату!\nПример: /date_{subject} 01.06.2025")
        return

    try:
        exam_date = datetime.strptime(context.args[0], "%d.%m.%Y").date()
        if exam_date < date.today():
            await update.message.reply_text(f"❌ Дата уже прошла!")
            return

        uid = update.effective_user.id
        db.set_exam_date(uid, subject, exam_date)

        days_left = (exam_date - date.today()).days
        await update.message.reply_text(
            f"✅ Дата экзамена по {SUBJECT_NAMES_RU[subject]} установлена!\n"
            f"📅 {exam_date.strftime('%d.%m.%Y')}\n"
            f"⏳ Осталось дней: {days_left}"
        )

    except ValueError:
        await update.message.reply_text("❌ Неверный формат! Используй: ДД.ММ.ГГГГ")


async def cmd_date_informatics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "informatics")

async def cmd_date_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "math_profile")

async def cmd_date_society(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "society")

async def cmd_date_biology(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "biology")

async def cmd_date_english(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "english")

async def cmd_date_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "history")

async def cmd_date_physics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "physics")

async def cmd_date_russian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "russian")

async def cmd_date_literature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "literature")

async def cmd_date_geography(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "geography")

async def cmd_date_chemistry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "chemistry")

async def cmd_date_german(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "german")

async def cmd_date_french(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "french")

async def cmd_date_spanish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "spanish")

async def cmd_date_chinese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_set_exam_date(update, context, "chinese")


# ============ MAIN ============

async def post_start(application: Application):
    try:
        await application.bot.set_my_short_description(BOT_SHORT_DESCRIPTION)
        await application.bot.set_my_description(BOT_DESCRIPTION)
    except Exception as e:
        print(f"Ошибка установки описания: {e}")

    commands = [
        BotCommand("start", "🚀 Запустить бота"),
        BotCommand("premium", "💎 Статус подписки"),
        BotCommand("tariffs", "💰 Тарифы и оплата"),
        BotCommand("cancel", "❌ Отмена")
    ]
    try:
        await application.bot.set_my_commands(commands)
    except Exception as e:
        print(f"Ошибка установки команд: {e}")


def main():
    application = Application.builder().token(BOT_TOKEN).post_init(post_start).build()

    application.add_handler(PreCheckoutQueryHandler(pre_checkout))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    application.add_handler(CommandHandler("premium", cmd_premium_status))
    application.add_handler(CommandHandler("tariffs", show_payment_menu))

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            MAIN_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler)
            ],

            # МАТЕМАТИКА
            MATH_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_menu_handler)
            ],
            MATH_SQRT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_sqrt)
            ],
            MATH_LOG: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_log)
            ],
            MATH_BIN: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_bin)
            ],
            MATH_POW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_pow)
            ],
            MATH_FACTORIAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_factorial)
            ],
            MATH_PERCENT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_percent)
            ],
            MATH_AVG: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_avg)
            ],
            MATH_GCD_LCM: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_gcd_lcm)
            ],
            MATH_TRIG: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_trig)
            ],
            MATH_COMB: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_comb)
            ],
            MATH_EQ: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_eq)
            ],
            MATH_CONVERT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_math_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, math_convert)
            ],

            # ЕГЭ
            EGE_SUBJECTS: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, ege_subjects_handler)
            ],
            EGE_SUBJECT_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_ege_subjects),
                MessageHandler(filters.TEXT & ~filters.COMMAND, ege_subject_view_handler)
            ],
            EGE_CHEATSHEET_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_ege_subject_view),
                MessageHandler(filters.TEXT & ~filters.COMMAND, ege_cheatsheet_handler)
            ],
            EGE_TASK_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_ege_subject_view),
                MessageHandler(filters.TEXT & ~filters.COMMAND, ege_task_menu_handler)
            ],

            # ЗАДАЧИ
            TASKS_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, tasks_menu_handler)
            ],
            TASK_ADD_NAME: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_tasks_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_add_name)
            ],
            TASK_ADD_PRIORITY: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_tasks_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_add_priority)
            ],
            TASK_ADD_DEADLINE: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_tasks_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_add_deadline)
            ],
            TASK_MANAGE_SELECT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_tasks_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_manage_select)
            ],
            TASK_MANAGE_ACTION: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_tasks_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, task_manage_action)
            ],

            # БУФЕР
            BUFFER_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, buffer_menu_handler)
            ],
            BUFFER_PERSONAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_buffer_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, buffer_personal_handler)
            ],
            BUFFER_PASSWORDS: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_buffer_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, buffer_passwords_handler)
            ],
            BUFFER_BIRTHDAYS: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_buffer_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, buffer_birthdays_handler)
            ],

            # ТВОРЧЕСТВО
            CREATIVITY_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, creativity_menu_handler)
            ],
            CR_MUSIC_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_creativity_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_menu_handler)
            ],
            CR_MUSIC_ALBUM_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_album_add_handler)
            ],
            CR_MUSIC_LIST: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_album_select_handler)
            ],
            CR_MUSIC_ALBUM_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_list),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_album_detail_handler)
            ],
            CR_MUSIC_TRACK_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_detail),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_track_add_handler)
            ],
            CR_MUSIC_TRACK_EDIT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_detail),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_track_edit_handler)
            ],
            CR_MUSIC_LYRICS_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_detail),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_lyrics_handler)
            ],
            CR_MUSIC_CONCEPT_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_detail),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_concept_handler)
            ],
            CR_MUSIC_COVER_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_album_detail),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_cover_handler)
            ],
            CR_MUSIC_SEARCH: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_music_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, music_search_handler)
            ],

            CR_BOOKS_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_creativity_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, books_menu_handler)
            ],
            CR_BOOKS_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_books_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, books_add_handler)
            ],
            CR_BOOKS_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_books_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, books_select_handler)
            ],
            CR_BOOKS_SEARCH: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_books_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, books_search_handler)
            ],

            CR_POEMS_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_creativity_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, poems_menu_handler)
            ],
            CR_POEMS_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_poems_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, poems_add_handler)
            ],
            CR_POEMS_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_poems_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, poems_select_handler)
            ],
            CR_POEMS_SEARCH: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_poems_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, poems_search_handler)
            ],

            CR_ART_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_creativity_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, art_menu_handler)
            ],
            CR_ART_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_art_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, art_add_handler)
            ],
            CR_ART_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_art_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, art_select_handler)
            ],

            # ЦИТАТНИК
            QUOTE_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, quote_menu_handler)
            ],
            QUOTE_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_quote_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, quote_add)
            ],
            QUOTE_DELETE: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_quote_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, quote_delete)
            ],

            # ГОРОСКОП
            HOROSCOPE_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, horoscope_menu_handler)
            ],
            HOROSCOPE_SIGN: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_horoscope_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, horoscope_sign_handler)
            ],

            # ЗАМЕТКИ
            NOTES_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notes_menu_handler)
            ],
            NOTES_ADD: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_notes_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notes_add)
            ],
            NOTES_DELETE: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_notes_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notes_delete)
            ],

            # ГОЛОС
            VOICE_MENU: [
                MessageHandler(filters.VOICE, voice_transcribe),
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, voice_menu_handler),
            ],

            # НАСТРОЙКИ
            SETTINGS_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, settings_handler)
            ],

            # ПЛАТЕЖИ
            PAYMENT_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, payment_menu_handler)
            ],

            PROMO_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_payment_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, promo_input_handler)
            ],

            # РУТИНА
            ROUTINE_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, routine_menu_handler)
            ],
            ROUTINE_HABIT_SELECT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_routine_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, routine_menu_handler)
            ],
            ROUTINE_CIGARETTE_SELECT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_routine_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, cigarette_menu_handler)
            ],
            ROUTINE_CIGARETTE_GOAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_cigarette_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, cigarette_goal_handler)
            ],
            ROUTINE_CIGARETTE_CURRENT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_cigarette_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, cigarette_current_handler)
            ],
            ROUTINE_TEETH_GOAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_teeth_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, teeth_goal_handler)
            ],
            ROUTINE_TEETH_LAST: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_teeth_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, teeth_current_handler)
            ],
            ROUTINE_BATH_GOAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_bath_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bath_goal_handler)
            ],
            ROUTINE_BATH_LAST: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_bath_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, bath_current_handler)
            ],
            ROUTINE_MONEY_GOAL: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_money_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, money_goal_handler)
            ],
            ROUTINE_MONEY_INCOME: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_money_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, money_income_handler)
            ],
            ROUTINE_MONEY_DATE: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_money_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, money_add_handler)
            ],
            ROUTINE_CHECKIN: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_routine_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, checkin_value_handler)
            ],

            # НУМЕРОЛОГИЯ
            NUMEROLOGY_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, numerology_menu_handler)
            ],
            NUMEROLOGY_INPUT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_numerology_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, numerology_input_handler)
            ],
            NUMEROLOGY_VIEW: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_numerology_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, numerology_view_handler)
            ],
            NUMEROLOGY_COMPATIBILITY: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_numerology_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, numerology_compatibility_handler)
            ],

            # УВЕДОМЛЕНИЯ
            NOTIFICATIONS_MENU: [
                MessageHandler(filters.Regex('^↩️ Назад$'), go_main),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notifications_menu_handler)
            ],
            NOTIFICATIONS_SET_TIME: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_notifications_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notifications_set_time_handler)
            ],
            NOTIFICATIONS_SET_DAYS: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_notifications_menu),
                MessageHandler(filters.Regex('^✅ Готово$'), show_notifications_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notifications_set_days_handler)
            ],
            NOTIFICATIONS_SET_CONTENT: [
                MessageHandler(filters.Regex('^↩️ Назад$'), show_notifications_menu),
                MessageHandler(filters.Regex('^✅ Готово$'), show_notifications_menu),
                MessageHandler(filters.TEXT & ~filters.COMMAND, notifications_set_content_handler)
            ],
        },
        fallbacks=[CommandHandler("start", cmd_start), CommandHandler("cancel", cmd_cancel)],
        allow_reentry=True,
    )

    application.add_handler(conv)
    application.add_handler(MessageHandler(filters.VOICE, voice_transcribe))

    date_commands = {
        "informatics": cmd_date_informatics,
        "math_profile": cmd_date_math,
        "society": cmd_date_society,
        "biology": cmd_date_biology,
        "english": cmd_date_english,
        "history": cmd_date_history,
        "physics": cmd_date_physics,
        "russian": cmd_date_russian,
        "literature": cmd_date_literature,
        "geography": cmd_date_geography,
        "chemistry": cmd_date_chemistry,
        "german": cmd_date_german,
        "french": cmd_date_french,
        "spanish": cmd_date_spanish,
        "chinese": cmd_date_chinese
    }

    for subj, handler in date_commands.items():
        application.add_handler(CommandHandler(f"date_{subj}", handler))

    print("🚀 ГОНЗО БОТ v4.5 ЗАПУЩЕН!")
    print("=" * 60)
    print("📚 Предметов ЕГЭ: 15")
    print("🔄 РУТИНА: ИСПРАВЛЕНА!")
    print("🔢 НУМЕРОЛОГИЯ: ДОБАВЛЕНА!")
    print("⏰ УВЕДОМЛЕНИЯ: ДОБАВЛЕНЫ!")
    print("📅 ДАТА: УЛУЧШЕНА!")
    print("=" * 60)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()