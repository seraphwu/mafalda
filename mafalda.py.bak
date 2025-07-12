# -*- coding: utf-8 -*-

# 導入所需函式庫
# Import necessary libraries
import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

# --- 設定 --- #
# --- Configuration --- #

# LINE Bot 的權杖和目標使用者 ID
# 警告：請勿將您的權杖直接寫在程式碼中。建議使用環境變數。
# 如何設定環境變數:
#   - Windows: set LINE_BOT_TOKEN="您的權杖"
#   - Linux/macOS: export LINE_BOT_TOKEN="您的權杖"
# WARNING: Do not hardcode your token in the script. Use environment variables instead.
LINE_BOT_TOKEN = os.environ.get('LINE_BOT_TOKEN')
# 同樣地，建議將使用者 ID 也設為環境變數
# Similarly, it's recommended to set the user ID as an environment variable.
LINE_USER_ID = os.environ.get('LINE_USER_ID', 'U16ef4f263d22028c4cc741b6a4b08d40') # 如果未設定環境變數，則使用預設值

# 要爬取的目標網址
# The target URL to scrape
TARGET_URL = "https://www.mirrormedia.mg/section/mafalda"


def fetch_horoscope_data(url):
    """
    從鏡週刊網站爬取瑪法達星座運勢資料。
    Scrapes Mafalda's horoscope data from the Mirror Media website.

    Args:
        url (str): 要爬取的網頁 URL。
                   The URL of the page to scrape.

    Returns:
        list: 一個包含標題和內文的字典列表，如果失敗則返回空列表。
              A list of dictionaries containing titles and content, or an empty list on failure.
    """
    horoscopes = []
    try:
        # 發送 GET 請求並設定編碼為 UTF-8
        # Send a GET request and set encoding to UTF-8
        response = requests.get(url, timeout=10) # 設定 10 秒超時
        response.raise_for_status()  # 如果請求失敗 (e.g., 404, 500)，會拋出例外
        response.encoding = 'UTF-8'

        # 使用 BeautifulSoup 解析 HTML
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 根據 class name 找到所有星座運勢的區塊
        # Find all horoscope sections by class name
        mafalda_sections = soup.find_all('a', class_='kELWiM')

        if not mafalda_sections:
            print("錯誤：在頁面上找不到指定的星座運勢區塊 (class='kELWiM')。")
            return []

        # 遍歷每個區塊，提取標題和內文
        # Iterate through each section to extract the title and content
        for section in mafalda_sections:
            title = section.find('div', class_='gLDNwx')
            text = section.find('div', class_='tPyZl')
            
            if title and text:
                horoscopes.append({
                    "title": title.get_text(strip=True),
                    "text": text.get_text(strip=True)
                })
        return horoscopes

    except requests.exceptions.RequestException as e:
        print(f"錯誤：爬取網頁時發生網路錯誤: {e}")
        return []
    except Exception as e:
        print(f"錯誤：解析內容時發生未知錯誤: {e}")
        return []

def send_line_notify(message):
    """
    透過 LINE Notify 發送推播訊息。
    Sends a push message via LINE Notify.

    Args:
        message (str): 要發送的訊息內容。
                       The message content to send.
    """
    if not LINE_BOT_TOKEN:
        print("錯誤：找不到 LINE_BOT_TOKEN 環境變數，無法發送訊息。")
        return

    headers = {
        'Authorization': f'Bearer {LINE_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    body = {
        'to': LINE_USER_ID,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    try:
        # 發送 POST 請求到 LINE Messaging API
        # Send a POST request to the LINE Messaging API
        response = requests.post(
            'https://api.line.me/v2/bot/message/push',
            headers=headers,
            data=json.dumps(body).encode('utf-8'),
            timeout=10
        )
        response.raise_for_status()
        print(f"訊息發送成功: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"錯誤：發送 LINE 訊息時發生網路錯誤: {e}")

def save_to_file(content):
    """
    將內容附加到以日期命名的檔案中。
    Appends content to a file named with the current date.

    Args:
        content (str): 要寫入檔案的文字內容。
                       The text content to write to the file.
    """
    # 產生檔名，例如：mafalda-2025-07-12.txt
    # Generate a filename, e.g., mafalda-2025-07-12.txt
    filename = f"mafalda-{datetime.now().strftime('%Y-%m-%d')}.txt"
    
    try:
        # 使用 'with open' 可以確保檔案被正確關閉
        # Using 'with open' ensures the file is properly closed
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        print(f"錯誤：寫入檔案 {filename} 時發生錯誤: {e}")


# --- 主程式執行區 --- #
# --- Main Execution Block --- #
if __name__ == "__main__":
    print("開始執行瑪法達星座運勢爬蟲...")
    
    # 1. 爬取星座運勢資料
    # 1. Fetch horoscope data
    horoscopes = fetch_horoscope_data(TARGET_URL)
    
    if horoscopes:
        print(f"成功爬取到 {len(horoscopes)} 則運勢。")
        full_content_for_file = ""
        
        # 2. 遍歷每則運勢，發送 LINE 通知並準備存檔內容
        # 2. Iterate through horoscopes, send LINE notifications, and prepare content for saving
        for horoscope in horoscopes:
            # 組合訊息內容
            # Combine message content
            message_to_send = f"{horoscope['title']}\n\n{horoscope['text']}"
            
            # 發送 LINE 通知
            # Send LINE notification
            send_line_notify(message_to_send)
            
            # 準備要寫入檔案的完整內容
            # Prepare the full content to be written to the file
            full_content_for_file += message_to_send + "\n\n----------\n"
        
        # 3. 將所有運勢一次性寫入檔案
        # 3. Write all horoscopes to the file at once
        save_to_file(full_content_for_file)
        print(f"所有運勢已成功儲存。")
    else:
        print("未爬取到任何運勢資料，程式結束。")

    print("執行完畢。")
