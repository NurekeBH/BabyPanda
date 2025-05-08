from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import requests

BOT_TOKEN = "7663338099:AAFtO9KiInm1jFNOQq-2RKSw_5SdqPMvnew"
API_URL = "http://127.0.0.1:8000/api/check-phone/"  # Django API

MANAGER_INFO = "Сіз VIP клиент ретінде тіркелмегенсіз.\nБайланыс: +7 777 123 4567"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton(text="Нөмірді жіберу", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(
        [[contact_button]], resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "VIP статус тексеру үшін нөміріңізді жіберіңіз:", reply_markup=reply_markup
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    await update.message.reply_text("Тексерілуде...")

    # Django API арқылы тексеру
    try:
        response = requests.get(API_URL, params={"phone": phone})
        data = response.json()
    except:
        await update.message.reply_text("Қате: сервер жауап бермеді.")
        return

    if data.get("exists"):
        # Mini Web App батырмасы
        await update.message.reply_text(
            "Сіз VIP клиентсіз!",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            text="🛍️ Тауарлар",
                            web_app=WebAppInfo(url="https://your-domain.kz/mini-app/"),
                        )
                    ]
                ],
                resize_keyboard=True,
            ),
        )
    else:
        await update.message.reply_text(MANAGER_INFO)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    print("Бот іске қосылды.")
    app.run_polling()
