from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router
from aiogram.types import FSInputFile
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

# Токен из переменной окружения
API_TOKEN = os.getenv("TGTOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# FSM состояния
class PriceForm(StatesGroup):
    waiting_for_price = State()

    # --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа/сборный/опт) ---
    # waiting_for_avia_price = State()
    waiting_for_bulk_price = State()
    waiting_for_bulk_weight = State()


exchange_rate_rub = 12
exchange_rate_usdt = 82


# =======================
#   AVIA / BULK / OPT
#   (временно не используется)
# =======================

# avia_price_items = [
#     "Кроссовки/Кеды/Туфли/Шлепанцы",
#     "Ботинки и обувь тяжелее 2кг",
#     "1 кг", "2 кг", "3 кг",
#     "Мобильный телефон", "Часы", "Ноутбук", "Сумка"
# ]
# AVIA_DELIVERY_COST = {
#     "Кроссовки/Кеды/Туфли/Шлепанцы": 2200,
#     "Ботинки и обувь тяжелее 2кг": 4000,
#     "1 кг": 2000,
#     "2 кг": 3800,
#     "3 кг": 5600,
#     "Мобильный телефон": 4300,
#     "Часы": 4300,
#     "Ноутбук": 5800,
#     "Сумка": 2000
# }

TARIFF_IMAGES = {
    "Сборный груз/Одежда": "photos/odezhda.jpg",
    "Хоз товар": "photos/hoz.jpg",
    "Обувь": "photos/obuv.jpg",
    "Мелкая бытовая техника": "photos/byt_tehnika.jpg",
    "Одно название продукта 18-25 дней": "photos/odno_18.jpg",
    "Одно название продукта 12-15 дней": "photos/odno_12.jpg",
    "Игрушки 12-15 дней": "photos/igrushki.jpg",
    "Носки 12-15 дней": "photos/noski.jpg",
    "Нижнее белье 12-15 дней": "photos/belbe12.jpg",
    "Нижнее белье 18-25 дней": "photos/belbe18.jpg",
    "Постельное белье/Полотенца 12-15 дней": "photos/post_belbe.jpg",
    "Продовольственная линия (еда, чипсы и т.д.)": "photos/eda.jpg"
}

CATEGORY_COST = {
    "Кроссовки": 1500,
    "Ботинки": 1800,
    "Кеды": 1400,
    "Шлепанцы / Сандали": 1300,
    "Туфли": 1500,
    "Пуховик": 1500,
    "Жилетка": 1300,
    "Парка": 1800,
    "Легкая куртка": 1200,
    "Худи / Толстовка": 1100,
    "Лонгслив": 900,
    "Футболка / рубашка": 800,
    "Топ": 750,
    "Пиджак": 1200,
    "Джинсы": 1100,
    "Шорты": 900,
    "Брюки": 1000,
    "Нижнее белье (муж)": 800,
    "Нижнее белье (жен)": 750,
    "Комплект нижнего белья": 1000,
    "Шапка": 900,
    "Кепка": 800,
    "Снуд": 950,
    "Теплый шарф": 800,
    "Легкий шарф": 750,
    "Очки": 700,
    "Часы": 800,
    "Украшения": 650,
    "Ремни": 1100,
    "Перчатки": 800,
    "Кошелек / Кардхолдер": 850,
    "1 пара": 650,
    "2 пары": 700,
    "3 пары": 750,
    "Женская сумка маленькая": 1000,
    "Женская сумка большая": 1200,
    "Рюкзак": 1200,
    "Дорожная сумка": 1400,
    "Сумка через плечо": 800,
    "Парфюм": 900,
    "Крем для лица / рук": 700,
    "Помада": 650,
    "Баскетбольный мяч": 1300,
    "Футбольный мяч": 1100,
    "Волейбольный мяч": 1000,
    "Шлем": 1600,
    "Labubu": 1100,
    "LEGO": 2000,
    # сюда потом легко добавишь другие категории
}

# ✅ Надбавка СДЭК (под ключ) — с запасом
SDEK_EXTRA = {
    # Обувь
    "Кроссовки": 2000,
    "Кеды": 2000,
    "Туфли": 2000,
    "Шлепанцы / Сандали": 2000,
    "Ботинки": 2500,

    # Верхняя одежда
    "Пуховик": 3500,
    "Парка": 3500,
    "Жилетка": 2500,
    "Легкая куртка": 2500,
    "Пиджак": 2000,
    "Худи / Толстовка": 2000,
    "Лонгслив": 1400,
    "Футболка / рубашка": 1200,
    "Топ": 1000,

    # Штаны
    "Джинсы": 1800,
    "Брюки": 1800,
    "Шорты": 1800,

    # Нижнее белье / носки
    "Нижнее белье (муж)": 1000,
    "Нижнее белье (жен)": 1000,
    "Комплект нижнего белья": 1600,
    "1 пара": 600,
    "2 пары": 800,
    "3 пары": 1000,

    # Головные уборы / шарфы
    "Шапка": 1000,
    "Кепка": 1000,
    "Снуд": 1000,
    "Теплый шарф": 1700,
    "Легкий шарф": 1300,

    # Аксессуары
    "Очки": 1000,
    "Часы": 1300,
    "Украшения": 1000,
    "Ремни": 1200,
    "Перчатки": 1000,
    "Кошелек / Кардхолдер": 1000,

    # Сумки / рюкзаки
    "Женская сумка маленькая": 2000,
    "Сумка через плечо": 3000,
    "Женская сумка большая": 3500,
    "Рюкзак": 3500,
    "Дорожная сумка": 4500,

    # Косметика
    "Парфюм": 1500,
    "Крем для лица / рук": 1500,
    "Помада": 1500,

    # Спорт
    "Баскетбольный мяч": 3000,
    "Футбольный мяч": 3000,
    "Волейбольный мяч": 3000,
    "Шлем": 3000,

    # Фигурки/LEGO
    "Labubu": 2500,
    "LEGO": 3000,
}

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧮 Калькулятор доставки с Poizon")],
        [KeyboardButton(text="❓ FAQ Вопросы и ответы")]
    ],
    resize_keyboard=True
)

