import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 建議先在終端機執行：pip install python-dotenv
# 並在同目錄下建立 .env 檔案，內容填入：
# LINE_TOKEN=你的Token
# LINE_USER_ID=你的UserID
from dotenv import load_dotenv
load_dotenv() 

def main():
    url = "https://www.mirrormedia.mg/section/mafalda"
    
    try:
        web = requests.get(url, timeout=10)
        web.raise_for_status() # 檢查 HTTP 狀態碼是否為 200
    except requests.RequestException as e:
        print(f"網頁請求失敗: {e}")
        return

    web.encoding = 'UTF-8'
    soup = BeautifulSoup(web.text, "html.parser")
    
    # 這裡的 class_ 未來極有可能會變動，需特別留意
    mafalda_list = soup.find_all('a', class_='eXHQwr')
    
    if not mafalda_list:
        print("警告：找不到符合的 HTML 標籤，網站架構可能已更改。")
        return

    # 取得環境變數中的金鑰
    line_token = os.getenv('LINE_TOKEN')
    line_user_id = os.getenv('LINE_USER_ID')
    
    if not line_token or not line_user_id:
        print("錯誤：找不到 LINE_TOKEN 或 LINE_USER_ID，請確認環境變數設定。")
        return

    headers = {
        'Authorization': f'Bearer {line_token}',
        'Content-Type': 'application/json'
    }

    # 設定檔案名稱與路徑
    time_string = datetime.now().strftime("%Y-%m-%d")
    filename = f"mafalda-{time_string}.txt"

    # 使用 with 語法自動管理檔案開關
    with open(filename, 'a', encoding='utf-8') as f:
        for item in mafalda_list:
            # 增加錯誤處理，避免因找不到標籤而導致程式崩潰
            title_tag = item.find('div', class_='bsRQQO')
            content_tag = item.find('div', class_='dylaxC')
            
            if title_tag and content_tag:
                title = title_tag.get_text(strip=True)
                content = content_tag.get_text(strip=True)
                message_content = f"{title}\n\n{content}"
                
                # 準備推播資料
                body = {
                    'to': line_user_id,
                    'messages': [{'type': 'text', 'text': message_content}]
                }
                
                # 執行 LINE 推播
                try:
                    req = requests.post('https://api.line.me/v2/bot/message/push', 
                                        headers=headers, 
                                        data=json.dumps(body).encode('utf-8'))
                    print(f"推播結果 ({title[:5]}...):", req.text)
                except requests.RequestException as e:
                    print(f"LINE 推播失敗: {e}")

                # 寫入本機檔案
                f.write(f"{title}\n{content}\n----------\n")
            else:
                print("跳過一筆資料：無法解析標題或內文，Class 名稱可能已跑版。")

if __name__ == "__main__":
    main()