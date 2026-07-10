import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 允許本機使用 .env，若在 GitHub Actions 環境沒有裝 dotenv 也不會報錯中斷
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    url = "https://www.mirrormedia.mg/section/mafalda"
    
    try:
        web = requests.get(url, timeout=15)
        web.raise_for_status()
    except requests.RequestException as e:
        print(f"網頁請求失敗: {e}")
        return

    web.encoding = 'UTF-8'
    soup = BeautifulSoup(web.text, "html.parser")
    
    # 改抓所有「文章連結」
    article_links = soup.find_all('a', href=lambda href: href and '/story/' in href)
    
    # 讀取金鑰 (GitHub Secrets / 本機 .env)
    line_token = os.getenv('LINE_TOKEN')
    line_user_id = os.getenv('LINE_USER_ID')
    
    if not line_token or not line_user_id:
        print("錯誤：環境變數中找不到 LINE_TOKEN 或 LINE_USER_ID。")
        return

    headers = {
        'Authorization': f'Bearer {line_token}',
        'Content-Type': 'application/json'
    }

    time_string = datetime.now().strftime("%Y-%m-%d")
    filename = f"mafalda-{time_string}.txt"
    valid_count = 0

    with open(filename, 'a', encoding='utf-8') as f:
        # 使用 set 記錄處理過的 URL，避免重複推播
        processed_urls = set()
        
        for link in article_links:
            href = link.get('href')
            if href in processed_urls:
                continue
                
            # 抽出該 <a> 標籤內的所有純文字區塊並過濾掉空值
            texts = [t for t in link.stripped_strings if t]
            
            # 【功能修正】如果第一個區塊只是單純的分類標籤「瑪法達」，直接將它剔除
            if texts and texts[0] == "瑪法達":
                texts.pop(0)
            
            # 確保裡面還有文字，且開頭符合星座運勢的關鍵字特徵
            if texts and ("瑪法達" in texts[0] or "座" in texts[0] or "星" in texts[0]):
                title = texts[0]
                # 將剩餘的文字合併為內文
                content = "\n".join(texts[1:]) if len(texts) > 1 else ""
                
                # 組合最終推播訊息
                message_content = f"{title}\n\n{content}" if content else title
                
                # 準備推播資料
                body = {
                    'to': line_user_id,
                    'messages': [{'type': 'text', 'text': message_content}]
                }
                
                try:
                    req = requests.post(
                        'https://api.line.me/v2/bot/message/push',
                        headers=headers,
                        data=json.dumps(body).encode('utf-8'),
                        timeout=10
                    )
                    print(f"推播結果 [{title[:8]}...]: {req.text}")
                except requests.RequestException as e:
                    print(f"LINE 推播連線失敗: {e}")

                # 寫入本機檔案備份
                f.write(f"{title}\n{content}\n----------\n" if content else f"{title}\n----------\n")
                processed_urls.add(href)
                valid_count += 1
                
    if valid_count == 0:
        print("警告：完全沒有抓到任何文章。鏡週刊可能大幅度改版了。")
    else:
        print(f"✅ 執行完成！共抓取並成功推播了 {valid_count} 篇文章（已剔除重複的分類標題）。")

if __name__ == "__main__":
    main()