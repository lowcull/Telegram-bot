const TOKEN = "8369466564:AAE5Bf6LjUPAGTzSwnry2donqyrvlO7Dxoo";
const ADMIN_ID = 6827582403;
const CARD_NUMBER = "5054161019772965";
const CARD_NAME = "امیرخانی";
const MY_TELEGRAM_ID = "LowCull";

const PANEL_URL = "https://vip-03.fl-sub.site:2096";
const PANEL_ADMIN_USERNAME = "Aras250g2";
const PANEL_ADMIN_PASSWORD = "HufGelpbrvnmR";

async function getMarzbanToken() {
    try {
        const response = await fetch(`${PANEL_URL}/api/admin/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `username=${encodeURIComponent(PANEL_ADMIN_USERNAME)}&password=${encodeURIComponent(PANEL_ADMIN_PASSWORD)}`
        });
        if (response.ok) {
            const data = await response.json();
            return data.access_token;
        }
    } catch (e) {
        console.error("Panel Token Error:", e);
    }
    return null;
}

async function sendTelegramMessage(chatId, text, replyMarkup = null) {
    let url = `https://api.telegram.org/bot${TOKEN}/sendMessage`;
    let body = { chat_id: chatId, text: text };
    if (replyMarkup) body.reply_markup = replyMarkup;

    await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
}

async function editMessageText(chatId, messageId, text, replyMarkup = null) {
    let url = `https://api.telegram.org/bot${TOKEN}/editMessageText`;
    let body = { chat_id: chatId, message_id: messageId, text: text };
    if (replyMarkup) body.reply_markup = replyMarkup;

    await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
}

export default {
    async fetch(request, env, ctx) {
        if (request.method !== "POST") {
            return new Response("Bot is running on Cloudflare Workers via GitHub!", { status: 200 });
        }

        try {
            const update = await request.json();

            if (update.message) {
                const msg = update.message;
                const chatId = msg.chat.id;
                const text = msg.text ? msg.text.trim() : "";
                const userName = msg.from.first_name || "کاربر";

                if (text === "/start") {
                    const welcomeText = `سلام ${userName} عزیز! 👋\n\nبه ربات خدمات هوشمند ما خوش آمدید.\nلطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:`;
                    const markup = {
                        inline_keyboard: [
                            [{ text: "🛒 ثبت سفارش و خرید اشتراک", callback_data: "cat_tunnel" }],
                            [{ text: "🎁 دریافت تست رایگان", callback_data: "free_test" }],
                            [{ text: "💬 ارتباط با پشتیبانی", url: `https://t.me/${MY_TELEGRAM_ID}` }]
                        ]
                    };
                    await sendTelegramMessage(chatId, welcomeText, markup);
                }
            } else if (update.callback_query) {
                const cq = update.callback_query;
                const chatId = cq.message.chat.id;
                const messageId = cq.message.message_id;
                const data = cq.data;

                await fetch(`https://api.telegram.org/bot${TOKEN}/answerCallbackQuery`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ callback_query_id: cq.id })
                });

                if (data === "cat_tunnel") {
                    const markup = {
                        inline_keyboard: [
                            [{ text: "🔹 ۵ گیگابایت (دائمی) ⟵ ۵۰,۰۰۰ تومان", callback_data: "plan_5gb_50000" }],
                            [{ text: "🔹 ۱۰ گیگابایت (دائمی) ⟵ ۹۹,۰۰۰ تومان", callback_data: "plan_10gb_99000" }],
                            [{ text: "بازگشت به منوی اصلی 🔙", callback_data: "main_menu" }]
                        ]
                    };
                    await editMessageText(chatId, messageId, "📦 لطفاً پلن دائمی مورد نظر خود را انتخاب نمایید:", markup);
                } else if (data === "main_menu") {
                    const welcomeText = `سلام کاربر عزیز! 👋\n\nبه ربات خدمات هوشمند ما خوش آمدید.\nلطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:`;
                    const markup = {
                        inline_keyboard: [
                            [{ text: "🛒 ثبت سفارش و خرید اشتراک", callback_data: "cat_tunnel" }],
                            [{ text: "🎁 دریافت تست رایگان", callback_data: "free_test" }],
                            [{ text: "💬 ارتباط با پشتیبانی", url: `https://t.me/${MY_TELEGRAM_ID}` }]
                        ]
                    };
                    await editMessageText(chatId, messageId, welcomeText, markup);
                }
            }
        } catch (err) {
            console.error("Webhook Error:", err);
        }

        return new Response("OK", { status: 200 });
    }
};
