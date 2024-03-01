# Musicbot

## 簡介
這個LINE Bot可以透過時間或地區篩選查詢音樂祭資訊，也可以隨機推薦歌曲

## 程式檔案簡介
### app.py
整個LINE Bot的主程式
### activities.py
音樂祭活動的flex message，以及時間、地點的篩選
### music.py
歌曲介紹功能的flex message
### spotifyAPI.py
連接Spotify API搜集歌曲資訊
