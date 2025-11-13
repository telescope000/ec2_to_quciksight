from flask import Flask, request, render_template_string
import csv, datetime, os, random
import requests

# --- 配置: 只需修改這裡的 Presigned URL ---
PRESIGNED_URL = "https://your-presigned-url"  # 外部生成的 URL

app = Flask(__name__)

# 將商品與地區改成英文，減少輸入錯誤
PRODUCTS = ['Phone', 'Laptop', 'Headphones', 'Mouse', 'Keyboard']
REGIONS = ['Taipei', 'New Taipei', 'Taichung', 'Kaohsiung', 'Tainan']

# --- 寫入訂單 CSV ---
def write_order(product, region, qty, price):
    if not os.path.exists('orders.csv'):
        with open('orders.csv', 'w', newline='') as f:
            csv.writer(f).writerow(['datetime','product','region','qty','price'])
    with open('orders.csv', 'a', newline='') as f:
        csv.writer(f).writerow([
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            product,
            region,
            qty,
            price
        ])

# --- 上傳 CSV 到 S3 (使用外部 Presigned URL) ---
def upload_to_s3():
    try:
        with open('orders.csv', 'rb') as f:
            response = requests.put(PRESIGNED_URL, data=f)
        if response.status_code == 200:
            return "✅ Upload Successful"
        else:
            return f"❌ Upload Failed: {response.status_code}, {response.text}"
    except Exception as e:
        return f"❌ Upload Error: {e}"

# --- Flask 路由 ---
@app.route('/', methods=['GET', 'POST'])
def order():
    message = ""
    if request.method == 'POST':
        if 'random_num' in request.form and request.form['random_num']:
            # 隨機生成多筆訂單
            n = int(request.form['random_num'])
            for _ in range(n):
                product = random.choice(PRODUCTS)
                region = random.choice(REGIONS)
                qty = random.randint(1, 10)
                price = round(random.uniform(100, 5000), 2)
                write_order(product, region, qty, price)
            message = f"✅ {n} Random Orders Generated!"
        else:
            # 手動下單
            write_order(
                request.form['product'],
                request.form['region'],
                int(request.form['qty']),
                float(request.form['price'])
            )
            message = "✅ Order Submitted!"

        # 上傳到 S3
        result = upload_to_s3()
        message += f" {result}"

    return render_template_string('''
        <h2>StarShop Order System</h2>
        <form method="post">
            Product: <input name="product"><br>
            Region: <input name="region"><br>
            Quantity: <input name="qty"><br>
            Price: <input name="price"><br><br>
            <input type="submit" value="Submit Order">
        </form>
        <hr>
        <h3>Generate Random Orders</h3>
        <form method="post">
            Number of Orders: <input name="random_num"><br><br>
            <input type="submit" value="Generate">
        </form>
        <p style="color:green;">{{ message }}</p>
    ''', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
