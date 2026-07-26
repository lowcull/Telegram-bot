import telebot
from telebot import types

TOKEN = "8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6827582403
CARD_NUMBER = "5054161019772965"
CARD_NAME = "امیرخانی"
MY_TELEGRAM_ID = "LowCull"

def main_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("🛒 خرید اشتراک جدید", callback_data="cat_tunnel")
    b2 = types.InlineKeyboardButton("🆓 دریافت اشتراک تست", callback_data="free_test")
    b3 = types.InlineKeyboardButton("🏷 اشتراک‌های من", callback_data="my_subs")
    b4 = types.InlineKeyboardButton("📄 فاکتورهای من", callback_data="my_invoices")
    b5 = types.InlineKeyboardButton("👤 حساب کاربری", callback_data="user_account")
    b6 = types.InlineKeyboardButton("📞 پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}")
    b7 = types.InlineKeyboardButton("📱 آموزش اتصال", url=f"https://t.me/{MY_TELEGRAM_ID}")
    b8 = types.InlineKeyboardButton("↗ سرویس گیمینگ", callback_data="gaming_service")
    b9 = types.InlineKeyboardButton("🤖 ساخت ربات تلگرام", callback_data="buy_bot")
    b10 = types.InlineKeyboardButton("📱 شماره مجازی", callback_data="buy_num")

    markup.add(b1)
    markup.add(b2)
    markup.add(b3, b4)
    markup.add(b5)
    markup.add(b6, b7)
    markup.add(b8)
    markup.add(b9, b10)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام Martin عزیز! 🌟\nبه فروشگاه خوش آمدید. لطفاً گزینه مورد نظر خود را انتخاب کنید:",
        reply_markup=main_inline_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.answer_callback_query(call.id)

    if call.data == "cat_tunnel":
        markup = types.InlineKeyboardMarkup(row_width=1)
        p1 = types.InlineKeyboardButton("💎 ۵ گیگابایت ⟵ ۵۰,۰۰۰ تومان (دائمی)", callback_data="plan_5gb")
        p2 = types.InlineKeyboardButton("💎 ۱۰ گیگابایت ⟵ ۹۹,۰۰۰ تومان (دائمی)", callback_data="plan_10gb")
        p3 = types.InlineKeyboardButton("💎 ۲۰ گیگابایت ⟵ ۱۷۹,۰۰۰ تومان (دائمی)", callback_data="plan_20gb")
        p4 = types.InlineKeyboardButton("💎 ۳۰ گیگابایت ⟵ ۲۶۵,۰۰۰ تومان (دائمی)", callback_data="plan_30gb")
        p5 = types.InlineKeyboardButton("💎 ۵۰ گیگابایت ⟵ ۳۸۹,۰۰۰ تومان (دائمی)", callback_data="plan_50gb")
        p6 = types.InlineKeyboardButton("💎 ۱۰۰ گیگابایت ⟵ ۶۹۹,۰۰۰ تومان (دائمی)", callback_data="plan_100gb")
        p7 = types.InlineKeyboardButton("🌟 ۱۵۰ گیگابایت + هدیه ویژه ⟵ ۸۸۹,۰۰۰ تومان (دائمی)", callback_data="plan_150gb")
        back = types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="main_menu")
        markup.add(p1, p2, p3, p4, p5, p6, p7, back)
        bot.edit_message_text("⚡️ لیست پلن‌های اختصاصی تانل (بدون محدودیت زمانی):\nلطفاً حجم مورد نظر خود را انتخاب کنید:", chat_id, message_id, reply_markup=markup)

    elif call.data.startswith("plan_"):
        plan_name = call.data.replace("plan_", "").upper()
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton("بازگشت 🔙", callback_data="cat_tunnel")
        markup.add(back)
        msg = (
            f"📌 **انتخاب شما: پلن {plan_name}**\n\n"
            "💳 **اطلاعات کارت جهت واریز وجه:**\n\n"
            f"مبلغ را به شماره کارت زیر واریز کرده و **عکس فیش** را همین‌جا ارسال کنید:\n\n"
            f"`{CARD_NUMBER}`\n"
            f"بنام: **{CARD_NAME}**\n\n"
            "⏳ پس از ارسال فیش، اشتراک شما در کمترین زمان تحویل داده می‌شود."
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "free_test":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("🎁 برای دریافت اشتراک تست، لطفاً به پیوی پشتیبانی پیام دهید.", chat_id, message_id, reply_markup=markup)

    elif call.data == "my_subs":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("🏷 شما در حال حاضر هیچ اشتراک فعالی ندارید.", chat_id, message_id, reply_markup=markup)

    elif call.data == "my_invoices":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("📄 فاکتور ثبت‌شده‌ای یافت نشد.", chat_id, message_id, reply_markup=markup)

    elif call.data == "user_account":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        user = call.from_user
        msg = f"👤 **حساب کاربری شما:**\n\nنام: {user.first_name}\nشناسه کاربری: `{user.id}`"
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "gaming_service":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("↗ **سرویس گیمینگ اختصاصی:**\nبه زودی پلن‌های مخصوص بازی اضافه خواهند شد.", chat_id, message_id, reply_markup=markup)

    elif call.data == "buy_num":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        msg = (
            "📱 **خرید شماره مجازی:**\n\n"
            "🇺🇸 **ریجن آمریکا (+1):** ۲۵۰,۰۰۰ تومان\n"
            "🇨🇦 **ریجن کانادا (+1):** ۲۵۰,۰۰۰ تومان\n\n"
            f"💳 کارت واریز:\n`{CARD_NUMBER}`\nبنام: **{CARD_NAME}**"
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "buy_bot":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💬 گفتگو در پیوی", url=f"https://t.me/{MY_TELEGRAM_ID}"),
            types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu")
        )
        bot.edit_message_text("🤖 برای سفارش ساخت ربات تلگرام، به پیوی مراجعه کنید:", chat_id, message_id, reply_markup=markup)

    elif call.data == "main_menu":
        bot.edit_message_text(
            "سلام Martin عزیز! 🌟\nبه فروشگاه خوش آمدید. لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            chat_id, message_id,
            reply_markup=main_inline_keyboard()
        )

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.reply_to(message, "✅ فیش واریزی شما دریافت شد و برای بررسی به مدیریت ارسال گردید. با شما تماس خواهیم گرفت.")
    user = message.from_user
    username = f"@{user.username}" if user.username else "ندارد"
    caption = (
        f"📩 **فیش واریزی جدید دریافت شد!**\n\n"
        f"👤 **نام کاربر:** {user.first_name}\n"
        f"🆔 **آیدی:** {username}\n"
        f"🔢 **شناسه عددی:** `{user.id}`"
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")

print("ربات روی آیدی LowCull_shop_bot روشن شد...")
bot.infinity_polling()