# FAQ клавиатура
faq_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 FAQ (обязательно к прочтению)")],
        [KeyboardButton(text="❓ Что такое Poizon?")],
        [KeyboardButton(text="📱 Как пользоваться Poizon?")],
        [KeyboardButton(text="💰 Ценники на Poizon")],
        [KeyboardButton(text="📦 Как заказать?")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# ✅ Калькулятор доставки (только авто, сроки 20–30 дней)
delivery_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚚 Авто 20–30 дней")],
        # [KeyboardButton(text="🚛 Авто 20–30 дней (≥1500¥)")],
        # --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕМ ---
        # [KeyboardButton(text="✈️ Авиа 2–6 дней")],
         [KeyboardButton(text="📦 Сборный груз от 5 кг 25-45 дней")],
        # [KeyboardButton(text="📦 Опт от 50 кг")],
        [KeyboardButton(text="⬅️ Назад в меню")]
    ],
    resize_keyboard=True
)

# Выбор типа товара
item_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👟 Обувь"), KeyboardButton(text="🧥 Верхняя одежда")],
        [KeyboardButton(text="👖 Штаны"), KeyboardButton(text="👙 Нижнее белье")],
        [KeyboardButton(text="🧢 Головные уборы"), KeyboardButton(text="🧦 Носки")],
        [KeyboardButton(text="👜 Сумки / рюкзаки"), KeyboardButton(text="👓 Аксессуары")],
        [KeyboardButton(text="💄 Косметика")],
        [KeyboardButton(text="🏀 Спорт"), KeyboardButton(text="🐻 Фигурки/LEGO")],
        [KeyboardButton(text="⬅️ Назад к доставке")]
    ],
    resize_keyboard=True
)

# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (опт/50кг) ---
bulk_50kg_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сборный груз/Одежда")],
        [KeyboardButton(text="Хоз товар")],
        [KeyboardButton(text="Обувь")],
        [KeyboardButton(text="Мелкая бытовая техника")],
        [KeyboardButton(text="Выделенная линия для определенных типов товаров")],
        [KeyboardButton(text="⬅️ Назад к доставке")]
    ],
    resize_keyboard=True
)

dedicated_line_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Одно название продукта 18-25 дней")],
        [KeyboardButton(text="Одно название продукта 12-15 дней")],
        [KeyboardButton(text="Игрушки 12-15 дней")],
        [KeyboardButton(text="Носки 12-15 дней")],
        [KeyboardButton(text="Нижнее белье 12-15 дней")],
        [KeyboardButton(text="Нижнее белье 18-25 дней")],
        [KeyboardButton(text="Постельное белье/Полотенца 12-15 дней")],
        [KeyboardButton(text="Продовольственная линия (еда, чипсы и т.д.)")],
        [KeyboardButton(text="⬅️ Назад к категориям 50кг")]
    ],
    resize_keyboard=True
)

# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа) ---
# avia_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="👟 Обувь")],
#         [KeyboardButton(text="Одежда/Аксессуары")],
#         [KeyboardButton(text="Мобильный телефон")],
#         [KeyboardButton(text="Часы")],
#         [KeyboardButton(text="Ноутбук")],
#         [KeyboardButton(text="Сумка")],
#         [KeyboardButton(text="Сборный груз от 3 кг")],
#         [KeyboardButton(text="⬅️ Назад к доставке")]
#     ],
#     resize_keyboard=True
# )
# avia_shoes_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Кроссовки/Кеды/Туфли/Шлепанцы")],
#         [KeyboardButton(text="Ботинки и обувь тяжелее 2кг")],
#         [KeyboardButton(text="⬅️ Назад к авиа-категориям")]
#     ],
#     resize_keyboard=True
# )
# weight_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="1 кг"), KeyboardButton(text="2 кг"), KeyboardButton(text="3 кг")],
#         [KeyboardButton(text="⬅️ Назад к авиа-категориям")]
#     ],
#     resize_keyboard=True
# )


