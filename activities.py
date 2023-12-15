import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from linebot.models import *

# 設定憑證文件路徑
credentials_path = '/Users/wei/Desktop/Dlab/linebot/musicbot/google.json'
# 設定憑證範圍
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# 載入憑證
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = pygsheets.authorize(service_file=credentials_path)

# 設定要讀取的 Google Sheets 名稱
sheet_name = 'activities'
# 開啟 Google Sheets
worksheet = gc.open(sheet_name).sheet1
# 將 Google Sheets 資料讀取到 Pandas DataFrame
df = worksheet.get_as_df()


# 類別,值
# 月份,地區 - 要有預設值
def FlexTemplateRegion(region = ''): 
    message = {
        "type" : "carousel",
        "contents" : []
    }

    if region != '':
         df1 = df[df['region'] == region].reset_index(drop = True)
         # df[df['region'] == region].reset_index(drop = True, inplace = True) #會更改到原本的df

    for a in range(len(df1)):
        # if df['region'][a] == region:  # 檢查地區條件
            review = {
            "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": f"{df1['pic_url'][a]}",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"{df1['name'][a]}",
            "weight": "bold",
            "size": "xl",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "日期｜",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": f"{df1['date'][a]}",
                    "size": "sm",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地點｜",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": f"{df1['place'][a]}",
                    "size": "sm",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "怎麼去 🗺️",
                  "uri": f"{df1['map_url'][a]}"
                },
                "margin": "sm"
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "了解更多 🎸",
                  "uri": f"{df1['ins_url'][a]}"
                },
                "margin": "sm"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }}
            message["contents"].append(review)

    if message["contents"]:  # 檢查是否有符合條件的 Bubble
        msg = FlexSendMessage(
            alt_text="相關活動",
            contents=message)
        return msg
    else:
        return None  # 如果沒有符合條件的 Bubble，可以回傳 None 或其他適當的值
    

def buttons_message1():
    message = TemplateSendMessage(
        alt_text='活動資訊',
        template=ButtonsTemplate(
            thumbnail_image_url='https://wallpapercrafter.com/desktop/201352-band-bass-death-and-metal-hd.jpg',
            title='開始時間',
            text='請選擇活動的開始時間',
            actions=[
                DatetimePickerTemplateAction(
                    label='點擊選擇',
                    data='start_date',
                    mode='date',
                    initial='2024-01-01',
                    max='2024-12-31',
                    min='2023-01-01'
                )]
        )
    )
    return message


def buttons_message2():
    message = TemplateSendMessage(
        alt_text='活動資訊',
        template=ButtonsTemplate(
            thumbnail_image_url='https://cdn.wallpapersafari.com/99/63/wyNrMG.jpg',
            title='結束時間',
            text='請選擇活動的結束時間',
            actions=[
                DatetimePickerTemplateAction(
                    label='點擊選擇',
                    data='end_date',
                    mode='date',
                    initial='2024-01-31',
                    max='2024-12-31',
                    min='2023-01-01'
                )]
        )
    )
    return message


def FlexTemplateDate(start_date, end_date): 
    message = {
        "type" : "carousel",
        "contents" : []
    }

    if start_date != '' and end_date != '':
        df_date1 = df[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)].reset_index(drop=True)

    for a in range(len(df_date1)):
        # if df['region'][a] == region:  # 檢查地區條件
            review = {
            "type": "bubble",
      "size": "kilo",
      "hero": {
        "type": "image",
        "url": f"{df_date1['pic_url'][a]}",
        "size": "full",
        "aspectMode": "cover",
        "aspectRatio": "320:213"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": f"{df_date1['name'][a]}",
            "weight": "bold",
            "size": "xl",
            "wrap": True
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "日期｜",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": f"{df_date1['date'][a]}",
                    "size": "sm",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "地點｜",
                    "size": "sm",
                    "color": "#8c8c8c",
                    "margin": "md",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": f"{df_date1['place'][a]}",
                    "size": "sm",
                    "color": "#666666"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "怎麼去 🗺️",
                  "uri": f"{df_date1['map_url'][a]}"
                },
                "margin": "sm"
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "了解更多 🎸",
                  "uri": f"{df_date1['ins_url'][a]}"
                },
                "margin": "sm"
              }
            ]
          }
        ],
        "spacing": "sm",
        "paddingAll": "13px"
      }}
            message["contents"].append(review)

    if message["contents"]:  # 檢查是否有符合條件的 Bubble
        msg = FlexSendMessage(
            alt_text="相關活動",
            contents=message)
        return msg
    else:
        return None


def FlexTemplateRegionText():

    messageRegionText = FlexSendMessage(
        alt_text='推薦歌曲',
        contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.roland.com/assets/images/products/categories/rct_v-drums_kit.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "請選擇活動地區",
        "weight": "bold",
        "size": "xl"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "北部",
          "text": "北部"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "中部",
          "text": "中部"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "南部",
          "text": "南部"
        },
        "height": "sm"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0,
    "action": {
      "type": "message",
      "label": "action",
      "text": "hello"
    }
  }
}
  
)
    return messageRegionText