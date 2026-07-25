import telebot
from telebot import types

TOKEN = "8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6827582403
CARD_NUMBER = "5054161019772965"
CARD_NAME = "امیرخانی"
MY_TELEGRAM_ID = "LowCull"  # آیدی تلگرام بدون @

# --- منوی اصلی شیشه‌ای ---
def main_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("🚀 خرید VPN", callback_data="cat_tunnel")
    b2 = types.InlineKeyboardButton("📱 شماره مجازی", callback_data="buy_num")
    b3 = types.InlineKeyboardButton("🤖 ساخت ربات تلگرام", callback_data="buy_bot")
    b4 = types.InlineKeyboardButton("💬 پشتیبانی", callback_data="support")
    markup.add(b1, b2)
    markup.add(b3, b4)
    return markup

# --- دستور /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"سلام {message.from_user.first_name} عزیز! 🌟\nبه فروشگاه خوش آمدید. لطفاً گزینه مورد نظر خود را انتخاب کنید:",
        reply_markup=main_inline_keyboard()
    )

# --- مدیریت کلیک روی دکمه‌ها ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # ۱. بخش VPN (مستقیم پلن‌های تانل)
    if call.data == "cat_tunnel":
        markup = types.InlineKeyboardMarkup(row_width=1)
        p1 = types.InlineKeyboardButton("💎 ۵ گیگابایت ⟷ ۵۰,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p2 = types.InlineKeyboardButton("💎 ۱۰ گیگابایت ⟷ ۹۹,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p3 = types.InlineKeyboardButton("💎 ۲۰ گیگابایت ⟷ ۱۷۹,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p4 = types.InlineKeyboardButton("💎 ۳۰ گیگابایت ⟷ ۲۶۵,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p5 = types.InlineKeyboardButton("💎 ۵۰ گیگابایت ⟷ ۳۸۹,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p6 = types.InlineKeyboardButton("💎 ۱۰۰ گیگابایت ⟷ ۶۹۹,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        p7 = types.InlineKeyboardButton("🌟 ۱۵۰ گیگابایت + هدیه ویژه ⟷ ۸۸۹,۰۰۰ تومان (دائمی)", callback_data="plan_pay")
        back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        markup.add(p1, p2, p3, p4, p5, p6, p7, back)
        bot.edit_message_text("⚡ **لیست پلن‌های اختصاصی تانل (بدون محدودیت زمانی):**\nلطفاً حجم مورد نظر خود را انتخاب کنید:", chat_id, message_id, reply_markup=markup, parse_mode="Markdown")

    # ۲. بخش شماره مجازی
    elif call.data == "buy_num":
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        markup.add(back)
        msg = (
            "📱 **خرید شماره مجازی:**\n\n"
            "🇺🇸 **ریجن آمریکا (+1):** ۲۵۰,۰۰۰ تومان\n"
            "🇨🇦 **ریجن کانادا (+1):** ۲۵۰,۰۰۰ تومان\n\n"
            f"💳 جهت خرید، مبلغ را به کارت زیر واریز کرده و **عکس فیش** را همین‌جا بفرستید:\n\n"
            f"`{CARD_NUMBER}`\n"
            f"بنام: **{CARD_NAME}**\n\n"
            "⚠️ همراه فیش مشخص کنید کدام ریجن را می‌خواهید."
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # ۳. بخش ساخت ربات (لینک مستقیم به پیوی)
    elif call.data == "buy_bot":
        markup = types.InlineKeyboardMarkup(row_width=1)
        pv_btn = types.InlineKeyboardButton("💬 گفتگو و ثبت سفارش در پیوی", url=f"https://t.me/{MY_TELEGRAM_ID}")
        back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        markup.add(pv_btn, back)
        msg = (
            "🤖 **خدمات طراحی و ساخت ربات تلگرام:**\n\n"
            "برای سفارش ربات اختصاصی، توضیحات و هماهنگی، مستقیم روی دکمه زیر کلیک کنید تا وارد پیوی بشید:"
        )
        bot.edit_message_text(msg, chat_id, message_id, reply_markup=markup)

    # ۴. کارت به کارت جهت خرید VPN
    elif call.data == "plan_pay":
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton("🔙 بازگشت به لیست پلن‌ها", callback_data="cat_tunnel")
        markup.add(back)
        msg = (
            "💳 **اطلاعات کارت جهت واریز وجه:**\n\n"
            f"مبلغ را به شماره کارت زیر واریز کرده و **رسید (عکس فیش)** را همین‌جا برای ما ارسال کنید:\n\n"
            f"`{CARD_NUMBER}`\n"
            f"بنام: **{CARD_NAME}**\n\n"
            "⏳ پس از ارسال فیش، اشتراک شما در کمترین زمان تحویل داده می‌شود."
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    # ۵. پشتیبانی
    elif call.data == "support":
        markup = types.InlineKeyboardMarkup(row_width=1)
        pv_btn = types.InlineKeyboardButton("💬 پیام به پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}")
        back = types.InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu")
        markup.add(pv_btn, back)
        bot.edit_message_text("💬 برای ارتباط با پشتیبانی، می‌توانید فیش/پیام خود را همین‌جا بفرستید یا مستقیم به پیوی پیام بدهید:", chat_id, message_id, reply_markup=markup)

    # بازگشت به منوی اصلی
    elif call.data == "main_menu":
        bot.edit_message_text(
            f"سلام {call.from_user.first_name} عزیز! 🌟\nبه فروشگاه خوش آمدید. لطفاً گزینه مورد نظر خود را انتخاب کنید:",
            chat_id,
            message_id,
            reply_markup=main_inline_keyboard()
        )

# --- دریافت فیش واریزی و ارسال برای ادمین ---
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

print("ربات با منوی کامل روشن شد...")
bot.infinity_polling()
