import sqlite3
import telebot
from telebot import types
import urllib3
from flask import Flask
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TOKEN = "8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo"
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 6827582403
CARD_NUMBER = "5054161019772965"
CARD_NAME = "امیرخانی"
MY_TELEGRAM_ID = "LowCull"

user_states = {}

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def init_db():
    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            balance INTEGER DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            plan_name TEXT,
            sub_name TEXT,
            price INTEGER,
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
    b4 = types.InlineKeyboardButton("💳 کیف پول من", callback_data="wallet_menu")
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
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, user_name, balance) VALUES (?, ?, 0)", (user_id, user_name))
    conn.commit()
    conn.close()

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
    user_name = call.from_user.first_name
    bot.answer_callback_query(call.id)

    conn = sqlite3.connect("bot_database.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, user_name, balance) VALUES (?, ?, 0)", (user_id, user_name))
    conn.commit()

    if call.data == "cat_tunnel":
        user_states.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        p1 = types.InlineKeyboardButton("🔹 ۵ گیگابایت (دائمی) ⟵ ۵۰,۰۰۰ تومان", callback_data="plan_5gb_50000")
        p2 = types.InlineKeyboardButton("🔹 ۱۰ گیگابایت (دائمی) ⟵ ۹۹,۰۰۰ تومان", callback_data="plan_10gb_99000")
        p3 = types.InlineKeyboardButton("🔹 ۲۰ گیگابایت (دائمی) ⟵ ۱۷۹,۰۰۰ تومان", callback_data="plan_20gb_179000")
        p4 = types.InlineKeyboardButton("🔹 ۵۰ گیگابایت (دائمی) ⟵ ۳۸۹,۰۰۰ تومان", callback_data="plan_50gb_389000")
        p5 = types.InlineKeyboardButton("🔹 ۱۰۰ گیگابایت (دائمی) ⟵ ۶۹۹,۰۰۰ تومان", callback_data="plan_100gb_699000")
        p6 = types.InlineKeyboardButton("🔹 ۱۵۰ گیگابایت (دائمی) ⟵ ۸۰۰,۰۰۰ تومان", callback_data="plan_150gb_800000")
        back = types.InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="main_menu")
        markup.add(p1, p2, p3, p4, p5, p6, back)
        bot.edit_message_text("📦 لطفاً پلن دائمی مورد نظر خود را انتخاب نمایید:", chat_id, message_id, reply_markup=markup)

    elif call.data.startswith("plan_"):
        parts = call.data.split("_")
        plan_code = parts[1]
        price = int(parts[2])
        
        user_states[chat_id] = {"step": "waiting_for_sub_name", "plan": plan_code, "price": price}
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("لغو و بازگشت 🔙", callback_data="cat_tunnel"))
        
        msg = (
            f"📌 **پلن انتخابی:** {plan_code.upper()} (دائمی)\n"
            f"💵 **مبلغ:** {price:,} تومان\n\n"
            "✍️ لطفاً یک **نام انگلیسی دلخواه** بدون فاصله برای این اشتراک (مثلا `martin`) بفرست:"
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "wallet_menu":
        user_states.pop(chat_id, None)
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance_row = cursor.fetchone()
        balance = balance_row[0] if balance_row else 0

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("➕ افزایش موجودی کیف پول", callback_data="charge_wallet"),
            types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu")
        )
        msg = f"💳 **کیف پول کاربری شما:**\n\nموجودی فعلی: **{balance:,} تومان**"
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "charge_wallet":
        user_states[chat_id] = {"step": "waiting_for_wallet_charge"}
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("لغو 🔙", callback_data="wallet_menu"))
        msg = (
            "💳 **شارژ کیف پول:**\n\n"
            f"لطفاً مبلغ مورد نظر خود برای شارژ را به کارت زیر واریز کنید:\n\n"
            f"`{CARD_NUMBER}`\n"
            f"به نام: **{CARD_NAME}**\n\n"
            "📸 سپس **تصویر فیش واریزی** خود را همین‌جا ارسال کنید تا ادمین موجودی شما را شارژ کند."
        )
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "free_test":
        user_states.pop(chat_id, None)
        cursor.execute("SELECT id FROM invoices WHERE user_id = ? AND plan_name = 'تست رایگان'", (user_id,))
        already_got = cursor.fetchone()
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        
        if already_got:
            bot.edit_message_text("❌ شما قبلاً از اشتراک تست رایگان استفاده کرده‌اید.", chat_id, message_id, reply_markup=markup)
        else:
            user_states[chat_id] = {"step": "waiting_for_test_receipt", "plan": "تست رایگان", "price": 0, "sub": f"test_{user_id}"}
            msg = (
                "🎁 **درخواست تست رایگان (۱۰۰ مگابایت ۲۴ ساعته)**\n\n"
                "برای دریافت تست رایگان، لطفاً نام دلخواه یا اسکرین‌شات درخواست خود را ارسال کنید تا ادمین کانفیگ را برای شما ارسال کند."
            )
            bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "my_subs":
        user_states.pop(chat_id, None)
        cursor.execute("SELECT plan_name, sub_name FROM invoices WHERE user_id = ? AND status = 'تایید شده'", (user_id,))
        rows = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))

        if rows:
            subs_text = "📦 **سرویس‌های شما:**\n\n"
            for row in rows:
                subs_text += f"🔹 پلن: {row[0]} ⟵ نام: **{row[1]}**\n"
        else:
            subs_text = "🏷 در حال حاضر هیچ اشتراکی ثبت نشده است."
            
        bot.edit_message_text(subs_text, chat_id, message_id, reply_markup=markup)

    elif call.data == "user_account":
        user_states.pop(chat_id, None)
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance_row = cursor.fetchone()
        balance = balance_row[0] if balance_row else 0
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        msg = f"👤 **اطلاعات حساب کاربری:**\n\nنام: {user_name}\nشناسه: `{user_id}`\nموجودی کیف پول: **{balance:,} تومان**"
        bot.edit_message_text(msg, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "buy_num":
        user_states.pop(chat_id, None)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("بازگشت 🔙", callback_data="main_menu"))
        msg = (
            "📱 **تعرفه شماره‌های مجازی:**\n\n"
            "🇺🇸 آمریکا (+1): ۲۵۰,۰۰۰ تومان\n"
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
        bot.edit_message_text("🤖 برای سفارش ربات اختصاصی به پیوی مراجعه کنید:", chat_id, message_id, reply_markup=markup)

    elif call.data == "main_menu":
        user_states.pop(chat_id, None)
        welcome_text = (
            f"سلام {user_name} عزیز! 👋\n\n"
            "به ربات خدمات هوشمند ما خوش آمدید.\n"
            "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
        )
        bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=main_inline_keyboard())

    elif call.data.startswith("buyok_") or call.data.startswith("buyno_"):
        if user_id != ADMIN_ID:
            return
        parts = call.data.split("_")
        action = parts[0]
        target_user_id = int(parts[1])
        plan_name = parts[2]
        sub_name = parts[3]
        price = int(parts[4])

        if action == "buyok":
            user_states[ADMIN_ID] = {"step": "waiting_for_link_to_send", "target_user": target_user_id, "plan": plan_name, "sub": sub_name, "price": price}
            bot.send_message(ADMIN_ID, f"✍️ لطفاً **لینک اشتراک** مربوط به کاربر `{target_user_id}` را همین‌جا به عنوان متن بفرستید:")
            try:
                bot.edit_message_caption("⏳ در انتظار ارسال لینک از طرف شما...", chat_id, message_id, reply_markup=None)
            except Exception:
                pass
        else:
            bot.send_message(target_user_id, "❌ فیش واریزی یا درخواست شما توسط ادمین رد شد.")
            try:
                bot.edit_message_caption("❌ رد شد.", chat_id, message_id, reply_markup=None)
            except Exception:
                pass

    elif call.data.startswith("chargeok_") or call.data.startswith("chargeno_"):
        if user_id != ADMIN_ID:
            return
        parts = call.data.split("_")
        action = parts[0]
        target_user_id = int(parts[1])
        amount = int(parts[2])

        if action == "chargeok":
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, target_user_id))
            conn.commit()
            bot.send_message(target_user_id, f"✅ مبلغ {amount:,} تومان به کیف پول شما واریز شد!")
            try:
                bot.edit_message_caption("✅ شارژ کیف پول تایید شد.", chat_id, message_id, reply_markup=None)
            except Exception:
                pass
        else:
            bot.send_message(target_user_id, "❌ درخواست شارژ کیف پول شما رد شد.")
            try:
                bot.edit_message_caption("❌ رد شد.", chat_id, message_id, reply_markup=None)
            except Exception:
                pass

    conn.close()

