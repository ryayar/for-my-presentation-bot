import random
import structlog
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton

from keyboards.open_site import get_open_site_kb, get_pharmacy_kb, get_search_buttons

# Declare router
router = Router()
router.message.filter(F.chat.type == "private")

# Declare logger
logger = structlog.get_logger()

PRODUCTS = {
    "Кагоцел таблетки 12мг 10шт": {
        "Ссылка на реестр": "https://grls.minzdrav.gov.ru/Grls_View_v2.aspx?routingGuid=28c3d2dc-d61f-4a6e-8be8-0a660b14a932",
        "Действующее вещество": "Кагоцел",
        "Полное торговое название": "Кагоцел",
        "Сфера применения": "Противовирусный",
        "Фармакологическая группа": "Противовирусное средство",
        "Зарегистрировано как": "Лекарственное средство",
        "Производитель": "Ниармедик Фарма ООО",
        "Страна производства": "Российская Федерация",
        "Код АТХ": "J05AX",
        "GTIN (штрих-код)": "04610020540019",
        "Дата регистрации": "19.11.2007",
        "Температура хранения": "T=+(02-25)C",
        "Возраст": "С 3 лет",
        "Дата перерегистрации": "24.02.2021\n",
        "Аналоги": "https://zdravcity.ru/analogs/kagocel/",
        "Способ применения и дозировка": (
            "*Препарат принимают внутрь, независимо от приема пищи.*\n\n"
            "🔹 *Взрослым* для лечения гриппа и ОРВИ:\n"
            "— В первые 2 дня: по 2 таб. 3 раза/сут.\n"
            "— В последующие 2 дня: по 1 таб. 3 раза/сут.\n"
            "— Всего на курс: 18 таб. (4 дня).\n\n"
            "🔹 *Профилактика гриппа и ОРВИ (взрослым)*:\n"
            "— 7-дневными циклами: 2 дня по 2 таб. 1 раз/сут, затем 5 дней перерыв.\n"
            "— Длительность курса: от 1 недели до нескольких месяцев.\n\n"
            "🔹 *Лечение герпеса*:\n"
            "— По 2 таб. 3 раза/сут в течение 5 дней.\n"
            "— Всего на курс: 30 таб. (5 дней).\n\n"
            "🔹 *Дети 3-6 лет (грипп, ОРВИ)*:\n"
            "— В первые 2 дня: по 1 таб. 2 раза/сут.\n"
            "— В последующие 2 дня: по 1 таб. 1 раз/сут.\n"
            "— Всего на курс: 6 таб. (4 дня).\n\n"
            "🔹 *Дети 6 лет и старше (грипп, ОРВИ)*:\n"
            "— В первые 2 дня: по 1 таб. 3 раза/сут.\n"
            "— В последующие 2 дня: по 1 таб. 2 раза/сут.\n"
            "— Всего на курс: 10 таб. (4 дня).\n\n"
            "🔹 *Профилактика у детей 3 лет и старше*:\n"
            "— 7-дневными циклами: 2 дня по 1 таб. 1 раз/сут, затем 5 дней перерыв.\n"
            "— Длительность курса: от 1 недели до нескольких месяцев."
        )
    }
}

PHARMACIES = {
    "москва": ["💊 Аптека №1 на Тверской", "💊 Аптека №2 у Кремля"],
    "питер": ["💊 Аптека на Невском", "💊 Аптека у Эрмитажа"],
    "новосибирск": ["💊 Аптека СибФарм", "💊 Здоровье Сибири"]
}


def get_product_keyboard(product_data) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🧪 Аналоги", url=product_data["Аналоги"]),
         InlineKeyboardButton(text="📜 Ссылка на реестр", url=product_data["Ссылка на реестр"])]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def generate_random_number(num_digits: int = 4) -> int:
    if num_digits < 1:
        raise ValueError("Количество цифр должно быть больше 0")

    min_value = 10 ** (num_digits - 1)  # Минимальное значение (например, 1000 для 4 цифр)
    max_value = 10 ** num_digits - 1  # Максимальное значение (например, 9999 для 4 цифр)

    return random.randint(min_value, max_value)


