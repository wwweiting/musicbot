from linebot.exceptions import (InvalidSignatureError)
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, PostbackEvent, TextSendMessage)
import os
from dotenv import load_dotenv
from activities import *
import pygsheets
from music import *


app = Flask(__name__)

load_dotenv()
TOKEN = os.getenv('DATABASE_TOKEN')
SECRET = os.getenv('DATABASE_SECRET')
line_bot_api = LineBotApi(TOKEN)
handler = WebhookHandler(SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    msg = event.message.text

    if '地區' in msg:
        message = FlexTemplateRegionText()
        line_bot_api.reply_message(event.reply_token, message)
    elif '北' in msg:
        region = '北'
        message = FlexTemplateRegion(region=region)
        line_bot_api.reply_message(event.reply_token, message)
    elif '中' in msg:
        region = '中'
        message = FlexTemplateRegion(region=region)
        line_bot_api.reply_message(event.reply_token, message)
    elif '南' in msg:
        region = '南'
        message = FlexTemplateRegion(region=region)
        line_bot_api.reply_message(event.reply_token, message)
    elif '時間' in msg:
        message = buttons_message1()
        line_bot_api.reply_message(event.reply_token, message)
    elif '推薦歌曲' in msg:
        message, artist = FlexTemplateMusic()
        message_band = FlexTemplateBand(artist)
        line_bot_api.reply_message(event.reply_token, (message, message_band))
    else:
        pass



credentials_path = 'google.json'
gc = pygsheets.authorize(service_file=credentials_path)


sh = gc.open_by_url('')
worksheet = sh.sheet1


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    postback_data = event.postback.data 
    selected_date = event.postback.params['date']

    all_data = worksheet.get_all_values()

    for index, row in enumerate(all_data):
        if row[0] == user_id:
            user_data_index = index
            break
    else:
        user_data_index = None
 
    if user_data_index is None:
        new_row = [user_id, None, None]
        worksheet.append_table([new_row], dimension='ROWS', overwrite=False)

        all_data = worksheet.get_all_values()

        user_data_index = next(index for index, row in enumerate(all_data) if row[0] == user_id)

    if postback_data == 'start_date':
        worksheet.update_value('B' + str(user_data_index + 1), selected_date)
        reply_text = f"你選的開始日期是 {selected_date} " # 提示選結束時間 or 分開按鈕
    elif postback_data == 'end_date':
        worksheet.update_value('C' + str(user_data_index + 1), selected_date)
        reply_text = f"你選的結束日期是 {selected_date} "

    all_data = worksheet.get_all_values()

    if all_data[user_data_index][1] and all_data[user_data_index][2]:
        start_date = all_data[user_data_index][1]
        end_date = all_data[user_data_index][2]
        message = FlexTemplateDate(start_date, end_date)
        line_bot_api.reply_message(event.reply_token, (TextSendMessage(text=reply_text), message))
        worksheet.delete_rows(user_data_index + 1)
    else:
        end_date_message = buttons_message2()
        line_bot_api.reply_message(event.reply_token, (TextSendMessage(text=reply_text), end_date_message))


if __name__ == "__main__":
    app.run(debug=True)
