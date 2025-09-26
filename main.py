from decouple import config
from telegram.ext import ApplicationBuilder,ContextTypes,CommandHandler,MessageHandler,filters
from telegram import Update
from openai import OpenAI

ai_token = config('AI_TOKEN')
token = config("TOKEN") 

ai_client = OpenAI(api_key=ai_token)

async def start_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('سلام لطفا سوال خود را بنویسید 👇')
async def messsage_handler(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    wait_message = await update.message.reply_text('چند لحظه منتظر بمانید')
    response = await ask_ai(user_message)
    await wait_message.edit_text(response)
async def ask_ai(message):
    try:
        response = ai_client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{
                'role':'system',
                'content':'وظیفه تو پاسخ مربوط به مسائل مربوط به پشتیبانی از سایت می باشد. از پاسخ به سوالات خارج از موضوع بپرهیز'
            },
            {
                'role':'user',
                'content':message
            }])
        return response.choices[0].message.content
    except Exception as e:
        return 'خطا در برقراری ارتباط'
def main():
    
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start',callback=start_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,callback=messsage_handler))
    app.run_polling()

if __name__ == '__main__':
    main()