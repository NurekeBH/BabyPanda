from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import requests

BOT_TOKEN = "7663338099:AAFtO9KiInm1jFNOQq-2RKSw_5SdqPMvnew"  # ← Боттың токенін қойыңыз
DJANGO_API_URL = "https://baby-panda-backend.onrender.com/api/check-phone/"  # ← Localhost немесе live сервер URL

WEBAPP_URL = "https://marua.kz/"  # ← кейін Web App сілтемесі

MANAGER_INFO = "Сіз VIP клиент ретінде тіркелмегенсіз.\n" "Байланыс: +7 777 123 4567"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton(text="📱 Нөмірді жіберу", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(
        [[contact_button]], resize_keyboard=True, one_time_keyboard=True
    )
    await update.message.reply_text(
        "VIP клиент статусын тексеру үшін телефон нөміріңізді жіберіңіз:",
        reply_markup=reply_markup,
    )


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.contact.phone_number
    await update.message.reply_text("Тексерілуде...")

    try:
        response = requests.get(DJANGO_API_URL, params={"phone": phone})
        data = response.json()
    except Exception as e:
        await update.message.reply_text(f"Қате: сервермен байланыс жоқ.\n{str(e)}")
        return

    if data.get("exists"):
        await update.message.reply_text(
            "✅ Сіз VIP клиентсіз!",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            text="🛍️ Тауарларды көру", web_app=WebAppInfo(url=WEBAPP_URL)
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

    print("🤖 Telegram бот іске қосылды!")
    app.run_polling()
о


# https://api.telegram.org/bot7663338099:AAFtO9KiInm1jFNOQq-2RKSw_5SdqPMvnew/setWebhook?url=https://marua.kz/bot.php
