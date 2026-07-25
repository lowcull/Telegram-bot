import telebot
from telebot import types

API_TOKEN = '8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo'
MY_TELEGRAM_ID = "LowCull"  # آیدی پشتیبانی

bot = telebot.TeleBot(API_TOKEN)

# کیبورد اصلی ربات
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    b1 = types.KeyboardButton("🛍️ خرید VPN")
    b2 = types.KeyboardButton("📱 خرید شماره مجازی")
    b3 = types.KeyboardButton("💳 کارت به کارت و ارسال فیش")
    b4 = types.KeyboardButton("💬 پشتیبانی")
    markup.add(b1, b2)
    markup.add(b3, b4)
    return markup

# کیبورد پلن‌های VPN (با ایموجی‌های جدید و دکمه بازگشت)
def vpn_plans_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    p1 = types.InlineKeyboardButton("⚡️ 30 گیگ | 265 تومان (بدون زمان)", callback_data="plan_30g")
    p2 = types.InlineKeyboardButton("🚀 50 گیگ | 389 تومان (بدون زمان)", callback_data="plan_50g")
    p3 = types.InlineKeyboardButton("💎 100 گیگ | 699 تومان (بدون زمان)", callback_data="plan_100g")
    p4 = types.InlineKeyboardButton("🎁 150 گیگ(با هدیه) | 889 تومان (بدون زمان)", callback_data="plan_150g")
    back_btn = types.InlineKeyboardButton("🔙 بازگشت", callback_data="back_to_main")
    
    markup.add(p1, p2, p3, p4, back_btn)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "سلام! به فروشگاه LowCull خوش آمدید.\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_keyboard()
    )

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    text = message.text

    if text == "🛍️ خرید VPN":
        bot.send_message(
            message.chat.id,
            "لطفاً پلن اشتراک خود را انتخاب کنید:",
            reply_markup=vpn_plans_keyboard()
        )

    elif text == "📱 خرید شماره مجازی":
        bot.send_message(
            message.chat.id,
            "جهت استعلام موجودی و خرید شماره مجازی کشور مورد نظرتان، به پشتیبانی پیام دهید."
        )

    elif text == "💳 کارت به کارت و ارسال فیش":
        bot.send_message(
            message.chat.id,
            "شماره کارت جهت واریز:\n`6037-9979-0000-0000`\nبه نام: مارتین\n\nلطفاً بعد از واریز، عکس فیش واریزی را همین‌جا ارسال کنید.",
            parse_mode="Markdown"
        )

    elif text == "💬 پشتیبانی":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("ارتباط با پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}")
        markup.add(btn)
        bot.send_message(
            message.chat.id,
            "جهت ارتباط با پشتیبانی روی دکمه زیر کلیک کنید:",
            reply_markup=markup
        )

# پردازش دکمه‌های اینلاین (انتخاب پلن یا بازگشت)
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "back_to_main":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "منوی اصلی:", reply_markup=main_keyboard())
    elif call.data.startswith('plan_'):
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "✅ درخواست شما ثبت شد.\n\nلطفاً مبلغ مورد نظر را واریز کرده و عکس فیش واریزی را در همین چت ارسال کنید تا کانفیگ برای شما ارسال شود."
        )

# دریافت عکس فیش و ارسال به پشتیبانی
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    user_info = f"👤 کاربر: @{message.from_user.username}\nنام: {message.from_user.first_name}\nآیدی عددی: `{message.from_user.id}`"
    
    bot.send_photo(
        f"@{MY_TELEGRAM_ID}",
        message.photo[-1].file_id,
        caption=f"📥 **فیش واریزی جدید دریافت شد!**\n\n{user_info}",
        parse_mode="Markdown"
    )
    
    bot.reply_to(message, "✅ فیش شما با موفقیت برای پشتیبانی ارسال شد. به زودی بررسی و سرویس شما تحویل داده می‌شود.")

bot.infinity_polling()
