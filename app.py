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
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
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
        # 其他訊息的處理
        pass


# 替換 'path/to/your/credentials.json' 為你的憑證 JSON 檔案的路徑
credentials_path = '/Users/wei/Desktop/Dlab/linebot/musicbot/google.json'
gc = pygsheets.authorize(service_file=credentials_path)

# 開啟你的 Google Sheets，替換 'Your Spreadsheet Name' 為你的表單名稱
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nh8DbHECrMCPBa1rTnouW9QCSE91tq6saEjhbWr_K-Y/edit#gid=0')
worksheet = sh.sheet1

# 在 Postback Event 中插入數據
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id  # 使用者的 ID
    postback_data = event.postback.data  # 'start_date' 或 'end_date'
    selected_date = event.postback.params['date']

    all_data = worksheet.get_all_values()

    # 找尋是否已經有相同 user_id 的資料
    for index, row in enumerate(all_data):
        if row[0] == user_id:
            user_data_index = index
            break
    else:
        user_data_index = None
 
    # 判斷user_id存不存在
    if user_data_index is None:
        new_row = [user_id, None, None]
        worksheet.append_table([new_row], dimension='ROWS', overwrite=False)

        # 重新獲取所有資料
        all_data = worksheet.get_all_values()

        # 找尋新加入的使用者資料的索引
        user_data_index = next(index for index, row in enumerate(all_data) if row[0] == user_id)

    # 更新開始、結束時間
    if postback_data == 'start_date':
        worksheet.update_value('B' + str(user_data_index + 1), selected_date)
        reply_text = f"你選的開始日期是 {selected_date} " # 提示選結束時間 or 分開按鈕
    elif postback_data == 'end_date':
        worksheet.update_value('C' + str(user_data_index + 1), selected_date)
        reply_text = f"你選的結束日期是 {selected_date} "

    # 重新得到完整的資料
    all_data = worksheet.get_all_values()

    if all_data[user_data_index][1] and all_data[user_data_index][2]:
        start_date = all_data[user_data_index][1]
        end_date = all_data[user_data_index][2]
            # 直接觸發活動查詢
        message = FlexTemplateDate(start_date, end_date)
        line_bot_api.reply_message(event.reply_token, (TextSendMessage(text=reply_text), message))
        worksheet.delete_rows(user_data_index + 1)
    else:
        end_date_message = buttons_message2()
        line_bot_api.reply_message(event.reply_token, (TextSendMessage(text=reply_text), end_date_message))


if __name__ == "__main__":
    app.run(debug=True)