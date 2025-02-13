from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_open_site_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Открыть сайт тут", web_app=WebAppInfo(url="https://oknapb.ru/temp/"))
    return kb.as_markup()


def get_pharmacy_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Аптека получения", web_app=WebAppInfo(url="https://oknapb.ru/temp/pharmacy.html"))
    return kb.as_markup()


def get_search_buttons() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔎 Найти товар", switch_inline_query_current_chat="поиск товара: ")
    kb.button(text="🏥 Найти аптеку", switch_inline_query_current_chat="найти аптеку в: ")
    kb.adjust(2)
    return kb.as_markup()