@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    chat_id = message.chat.id
    
    if chat_id == ADMIN_ID and chat_id in user_states and user_states[chat_id].get("step") == "waiting_for_link_to_send":
        sub_url = message.text.strip()
        info = user_states[chat_id]
        target_user_id = info["target_user"]
        plan_name = info["plan"]
        sub_name = info["sub"]
        price = info["price"]

        conn = sqlite3.connect("bot_database.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO invoices (user_id, user_name, plan_name, sub_name, price, status) VALUES (?, ?, ?, ?, ?, ?)", 
                       (target_user_id, "کاربر", plan_name, sub_name, price, "تایید شده"))
        conn.commit()
        conn.close()

        bot.send_message(target_user_id, f"🎉 **پرداخت و سفارش شما تایید شد!**\n\n📦 پلن: {plan_name.upper()}\n🔗 **لینک اتصال شما:**\n`{sub_url}`", parse_mode="Markdown")
        bot.reply_to(message, "✅ لینک با موفقیت برای کاربر ارسال شد و فاکتور ثبت گردید.")
        user_states.pop(chat_id, None)
        return

    if chat_id not in user_states:
        return

    state_info = user_states[chat_id]

    if state_info.get("step") == "waiting_for_sub_name":
        sub_name = message.text.strip().lower()
        plan_name = state_info["plan"]
        price = state_info["price"]

        user_states[chat_id] = {"step": "waiting_for_payment_receipt", "plan": plan_name, "sub": sub_name, "price": price}
        
        msg = (
            f"🛒 **ثبت سفارش اشتراک {plan_name.upper()}**\n"
            f"💵 مبلغ قابل پرداخت: **{price:,} تومان**\n\n"
            f"لطفاً مبلغ را به کارت زیر واریز کنید:\n`{CARD_NUMBER}`\n"
            f"به نام: **{CARD_NAME}**\n\n"
            "📸 **اکنون عکس فیش واریزی خود را همین‌جا ارسال کنید.**"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    user = message.from_user
    if user.id == ADMIN_ID:
        if ADMIN_ID in user_states and user_states[ADMIN_ID].get("step") == "waiting_for_link_to_send":
            bot.reply_to(message, "لطفاً لینک اتصال (به صورت متن) را ارسال کنید، نه عکس!")
        return

    chat_id = message.chat.id
    
    if chat_id in user_states and user_states[chat_id].get("step") in ["waiting_for_payment_receipt", "waiting_for_test_receipt"]:
        state_info = user_states[chat_id]
        plan_name = state_info["plan"]
        sub_name = state_info["sub"]
        price = state_info["price"]

        bot.reply_to(message, "✅ تصویر فیش شما دریافت شد. پس از بررسی ادمین، لینک اتصال برای شما ارسال خواهد شد.")
        
        caption = (
            f"📩 **درخواست جدید (تایید دستی):**\n\n"
            f"👤 نام: {user.first_name}\n"
            f"🆔 آیدی عددی: `{user.id}`\n"
            f"📦 پلن: {plan_name.upper()}\n"
            f"✍️ نام اشتراک: `{sub_name}`\n"
            f"💵 مبلغ: {price:,} تومان"
        )

        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        admin_markup.add(
            types.InlineKeyboardButton("✅ تایید و ارسال لینک", callback_data=f"buyok_{user.id}_{plan_name}_{sub_name}_{price}"),
            types.InlineKeyboardButton("❌ رد درخواست", callback_data=f"buyno_{user.id}_0_0_0")
        )

        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)
        user_states.pop(chat_id, None)
    else:
        bot.reply_to(message, "✅ تصویر فیش شارژ کیف پول دریافت شد. پس از تایید ادمین، موجودی شما شارژ خواهد شد.")
        
        caption = (
            f"📩 **درخواست شارژ کیف پول:**\n\n"
            f"👤 نام: {user.first_name}\n"
            f"🆔 آیدی عددی: `{user.id}`"
        )

        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        admin_markup.add(
            types.InlineKeyboardButton("✅ شارژ ۵۰ تومانی", callback_data=f"chargeok_{user.id}_50000"),
            types.InlineKeyboardButton("✅ شارژ ۱۰۰ تومانی", callback_data=f"chargeok_{user.id}_100000"),
            types.InlineKeyboardButton("❌ رد درخواست", callback_data=f"chargeno_{user.id}_0")
        )

        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown", reply_markup=admin_markup)

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
            