# Declare handlers
@router.message(Command("start"))
async def cmd_owner_hello(message: Message):
    args = message.text.split(" ", 1)
    ref_code = None

    if len(args) > 1 and args[1].startswith("ref-"):
        ref_code = args[1].replace("ref-", "")

    welcome_message = (
        "Поддерживается ссылка формата https://t.me/ForMyPresentationBot?start=ref-101412975\n\n"
        "/site - Отправляет кнопку с сайтом в фулскрине\n\n"
        "/check_code - Отправляет код авторизации на сайте\n\n"
        "/check_bitrix_code - Отправляет код авторизации в Bitrix\n\n"
        "/order - Отправляет номер заказа и кнопку с аптекой\n\n"
        "/code_order - Проверочный код для получения заказа\n\n"
        "/search - Поиск по товару и поиск аптеке"
    )

    if ref_code:
        welcome_message = f"🎉 Добро пожаловать!\nВаш реферальный код: <code>{ref_code}</code>\n\n" + welcome_message

    await message.answer(welcome_message)


@router.message(Command("site"))
async def cmd_site(message: Message):
    await message.answer("Открой сайт Здравсити прямо тут!\n"
                         "Ты не пожалеешь 👍", reply_markup=get_open_site_kb())


@router.message(Command("check_code"))
async def cmd_site(message: Message):
    code = await generate_random_number()
    await message.answer(f"<code>{code}</code>\nВаш код для авторизации на сайте Здравсити",
                         reply_markup=get_open_site_kb())


@router.message(Command("check_bitrix_code"))
async def cmd_site(message: Message):
    await message.answer("Код проверки телефона на Здравсити\n\n<code>9851</code>")


@router.message(Command("check_bitrix_code"))
async def cmd_site(message: Message):
    await message.answer("Код проверки телефона на Здравсити\n\n<code>9851</code>")


@router.message(Command("order"))
async def cmd_site(message: Message):
    code = await generate_random_number(10)
    await message.answer(f"Заказ <code>{code}</code> готов к выдаче.", reply_markup=get_pharmacy_kb())


@router.message(Command("code_order"))
async def cmd_site(message: Message):
    code = await generate_random_number()
    await message.answer(f"<code>{code}</code>\n\nПроверочный код для получения заказа")


@router.message(Command("search"))
async def cmd_site(message: Message):
    keyboard = get_search_buttons()
    await message.answer("Пример поиска товара или аптеки\n\n"
                         "Пример товара \"Кагоцел\"\n"
                         "Пример городов аптек \"москва\" и \"новосибирск\"", reply_markup=keyboard)


@router.inline_query()
async def inline_query_handler(query: InlineQuery):
    text = query.query.lower().strip()

    results = []

    if text.startswith("поиск товара:"):
        search_term = text.replace("поиск товара:", "").strip()

        matching_products = [product for product in PRODUCTS if search_term in product.lower()]

        if matching_products:
            for product in matching_products:
                product_data = PRODUCTS[product]

                description = "\n".join([
                    f"*{key}*: {value}" for key, value in product_data.items()
                    if key not in ["Ссылка на реестр", "Аналоги"]
                ])

                keyboard = get_product_keyboard(product_data)

                results.append(
                    InlineQueryResultArticle(
                        id=f"product_{product}",
                        title=f"🔎 {product}",
                        description=f"{product_data['Сфера применения']} | {product_data['Фармакологическая группа']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"📦 *{product}*\n\n{description}",
                            parse_mode="Markdown"
                        ),
                        reply_markup=keyboard
                    )
                )
        else:
            results.append(
                InlineQueryResultArticle(
                    id="no_product",
                    title="🚫 Товар не найден",
                    description="Попробуйте другой запрос.",
                    input_message_content=InputTextMessageContent(
                        message_text="❌ Товар не найден. Попробуйте другой запрос."
                    )
                )
            )
    elif text.startswith("найти аптеку в:"):
        city_part = text.replace("найти аптеку в:", "").strip()

        matching_cities = [city for city in PHARMACIES if city_part in city]

        if matching_cities:
            for city in matching_cities:
                pharmacies = "\n".join(PHARMACIES[city])
                results.append(
                    InlineQueryResultArticle(
                        id="pharmacy_" + city,
                        title=f"🏥 Аптеки в {city.capitalize()}",
                        description=f"Найдено {len(PHARMACIES[city])} аптек",
                        input_message_content=InputTextMessageContent(
                            message_text=f"🏥 Аптеки в {city.capitalize()}:\n\n{pharmacies}",
                            parse_mode="Markdown"
                        )
                    )
                )
        else:
            results.append(
                InlineQueryResultArticle(
                    id="no_pharmacy",
                    title="🚫 Аптеки не найдены",
                    description="Попробуйте другой город.",
                    input_message_content=InputTextMessageContent(
                        message_text="❌ Аптеки не найдены. Попробуйте другой населенный пункт."
                    )
                )
            )

    await query.answer(results, cache_time=1)
