from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8476450459:AAGQJlFdAZkAdnKcIf3Cx22GsrzD3dcS0H4"
ADMIN_ID = 8406284178

# ===== MAHSULOTLAR =====
PRODUCTS = {
    "🍔 Burger": 25000,
    "🍟 Kartoshka": 15000,
    "🌭 Hot-dog": 18000,
    "🍕 Pizza": 45000,
    "🥤 Ichimlik": 10000,
}

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🍔 Buyurtma berish"],
        ["📍 Manzil", "📞 Aloqa"],
        ["📊 Statistika"]
    ]
    await update.message.reply_text(
        "🍟 Fast Food Buyurtma Botiga xush kelibsiz!",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ===== TEXT HANDLER =====
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # BUYURTMA
    if text == "🍔 Buyurtma berish":
        keyboard = [
            ["🍔 Burger", "🍟 Kartoshka"],
            ["🌭 Hot-dog", "🍕 Pizza"],
            ["🥤 Ichimlik"],
            ["⬅️ Orqaga"]
        ]
        await update.message.reply_text(
            "📋 Mahsulot tanlang:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # MAHSULOT TANLANDI
    elif text in PRODUCTS:
        context.user_data["product"] = text
        context.user_data["price"] = PRODUCTS[text]

        await update.message.reply_text(
            f"✅ {text} tanlandi\n"
            f"💰 Narxi: {PRODUCTS[text]} so‘m\n\n"
            "💳 To‘lov qiling:\n"
            "8600 1234 5678 9012\n"
            "👤 Jaxonbek A.\n\n"
            "📸 To‘lovdan so‘ng SKRINSHOT yuboring"
        )

    # MANZIL
    elif text == "📍 Manzil":
        await update.message.reply_text(
            "📍 Yetkazib berish manzili:\n"
            "Toshkent shahar\n"
            "📞 +998 90 123 45 67"
        )

    # ALOQA
    elif text == "📞 Aloqa":
        await update.message.reply_text(
            "📞 Operator bilan aloqa:\n"
            "@abduvaliyevv16\n"
            
        )

    # STATISTIKA
    elif text == "📊 Statistika":
        if update.message.from_user.id != ADMIN_ID:
            await update.message.reply_text("❌ Siz admin emassiz")
            return
        await update.message.reply_text(
            "📊 Statistika (demo):\n"
            "🛒 Buyurtmalar: 0\n"
            "💰 Jami: 0 so‘m"
        )

    # ORQAGA
    elif text == "⬅️ Orqaga":
        await start(update, context)

# ===== SKRINSHOT =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "product" not in context.user_data:
        await update.message.reply_text("❗ Avval mahsulot tanlang")
        return

    user = update.message.from_user
    product = context.user_data["product"]
    price = context.user_data["price"]

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"confirm_{user.id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user.id}")
        ]
    ])

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=(
            "🧾 Yangi buyurtma\n\n"
            f"👤 User: @{user.username}\n"
            f"🆔 ID: {user.id}\n"
            f"🍔 Mahsulot: {product}\n"
            f"💰 Narx: {price} so‘m"
        ),
        reply_markup=keyboard
    )

    await update.message.reply_text(
        "✅ Buyurtma yuborildi\n⏳ Admin tasdiqlashini kuting"
    )

    context.user_data.clear()

# ===== ADMIN TASDIQLASH =====
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")

    if action == "confirm":
        await query.edit_message_caption("✅ Buyurtma TASDIQLANDI")
        await context.bot.send_message(
            chat_id=int(user_id),
            text="✅ Buyurtmangiz tasdiqlandi!\n🚚 Yetkazib beriladi"
        )

    elif action == "reject":
        await query.edit_message_caption("❌ Buyurtma RAD ETILDI")
        await context.bot.send_message(
            chat_id=int(user_id),
            text="❌ Buyurtmangiz rad etildi\n📞 Operator bilan bog‘laning"
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(admin_callback))

    print("🤖 Fast Food Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()
