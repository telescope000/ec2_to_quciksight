import csv

# 建立 orders.csv，並寫入欄位名稱
with open('orders.csv', mode='w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerow(['datetime','product','region','qty','price'])
