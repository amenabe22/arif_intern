#!/usr/bin/env python

import logging
import telegram
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import __version__ as TG_VER

BOT_TOKEN = "6058027851:AAH0Wc7UUY5ab7E5mZ6l5QfOTn53GTiCv9E"
SHEET_TITLE = "Arifpay - Finance Intern Application List"

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

FULL_NAME, PHONE, EMAIL, AVAILABILITY, UNIVERSITY, DEPARTMENT, VOULENTEER, GPA, ADDRESS  = range(9)

# save data to google sheet
def upload_result(user_data):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('moyats-60dfd-52f57c83cf27.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_TITLE).sheet1
    sheet.append_row([user_data['full_name'], user_data['phone_number'], user_data['email'], user_data['availability'], user_data['university'], user_data['department'], user_data['voulenteer'], user_data['gpa'], user_data['address']])
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    await update.message.reply_text(
        "Hi! Welcome to ArifPay Bot. I will ask you a few questions to get to know you better. "
        "What is your Full Name?",
    )

    return FULL_NAME

async def name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the entered full name and asks for a phone number."""
    user = update.message.from_user
    logger.info("Full Name of %s: %s", user.first_name, update.message.text)
    context.user_data["full_name"] = update.message.text
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Share contact', request_contact=True)]])
    await update.message.reply_text(
        "I see! Please send me your phone number",
        reply_markup=reply_markup
    )
    return PHONE

async def phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Contact: %s: %s", user.first_name, update.message.contact.phone_number)
    context.user_data["phone_number"] = update.message.contact.phone_number
    await update.message.reply_text(
        "I see! Please send me your email address",
        reply_markup=ReplyKeyboardRemove()
    )
    return EMAIL

async def email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Email: %s: %s", user.first_name, update.message.text)
    all_options = ["Yes", "No"]
    context.user_data["email"] = update.message.text
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(option)] for option in all_options])
    await update.message.reply_text(
        "I see! Are you available in one week from this day?",
        reply_markup=reply_markup
    )
    return AVAILABILITY

async def availability_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Availability: %s: %s", user.first_name, update.message.text)
    context.user_data["availability"] = update.message.text
    all_unis = ["Addis Ababa Commerce", "Hilcoe"]
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(university)] for university in all_unis])
    await update.message.reply_text(
        "I see! Please send me your university name",
        reply_markup=reply_markup
    )
    return UNIVERSITY

async def university_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User University: %s: %s", user.first_name, update.message.text)
    context.user_data["university"] = update.message.text
    all_deps = ["Accounting & Finance", "Software Engineering",]
    reply_markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(dep)] for dep in all_deps])
    await update.message.reply_text(
        "I see! Please select a department you would like to join",
        reply_markup=reply_markup
    )
    return DEPARTMENT

async def department_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Department: %s: %s", user.first_name, update.message.text)
    context.user_data["department"] = update.message.text
    await update.message.reply_text(
        "I see! tell me about your experience voulenteering ?",
        reply_markup=ReplyKeyboardRemove()
    )
    return VOULENTEER

async def voulenteer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Voulenteering Experience: %s: %s", user.first_name, update.message.text)
    context.user_data["voulenteer"] = update.message.text
    await update.message.reply_text(
        "what's your GPA ?",
    )

    return GPA

async def gpa_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Address: %s: %s", user.first_name, update.message.text)
    context.user_data["gpa"] = update.message.text
    await update.message.reply_text(
        "what's your address ?",
    )

    return ADDRESS

async def address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User Address: %s: %s", user.first_name, update.message.text)
    context.user_data["address"] = update.message.text
    upload_result(context.user_data)
    await update.message.reply_text(
        "Thank you for your time. We will contact you soon",
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            PHONE: [MessageHandler(filters.CONTACT, phone_handler)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_handler)],
            AVAILABILITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, availability_handler)],
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, university_handler)],
            DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, department_handler)],
            VOULENTEER: [MessageHandler(filters.TEXT & ~filters.COMMAND, voulenteer_handler)],
            GPA: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpa_handler)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
