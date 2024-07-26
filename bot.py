import os
import shutil
import subprocess
import zipfile
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def scrape_website(base_url, folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
    
    subprocess.run(['scrapy', 'crawl', 'download_files', '-a', f'base_url={base_url}'], cwd='website_scraper')
    
    if os.path.exists(folder) and os.listdir(folder):
        return folder
    else:
        return None

def zip_files(folder):
    zip_filename = f'{folder}.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder))
    return zip_filename

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('أرسل لي رابط الموقع الذي ترغب في تحميل ملفاته.')

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    folder = 'website_scraper/downloaded_website'
    
    try:
        scraped_folder = scrape_website(url, folder)
        if scraped_folder:
            update.message.reply_text(f'تم تحميل ملفات الموقع بنجاح. يتم الآن ضغط الملفات...')
            zip_filename = zip_files(folder)
            with open(zip_filename, 'rb') as f:
                context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(f, zip_filename))
            update.message.reply_text('تم إرسال الملفات المضغوطة بنجاح.')
        else:
            update.message.reply_text('لم يتم العثور على ملفات لتحميلها.')
    except Exception as e:
        update.message.reply_text(f'حدث خطأ أثناء تحميل ملفات الموقع: {e}')

def main():
    token = '7235293038:AAG9RdOV0AXcXxn32wY62njSc6wbPayjOvA'
    
    updater = Updater(token)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
