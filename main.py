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
    # منوی جدید بدون گزینه‌های اضافی و با چیدمان اختصاصی
    b1 = types.InlineKeyboardButton("🛒 ثبت سفارش و خرید اشتراک", callback_data="cat_tunnel")
    b2 = types.InlineKeyboardButton("🎁 دریافت تست رایگان", callback_data="free_test")
    b3 = types.InlineKeyboardButton("📦 سرویس‌های من", callback_data="my_subs")
    b4 = types.InlineKeyboardButton("📋 لیست فاکتورها", callback_data="my_invoices")
    b5 = types.InlineKeyboardButton("⚙️ پنل کاربری من", callback_data="user_account")
    b6 = types.InlineKeyboardButton("💬 ارتباط با پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}")
    b7 = types.InlineKeyboardButton("🤖 سفارش ساخت ربات", callback_data="buy_bot")
    b8 = types.InlineKeyboardButton("📱 بخش شماره‌های مجازی", callback_data="buy_num")

    markup.add(b1)
    markup.add(b2)
    markup.add(b3, b4)
    markup.add(b5)
    markup.add(b6)
    markup.add(b7, b8)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"سلام {user_name} عزیز! 👋\n\n"
        "به ربات خدمات هوشمند ما خوش آمدید.\n"
        "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=main_inline_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    bot.answer_callback_query(call.id)
    user_name = call.from_user.first_name

    if call.data == "cat_tunnel":
        markup = types.InlineKeyboardMarkup(row_width=1)
        p1 = types.InlineKeyboardButton("🔹 ۵ گیگابایت ⟵ ۵۰,۰۰۰ تومان", callback_data="plan_5gb")
        p2 = types.InlineKeyboardButton("🔹 ۱۰ گیگابایت ⟵ ۹۹,۰۰۰ تومان", callback_data="plan_10gb")
        p3 = types.InlineKeyboardButton("🔹 ۲۰ گیگابایت ⟵ ۱۷۹,۰۰۰ تومان", callback_data="plan_20gb")
        p4 = types.InlineKeyboardButton("🔹 ۳۰ گیگابایت ⟵ ۲۶۵,۰۰۰ تومان", callback_data="plan_30gb")
        p5 = types.InlineKeyboardButton("🔹 ۵۰ گیگابایت ⟵ ۳۸۹,۰۰۰ تومان", callback_data="plan_50gb")
        p6 = types.InlineKeyboardButton("🔹 ۱۰۰ گیگابایت ⟵ ۶۹۹,۰۰۰ تومان", callback_data="plan_100gb")
        p7 = types.InlineKeyboardButton("🌟 ۱۵۰ گیگابایت + هدیه ⟵ ۸۸۹,۰۰۰ تومان", callback_data="plan_150gb")
        back = types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="main_menu")
        markup.add(p1, p2, p3, p4, p5, p6, p7, back)
        bot.edit_message_text("📦 لطفاً حجم مورد نظر خود را انتخاب نمایید:", chat_id, message_id, reply_markup=markup)

    elif call.data.startswith("plan_"):
        plan_name = call.data.replace("plan_", "").upper()
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton("بازگشت 🔙", callback_data="cat_tunnel")
        markup.add(back)
        msg = (
            f"📌 **پلن انتخابی شما: {plan_name}**\n\n"
            "💳 **شماره کارت جهت واریز وجه:**\n\n"
            f"`{CARD_NUMBER}`\n"
            f"به نام: **{CARD_NAME}**\n\n"
            "📸 پس از واریز وجه، لطفاً **تصویر فیش واریزی** را همین‌جا ارسال کنید تا سرویس شما فعال شود."
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "free_test":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("🎁 برای دریافت اشتراک تست، لطفاً به پشتیبانی پیام دهید.", chat_id, message_id, reply_markup=markup)

    elif call.data == "my_subs":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("🏷 در حال حاضر هیچ اشتراک فعالی برای شما ثبت نشده است.", chat_id, message_id, reply_markup=markup)

    elif call.data == "my_invoices":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("📄 فاکتور پرداخت‌شده‌ای یافت نشد.", chat_id, message_id, reply_markup=markup)

    elif call.data == "user_account":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        user = call.from_user
        msg = f"👤 **اطلاعات حساب کاربری:**\n\nنام: {user.first_name}\nشناسه تلگرام: `{user.id}`"
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "buy_num":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        msg = (
            "📱 **تعرفه شماره‌های مجازی:**\n\n"
            "🇺🇸 آمریکا (+1): ۲۵۰,۰۰۰ تومان\n"
            "🇨🇦 کانادا (+1): ۲۵۰,۰۰۰ تومان\n\n"
            f"💳 کارت واریز:\n`{CARD_NUMBER}`"
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "buy_bot":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💬 گفتگو با پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}"),
            types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu")
        )
        bot.edit_message_text("🤖 برای سفارش طراحی و ساخت ربات اختصاصی، به پیوی مراجعه کنید:", chat_id, message_id, reply_markup=markup)

    elif call.data == "main_menu":
        welcome_text = (
            f"سلام {user_name} عزیز! 👋\n\n"
            "به ربات خدمات هوشمند ما خوش آمدید.\n"
            "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
        )
        bot.edit_message_text(
            welcome_text,
            chat_id, message_id,
            reply_markup=main_inline_keyboard()
        )

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.reply_to(message, "✅ فیش شما دریافت شد. پس از بررسی توسط مدیریت، اطلاعات سرویس برای شما ارسال خواهد شد.")
    user = message.from_user
    username = f"@{user.username}" if user.username else "ندارد"
    caption = (
        f"📩 **رسید پرداخت جدید:**\n\n"
        f"👤 نام: {user.first_name}\n"
        f"🆔 آیدی: {username}\n"
        f"🔢 آیدی عددی: `{user.id}`"
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")

bot.infinity_polling(skip_pending=True)
