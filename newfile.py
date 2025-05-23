from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '7832401196:AAEEEEzehGZhf0PWUMSZd1j2LI36AVi7nfE'
ADMIN_ID = 6994702413  # آیدی عددی ادمین (خودت)

CARD_NUMBER = '6037 9917 7446 9427'
CARD_NAME = 'مبین'

# متن ترفند کامل
TRICK_TEXT = """ترفند چت‌بات ChatGPT (رفع محدودیت):

وقتی در چت‌بات ChatGPT هستید و یه پیام لیمیت می‌گیرید که مثلاً زده:
«الان لیمیت هستید. دو ساعت بعد می‌تونید چت کنید»

**ترفند:**
مثلاً ساعت ۸ شب هستید و این لیمیت اومده. برید به:
تنظیمات گوشی > تاریخ و ساعت (Date & Time)
ساعت رو ۲ ساعت جلو ببرید (۸ میشه ۱۰)

برگردید توی ChatGPT... سورپرایز!
لیمیت برطرف شده!

**همین ترفند برای آپلود فایل هم هست**
مثلاً نوشته ۵ ساعت دیگه می‌تونی آپلود کنی؟ ساعت گوشی رو جلو ببر یا اگه نشد یه روز بزن جلو.

**نکته:** اگه ساعت لیمیت مشخص نیست یا نمیدانی ، یه روز کامل بزن جلو، حل میشه!
"""

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "خوش اومدی به رباتی که ترفند چت جی‌پی‌تی رو نامحدود بهت میگه، بدون خرید اکانت و اشتراک.\n"
        "اگر می‌خوای ترفند رو بدونی، کلمه «نامحدود» رو بفرست."
    )

def handle_text(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if "نامحدود" in text:
        update.message.reply_text(
            "کار ترفند خیلی آسونه!\n"
            "قیمت: 100 هزارتومن ناقابل.\n"
            "اگه می‌خوای شماره کارت رو بفرستم، کلمه «شماره کارت» رو بفرست."
        )

    elif "شماره کارت" in text:
        update.message.reply_text(
            f"شماره کارت:\n{CARD_NUMBER}\n"
            f"به‌نام: {CARD_NAME}\n\n"
            "بعد از واریز، لطفاً **رسید رو به‌صورت عکس بفرست**."
        )

def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].file_id
    caption = f"رسید واریز از @{user.username or 'کاربر بدون آیدی'}\nID: {user.id}\nبرای تأیید، روی این پیام ریپلای کن و بنویس: اوک"

    context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file, caption=caption)
    update.message.reply_text("رسید دریافت شد! منتظر تأیید باش...")

def confirm(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        original = update.message.reply_to_message.caption
        if original and "ID:" in original:
            lines = original.splitlines()
            for line in lines:
                if line.startswith("ID:"):
                    user_id = int(line.replace("ID:", "").strip())
                    context.bot.send_message(chat_id=user_id, text=TRICK_TEXT)
                    update.message.reply_text("ترفند برای کاربر ارسال شد.")
                    return
    update.message.reply_text("خطا در پردازش تأیید. مطمئن شو روی پیام رسید ریپلای کردی و نوشتی اوک.")

# اجرای ربات
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))
dp.add_handler(MessageHandler(Filters.reply & Filters.text, confirm))

print("ربات روشنه...")
updater.start_polling()
updater.idle()