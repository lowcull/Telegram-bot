import sqlite3
import telebot
from telebot import types

TOKEN = "8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6827582403
CARD_NUMBER = "5054161019772965"
CARD_NAME = "امیرخانی"
MY_TELEGRAM_ID = "LowCull"

# دیکشنری برای مدیریت مراحل ربات (هم برای خرید کاربر و هم برای ارسال کانفیگ توسط ادمین)
user_states = {}

def init_db():
    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            plan_name TEXT,
            sub_name TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def main_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
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
    if message.chat.id != ADMIN_ID:
        user_states.pop(message.chat.id, None)
    welcome_text = (
        f"سلام {user_name} عزیز! 👋\n\n"
        "به ربات خدمات هوشمند ما خوش آمدید.\n"
        "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_inline_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = call.from_user.id
    bot.answer_callback_query(call.id)

    if call.data == "cat_tunnel":
        user_states.pop(chat_id, None)
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
        user_states[chat_id] = {"step": "waiting_for_sub_name", "plan": plan_name}
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton("لغو و بازگشت 🔙", callback_data="cat_tunnel")
        markup.add(back)
        
        msg = (
            f"📌 **پلن انتخابی: {plan_name}**\n\n"
            "✍️ لطفاً یک **نام دلخواه** برای این اشتراک (مثلاً نام خودت یا مدل گوشی) ارسال کن:"
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "free_test":
        user_states.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        bot.edit_message_text("🎁 برای دریافت اشتراک تست، لطفاً به پشتیبانی پیام دهید.", chat_id, message_id, reply_markup=markup)

    elif call.data == "my_subs":
        user_states.pop(chat_id, None)
        conn = sqlite3.connect("bot_database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT plan_name, sub_name FROM invoices WHERE user_id = ? AND status = 'تایید شده'", (user_id,))
        rows = cursor.fetchall()
        conn.close()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))

        if rows:
            subs_text = "📦 **سرویس‌های فعال شما:**\n\n"
            for row in rows:
                subs_text += f"🔹 پلن: {row[0]} ⟵ نام اشتراک: **{row[1]}** (دائمی)\n"
        else:
            subs_text = "🏷 در حال حاضر هیچ اشتراک فعالی برای شما ثبت نشده است."
            
        bot.edit_message_text(subs_text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "my_invoices":
        user_states.pop(chat_id, None)
        conn = sqlite3.connect("bot_database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT plan_name, sub_name, status FROM invoices WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))

        if rows:
            inv_text = "📋 **لیست فاکتورهای شما:**\n\n"
            for row in rows:
                inv_text += f"▪️ پلن {row[0]} ({row[1]}) ⟵ وضعیت: **{row[2]}**\n"
        else:
            inv_text = "📄 فاکتور ثبت‌شده‌ای یافت نشد."

        bot.edit_message_text(inv_text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "user_account":
        user_states.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        user = call.from_user
        msg = f"👤 **اطلاعات حساب کاربری:**\n\nنام: {user.first_name}\nشناسه تلگرام: `{user.id}`"
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "buy_num":
        user_states.pop(chat_id, None)
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
        user_states.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💬 گفتگو با پشتیبانی", url=f"https://t.me/{MY_TELEGRAM_ID}"),
            types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu")
        )
        bot.edit_message_text("🤖 برای سفارش طراحی و ساخت ربات اختصاصی، به پیوی مراجعه کنید:", chat_id, message_id, reply_markup=markup)

    elif call.data == "main_menu":
        user_states.pop(chat_id, None)
        user_name = call.from_user.first_name
        welcome_text = (
            f"سلام {user_name} عزیز! 👋\n\n"
            "به ربات خدمات هوشمند ما خوش آمدید.\n"
            "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
        )
        bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=main_inline_keyboard())

    # --- مدیریت تایید یا رد فیش توسط ادمین ---
    elif call.data.startswith("approve_") or call.data.startswith("reject_"):
        if user_id != ADMIN_ID:
            return
        
        parts = call.data.split("_")
        action = parts[0]
        target_user_id = int(parts[1])

        conn = sqlite3.connect("bot_database.db", check_same_thread=False)
        cursor = conn.cursor()

        if action == "approve":
            cursor.execute("UPDATE invoices SET status = 'تایید شده' WHERE user_id = ? AND status = 'در انتظار تایید'", (target_user_id,))
            conn.commit()
            conn.close()

            # تنظیم وضعیت ادمین برای اینکه لینک کانفیگ را برای این کاربر بفرستد
            user_states[ADMIN_ID] = {"step": "waiting_for_config", "target_user": target_user_id}
            
            bot.edit_message_caption("✅ فیش تایید شد.\n\n👇 **حالا لینک کانفیگ یا متن اشتراک را همین‌جا ارسال کنید تا برای کاربر فرستاده شود:**", chat_id, message_id)
        else:
            cursor.execute("UPDATE invoices SET status = 'رد شده' WHERE user_id = ? AND status = 'در انتظار تایید'", (target_user_id,))
            conn.commit()
            conn.close()
            bot.send_message(target_user_id, "❌ متأسفانه فیش واریزی شما توسط مدیریت **رد** شد.")
            bot.edit_message_caption("❌ این فیش رد شد.", chat_id, message_id)

# --- دریافت پیام‌های متنی (نام اشتراک توسط کاربر یا کانفیگ توسط ادمین) ---
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    # اگر ادمین در حال ارسال کانفیگ برای کاربر تاییدشده باشد
    if user_id == ADMIN_ID:
        if chat_id in user_states and user_states[chat_id].get("step") == "waiting_for_config":
            target_user_id = user_states[chat_id]["target_user"]
            config_text = message.text.strip()

            # ارسال کانفیگ به کاربر
            bot.send_message(
                target_user_id,
                f"🎉 **پرداخت شما تایید و اشتراک شما فعال شد!**\n\n"
                f"🔗 **لینک اتصال / کانفیگ شما:**\n`{config_text}`\n\n"
                f"می‌توانید از بخش «سرویس‌های من» سوابق خود را مشاهده کنید.",
                parse_mode="Markdown"
            )

            bot.reply_to(message, "✅ کانفیگ با موفقیت برای کاربر ارسال شد.")
            user_states.pop(chat_id, None)
        return

    # اگر کاربر عادی در حال فرستادن نام اشتراک باشد
    if chat_id in user_states and user_states[chat_id].get("step") == "waiting_for_sub_name":
        sub_name = message.text.strip()
        plan_name = user_states[chat_id]["plan"]

        conn = sqlite3.connect("bot_database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO invoices (user_id, user_name, plan_name, sub_name, status) VALUES (?, ?, ?, ?, ?)", 
                       (user_id, user_name, plan_name, sub_name, "در انتظار تایید"))
        conn.commit()
        conn.close()

        user_states.pop(chat_id, None)

        msg = (
            f"📌 **پلن:** {plan_name}\n"
            f"🏷 **نام اشتراک:** `{sub_name}`\n\n"
            "💳 **شماره کارت جهت واریز وجه:**\n\n"
            f"`{CARD_NUMBER}`\n"
            f"به نام: **{CARD_NAME}**\n\n"
            "📸 پس از واریز مبلغ، لطفاً **تصویر فیش واریزی** خود را همین‌جا ارسال کنید."
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    user = message.from_user
    if user.id == ADMIN_ID:
        return

    bot.reply_to(message, "✅ فیش شما دریافت شد. پس از بررسی توسط مدیریت، نتیجه به شما اعلام خواهد شد.")
    
    username = f"@{user.username}" if user.username else "ندارد"
    caption = (
        f"📩 **رسید پرداخت جدید:**\n\n"
        f"👤 نام: {user.first_name}\n"
        f"🆔 آیدی: {username}\n"
        f"🔢 آیدی عددی: `{user.id}`"
    )

    admin_markup = types.InlineKeyboardMarkup(row_width=2)
    admin_markup.add(
        types.InlineKeyboardButton("✅ تایید فیش", callback_data=f"approve_{user.id}"),
        types.InlineKeyboardButton("❌ رد فیش", callback_data=f"reject_{user.id}")
    )

    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)

bot.infinity_polling(skip_pending=True)
        