# Обувь
shoes_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Кроссовки")],
        [KeyboardButton(text="Ботинки"), KeyboardButton(text="Кеды")],
        [KeyboardButton(text="Шлепанцы / Сандали")],
        [KeyboardButton(text="Туфли")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура верхней одежды
outerwear_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Пуховик"), KeyboardButton(text="Жилетка")],
        [KeyboardButton(text="Парка"), KeyboardButton(text="Легкая куртка")],
        [KeyboardButton(text="Пиджак")],
        [KeyboardButton(text="Худи / Толстовка"), KeyboardButton(text="Лонгслив")],
        [KeyboardButton(text="Футболка / рубашка"), KeyboardButton(text="Топ")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура штанов
pants_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Джинсы")],
        [KeyboardButton(text="Брюки")],
        [KeyboardButton(text="Шорты")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура нижнего белья
underwear_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Нижнее белье (муж)")],
        [KeyboardButton(text="Нижнее белье (жен)")],
        [KeyboardButton(text="Комплект нижнего белья")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура головных уборов
headwear_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Шапка")],
        [KeyboardButton(text="Кепка")],
        [KeyboardButton(text="Снуд")],
        [KeyboardButton(text="Теплый шарф")],
        [KeyboardButton(text="Легкий шарф")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура аксессуаров
accessories_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Очки")],
        [KeyboardButton(text="Часы")],
        [KeyboardButton(text="Украшения")],
        [KeyboardButton(text="Ремни")],
        [KeyboardButton(text="Перчатки")],
        [KeyboardButton(text="Кошелек / Кардхолдер")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура носков
socks_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1 пара")],
        [KeyboardButton(text="2 пары")],
        [KeyboardButton(text="3 пары")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура сумки / рюкзаки
bags_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Женская сумка маленькая")],
        [KeyboardButton(text="Женская сумка большая")],
        [KeyboardButton(text="Рюкзак")],
        [KeyboardButton(text="Дорожная сумка")],
        [KeyboardButton(text="Сумка через плечо")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура косметики
cosmetics_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Парфюм")],
        [KeyboardButton(text="Крем для лица / рук")],
        [KeyboardButton(text="Помада")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура спорт
sport_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Баскетбольный мяч")],
        [KeyboardButton(text="Футбольный мяч")],
        [KeyboardButton(text="Волейбольный мяч")],
        [KeyboardButton(text="Шлем")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

# Клавиатура фигурок/LEGO
figures_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Labubu")],
        [KeyboardButton(text="LEGO")],
        [KeyboardButton(text="⬅️ Назад к категориям")]
    ],
    resize_keyboard=True
)

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оформить заказ", url="https://t.me/buyer_17teen")],
    [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="back_to_main")]
])

# ========== HANDLERS ==========

@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    user_name = message.from_user.first_name
    welcome_text = f"Привет, {user_name}!\nЯ чат-бот магазина 17teen shop 😇"
    await message.answer(welcome_text, reply_markup=main_keyboard)

@router.message(F.text == "🧮 Калькулятор доставки с Poizon")
async def calculator_handler(message: types.Message):
    await message.answer("Выберите тип доставки:", reply_markup=delivery_keyboard)

@router.message(F.text == "🚚 Авто 20–30 дней")
async def handle_auto_delivery(message: types.Message, state: FSMContext):
    await state.update_data(delivery_type=message.text)  # можно оставить, на расчёт больше не влияет
    await message.answer("Выберите тип товара:", reply_markup=item_type_keyboard)



# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа) ---
# @router.message(F.text == "✈️ Авиа 2–6 дней")
# async def handle_avia_delivery(message: types.Message, state: FSMContext):
#     await state.update_data(delivery_type=message.text)
#     await message.answer("Выберите категорию товара для авиа-доставки:", reply_markup=avia_keyboard)

@router.message(F.text == "📦 Сборный груз от 5 кг 25-45 дней")
async def handle_bulk_5kg_start(message: types.Message, state: FSMContext):
    await state.set_state(PriceForm.waiting_for_bulk_price)
    await message.answer(
        "📦 <b>Сборный груз от 5 кг</b>\n\n"
        "Введите общую стоимость всех товаров в юанях (¥):",
        reply_markup=ReplyKeyboardRemove()
    )
@router.message(PriceForm.waiting_for_bulk_price)
async def handle_bulk_5kg_price_input(message: types.Message, state: FSMContext):
    try:
        total_price_yuan = float(message.text.replace(",", "."))
        await state.update_data(total_price_yuan=total_price_yuan)
        await state.set_state(PriceForm.waiting_for_bulk_weight)
        await message.answer("Теперь укажите примерный вес груза в кг:")
    except ValueError:
        await message.answer("Введите корректное число стоимости в юанях (например: 5200 или 5200.5):")

@router.message(PriceForm.waiting_for_bulk_weight)
async def handle_bulk_5kg_weight_input(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text.replace(",", "."))

        if weight < 5:
            await message.answer(
                "⚠️ Сборный груз рассчитывается <b>от 5 кг</b>.\n"
                "Пожалуйста, укажите вес <b>5 кг или больше</b>."
            )
            return

        data = await state.get_data()
        total_price_yuan = float(data.get("total_price_yuan", 0))

        # Формула:
        # (стоимость товаров * курс) + (вес * 600) + 1000
        total_rub = (total_price_yuan * exchange_rate_rub) + (weight * 600) + 1000
        total_usdt = round(total_rub / exchange_rate_usdt)

        await message.answer(
            "📦 <b>Сборный груз от 5 кг</b>\n\n"
            f"Примерная стоимость выкупа и доставки <b>до Москвы</b>:\n"
            f"<b>{int(total_rub)} ₽</b> или <b>{total_usdt} USDT</b>\n\n"
            "⚠️ Стоимость <b>приблизительная</b> — точная будет известна после взвешивания на складе в Китае.\n\n"
            "⛔ <i>Важно:</i> это стоимость доставки только <b>до Москвы</b>.\n"
            "Доставку <b>СДЭК / ПЭК</b> до вашего города вы оплачиваете отдельно при получении.\n\n"
            "Для оформления заказа обратитесь к менеджеру 👉 <b>@buyer_17teen</b>",
            reply_markup=keyboard
        )

        await state.clear()

    except ValueError:
        await message.answer("Введите корректный вес в килограммах (например: 5 или 12.5):")

# @router.message(PriceForm.waiting_for_bulk_price)
# async def handle_bulk_price_input(message: types.Message, state: FSMContext):
#     try:
#         total_price_yuan = float(message.text.replace(",", "."))
#         await state.update_data(total_price_yuan=total_price_yuan)
#         await message.answer("Теперь укажите примерный вес груза в кг:")
#         await state.set_state(PriceForm.waiting_for_bulk_weight)
#     except ValueError:
#         await message.answer("Введите корректное число стоимости в юанях:")

# @router.message(PriceForm.waiting_for_bulk_weight)
# async def handle_bulk_weight_input(message: types.Message, state: FSMContext):
#     try:
#         weight = float(message.text.replace(",", "."))
#         data = await state.get_data()
#         total_price_yuan = data.get("total_price_yuan")
#
#         delivery_cost = total_price_yuan * exchange_rate_rub + weight * 700
#         delivery_cost_usdt = round(delivery_cost / exchange_rate_usdt)
#
#         await message.answer(
#             f"Примерная стоимость выкупа и доставки до Москвы: <b>{int(delivery_cost)} ₽</b> или <b>{delivery_cost_usdt} USDT</b>\n\n"
#             f"⚠️ Точная стоимость будет известна после взвешивания на складе в Китае.\n\n"
#             f"Для оформления заказа обратитесь к менеджеру 👉 <b>@buyer_17teen</b>",
#             reply_markup=keyboard
#         )
#         await state.clear()
#     except ValueError:
#         await message.answer("Введите корректный вес в килограммах:")

# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа) ---
# @router.message(F.text.in_(avia_price_items))
# async def ask_avia_price(message: types.Message, state: FSMContext):
#     selected_item = message.text
#     await state.update_data(avia_item=selected_item)
#     await state.set_state(PriceForm.waiting_for_avia_price)
#     photo_znak = "photos/znak.jpg"
#     photo1 = FSInputFile(photo_znak)
#     await message.answer_photo(photo1)
#     await message.answer(
#         "⚠️ Обратите внимание: товары со знаком \"приблизительно равно\" <b>(≈) не выкупаем</b>⛔!"
#     )
#     await message.answer(
#         f"Введите стоимость «{selected_item}» в юанях (¥):",
#         reply_markup=ReplyKeyboardRemove()
#     )

@router.message(F.text == "⬅️ Назад к доставке")
async def back_to_delivery(message: types.Message):
    await message.answer("Выберите тип доставки:", reply_markup=delivery_keyboard)

@router.message(F.text == "👟 Обувь")
async def handle_shoes_button(message: types.Message, state: FSMContext):
    data = await state.get_data()
    delivery_type = data.get("delivery_type", "")
    # --- авиа временно выключено ---
    # if "✈️" in delivery_type:
    #     await message.answer("Выберите тип обуви для авиа-доставки:", reply_markup=avia_shoes_keyboard)
    # else:
    await message.answer("Выберите категорию обуви:", reply_markup=shoes_keyboard)

@router.message(F.text == "👜 Сумки / рюкзаки")
async def show_bags_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=bags_keyboard)

# --- авиа временно выключено ---
# @router.message(F.text == "Одежда/Аксессуары")
# async def handle_clothes_in_air(message: types.Message):
#      await message.answer("Укажите примерный вес.\nЕсли вес меньше 1 кг, то доставка будет рассчитываться по тарифу 1 кг.", reply_markup=weight_keyboard)

@router.message(F.text == "🧥 Верхняя одежда")
async def show_outerwear_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=outerwear_keyboard)

@router.message(F.text == "👖 Штаны")
async def show_pants_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=pants_keyboard)

@router.message(F.text == "👙 Нижнее белье")
async def show_underwear_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=underwear_keyboard)

@router.message(F.text == "🧦 Носки")
async def show_socks_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=socks_keyboard)

