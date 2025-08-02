import requests
from bs4 import BeautifulSoup
import csv

# Step 1: Send request to the website
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Find product containers
products = soup.select(".thumbnail")

# Step 3: Write product data to CSV
with open("products.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Product Name", "Price", "Rating"])

    for product in products:
        name = product.select_one(".title").get_text(strip=True)
        price = product.select_one(".pull-right.price").get_text(strip=True)
        rating = len(product.select("div.ratings span.glyphicon-star"))  # ✅ Corrected here
        writer.writerow([name, price, rating])

# Step 4: Read from CSV and generate HTML
with open("products.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

    html_content = '''
    <html>
    <head>
        <title>Product List</title>
        <style>
            body {
                font-family: Arial;
                background-color: #f0f0f0;
                padding: 20px;
            }
            table {
                width: 80%;
                margin: auto;
                border-collapse: collapse;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                background-color: white;
            }
            th, td {
                padding: 12px;
                border: 1px solid #ccc;
                text-align: center;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            caption {
                font-size: 1.5em;
                margin-bottom: 10px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <table>
            <caption>Product Information</caption>
            <tr>
    '''

    for header in rows[0]:
        html_content += f'<th>{header}</th>'
    html_content += '</tr>'

    for row in rows[1:]:
        html_content += '<tr>'
        for col in row:
            html_content += f'<td>{col}</td>'
        html_content += '</tr>'

    html_content += '''
        </table>
    </body>
    </html>
    '''

# Step 5: Save as HTML
with open("products.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Scraping done! Open 'products.html' to view the product table.")
