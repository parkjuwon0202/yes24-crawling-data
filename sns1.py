import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.yes24.com/product/category/bestseller?CategoryNumber=001&sumgb=06'
headers = {'User-Agent': 'Mozilla/5.0'}

res = requests.get(url, headers=headers)
res.raise_for_status()

soup = BeautifulSoup(res.text, 'html.parser')

book_items = soup.select('li[data-goods-no]')

# 크롤링 데이터 저장할 리스트
books = []

for item in book_items:
    rank_tag = item.select_one('em.ico.rank')
    rank = rank_tag.text.strip() if rank_tag else 'N/A'
    
    title_tag = item.select_one('a.gd_name')
    title = title_tag.text.strip() if title_tag else 'N/A'
    
    author_tag = item.select_one('span.authPub.info_auth a')
    author = author_tag.text.strip() if author_tag else 'N/A'
    
    publisher_tag = item.select_one('span.authPub.info_pub a')
    publisher = publisher_tag.text.strip() if publisher_tag else 'N/A'
    
    books.append({
        '순위': rank,
        '책제목': title,
        '저자': author,
        '출판사': publisher
    })

# 리스트를 데이터프레임으로 변환
df = pd.DataFrame(books)

# CSV로 저장
df.to_csv('yes24_bestseller.csv', index=False, encoding='utf-8-sig')

print("크롤링 완료, yes24_bestseller.csv 파일로 저장되었습니다.")