@router.message(F.text == "🧢 Головные уборы")
async def show_headwear_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=headwear_keyboard)

@router.message(F.text == "👓 Аксессуары")
async def show_accessories_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=accessories_keyboard)

@router.message(F.text == "💄 Косметика")
async def show_cosmetics_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=cosmetics_keyboard)

@router.message(F.text == "🏀 Спорт")
async def show_sport_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=sport_keyboard)

@router.message(F.text == "🐻 Фигурки/LEGO")
async def show_figures_options(message: types.Message):
    await message.answer("Выберите подходящий раздел:", reply_markup=figures_keyboard)

# --- авиа временно выключено ---
# @router.message(F.text == "⬅️ Назад к авиа-категориям")
# async def back_to_avia_categories(message: types.Message):
#     await message.answer("Выберите категорию товара для авиа-доставки:", reply_markup=avia_keyboard)

@router.message(F.text.in_(CATEGORY_COST.keys()))
async def ask_price(message: types.Message, state: FSMContext):
    category = message.text
    await state.update_data(category=category)
    await state.set_state(PriceForm.waiting_for_price)
    photo_znak = "photos/znak.jpg"
    photo1 = FSInputFile(photo_znak)
    await message.answer_photo(photo1)
    await message.answer(
        "⚠️ Обратите внимание: товары со знаком \"приблизительно равно\" <b>(≈) не выкупаем</b>⛔!"
    )
    await message.answer(
        f"Введите стоимость товара \"{category}\" в юанях (¥):",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(PriceForm.waiting_for_price)
async def calculate_price(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        category = data.get("category")

        base_delivery_cost = CATEGORY_COST.get(category, 1500)
        sdek_extra = SDEK_EXTRA.get(category, 2000)  # если нет категории — возьмём 2000 запасом
        delivery_cost = base_delivery_cost + sdek_extra  # под ключ до СДЭК

        price_yuan = float(message.text.replace(",", "."))

        # Таможня 15% только для заказов от 1500¥
        customs_rub = 0
        if price_yuan >= 1500:
            customs_rub = price_yuan * exchange_rate_rub * 0.15

        # Основная логика по цене
        if price_yuan < 1500:
            total_rub = price_yuan * exchange_rate_rub + delivery_cost + 1000
        else:
            total_rub = (
                price_yuan * exchange_rate_rub
                + delivery_cost
                + customs_rub
                + 3.6825 * (price_yuan ** 0.8558)
            )

        total_usdt = round(total_rub / exchange_rate_usdt)

        note = (
            "✅ Это финальная стоимость <b>под ключ</b>.\n"
            "Доставка до ближайшего пункта <b>СДЭК</b> включена."
        )

        await message.answer(
            f"Итоговая стоимость для «{category}»:\n"
            f"<b>{int(total_rub)} ₽</b> или <b>{total_usdt} USDT</b>\n\n"
            f"{note}\n\n"
            f"Для оформления заказа обратитесь к менеджеру 👉 <b>@buyer_17teen</b>",
            reply_markup=keyboard
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число в юанях:")
        return

    await state.clear()


# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа) ---
# @router.message(PriceForm.waiting_for_avia_price)
# async def calculate_avia_price(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#         item = data.get("avia_item", "товар")
#         price_yuan = float(message.text.replace(",", "."))
#         delivery_cost = AVIA_DELIVERY_COST.get(item, 1500)
#
#         if price_yuan < 1500:
#             total_rub = price_yuan * exchange_rate_rub + delivery_cost + 1500
#         else:
#             total_rub = price_yuan * exchange_rate_rub + delivery_cost + 3.6825 * (price_yuan ** 0.8558)
#         total_usdt = round(total_rub / exchange_rate_usdt)
#
#         await message.answer(
#             f"Примерная стоимость для «{item}»:\n"
#             f"<b>{int(total_rub)} ₽</b> или <b>{total_usdt} USDT</b>\n\n"
#             f"Точная стоимость будет расчитана после взвешивания груза на нашем складе.\n\n"
#             f"Для оформления заказа обратитесь к менеджеру 👉 <b>@buyer_17teen</b>",
#             reply_markup=keyboard
#         )
#     except ValueError:
#         await message.answer("Пожалуйста, введите корректную сумму в юанях:")
#         return
#     await state.clear()

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: types.CallbackQuery):
    await callback.message.answer("Вы в главном меню:", reply_markup=main_keyboard)
    await callback.answer()

# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (авиа) ---
# @router.message(F.text == "Сборный груз от 3 кг")
# async def handle_bulk_delivery(message: types.Message):
#     await message.answer("Для расчета доставки напишите менеджеру 👉 @buyer_17teen")

@router.message(F.text == "⬅️ Назад к категориям")
async def back_to_categories(message: types.Message):
    await message.answer("Выберите тип товара:", reply_markup=item_type_keyboard)

@router.message(F.text == "❓ FAQ Вопросы и ответы")
async def faq_menu(message: types.Message):
    await message.answer("Выберите интересующий вас вопрос:", reply_markup=faq_keyboard)

@router.message(F.text == "📌 FAQ (обязательно к прочтению)")
async def faq_main(message: types.Message):
    await message.answer("https://telegra.ph/FAQ-03-24-21")

@router.message(F.text == "❓ Что такое Poizon?")
async def faq_what_is_poizon(message: types.Message):
    await message.answer("https://telegra.ph/CHto-takoe-Poizon-03-24-2")

@router.message(F.text == "📱 Как пользоваться Poizon?")
async def faq_how_to_use_poizon(message: types.Message):
    await message.answer("https://telegra.ph/Kak-polzovatsya-Poizon-03-25-3")

@router.message(F.text == "💰 Ценники на Poizon")
async def faq_prices_poizon(message: types.Message):
    await message.answer("https://t.me/shop_17teen/367")

@router.message(F.text == "📦 Как заказать?")
async def faq_how_to_order(message: types.Message):
    await message.answer("https://t.me/shop_17teen/363")

@router.message(F.text == "⬅️ Назад в меню")
async def back_to_menu(message: types.Message):
    await message.answer("Возвращаемся в меню:", reply_markup=main_keyboard)

# --- ВРЕМЕННО НЕ ИСПОЛЬЗУЕТСЯ (опт/50кг) ---
# @router.message(F.text == "📦 Опт от 50 кг")
# async def handle_bulk_50kg(message: types.Message):
#     await message.answer("Выберите категорию вашего груза:", reply_markup=bulk_50kg_keyboard)

# @router.message(F.text == "Выделенная линия для определенных типов товаров")
# async def handle_dedicated_line(message: types.Message):
#     await message.answer("Выберите подкатегорию:", reply_markup=dedicated_line_keyboard)

# @router.message(F.text.in_(TARIFF_IMAGES.keys()))
# async def send_tariff_image(message: types.Message):
#     category = message.text
#     photo_path = TARIFF_IMAGES[category]
#
#     try:
#         photo = FSInputFile(photo_path)
#         await message.answer_photo(photo)
#
#         await message.answer(
#             f"В таблице выше указаны тарифы на доставку в категории \"{category}\" , стоимость указана в $ за 1 кг.\n\n"
#             f"Для предварительного расчета и оформления заказа пишите 👉 <b>@buyer_17teen</b>",
#             reply_markup=keyboard
#         )
#     except FileNotFoundError:
#         await message.answer("❗ Фото с тарифами пока не загружено.")

# @router.message(F.text == "⬅️ Назад к категориям 50кг")
# async def back_to_50kg_categories(message: types.Message):
#     await message.answer("Выберите категорию вашего груза:", reply_markup=bulk_50kg_keyboard)

# RUN
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
