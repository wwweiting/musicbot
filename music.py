import pygsheets
from oauth2client.service_account import ServiceAccountCredentials
from linebot.models import *
import random

# 設定憑證文件路徑
credentials_path = '/Users/wei/Desktop/Dlab/linebot/musicbot/google.json'
# 設定憑證範圍
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# 載入憑證
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = pygsheets.authorize(service_file=credentials_path)

shMusic = gc.open_by_url('https://docs.google.com/spreadsheets/d/1VA4In_Z_7MV4nI_ckfGaHaZXpvFaSlvrjaE2hXdrlQ8/edit#gid=0')
worksheetMusic = shMusic.sheet1
dfMusic = worksheetMusic.get_as_df()

shBand = gc.open_by_url('https://docs.google.com/spreadsheets/d/1VdCB8LcC4ul0bpguaGPT5OBPd0SaHnMrJQWidBApuMg/edit#gid=0')
worksheetBand = shBand.sheet1
dfBand = worksheetBand.get_as_df()
    

def FlexTemplateMusic():
    random_index = random.randint(0, len(dfMusic) - 1)
    random_song = dfMusic.iloc[random_index]
    
    music = random_song['music']
    link = random_song['link']
    artist = random_song['artist']
    message = TextSendMessage(text=f"聽聽看{artist}的《{music}》吧🎧\n{link}")
    return message, artist


def FlexTemplateBand(artist):
    df = dfBand[dfBand['artist'] == artist].iloc[0]

    message_band = FlexSendMessage(
        alt_text='推薦歌曲',
        contents={
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": f"{df['img']}",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "150:100",
                                "flex": 1
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "image",
                                        "url": f"{df['ig_img']}",
                                        "aspectMode": "cover",
                                        "size": "full"
                                    }
                                ],
                                "cornerRadius": "100px",
                                "width": "72px",
                                "height": "72px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "contents": [
                                            {
                                                "type": "span",
                                                "text": f"{df['artist']}",
                                                "weight": "bold",
                                                "color": "#000000",
                                                "size": "md"
                                            }
                                        ],
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "contents": [
                                            {
                                                "type": "span",
                                                "text": f"{df['info']}",
                                                "color": "#6C6C6C"
                                            }
                                        ],
                                        "size": "sm",
                                        "wrap": True
                                    }
                                ]
                            }
                        ],
                        "spacing": "xl",
                        "paddingAll": "20px"
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "更多資訊 🎸",
                            "uri": f"{df['ig_url']}"
                        },
                        "margin": "none",
                        "offsetBottom": "xs"
                    }
                ],
                "paddingAll": "0px"
            }
        }
  
)
    return message_band

